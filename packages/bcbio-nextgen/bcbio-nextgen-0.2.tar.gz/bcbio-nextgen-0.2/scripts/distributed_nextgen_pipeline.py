#!/usr/bin/env python
"""Run an automated analysis pipeline in a distributed cluster architecture.

Automate:
 - starting working nodes to process the data
 - kicking off an analysis
 - cleaning up nodes on finishing

Currently works on LSF managed clusters but is written generally to work
on other architectures.

Usage:
  run_distributed_job.py <config_file> <fc_dir> [<run_info_yaml>]
"""
import sys
import time
import math
import subprocess

import yaml

from bcbio.pipeline.run_info import get_run_info
from bcbio.distributed import lsf, sge

def main(config_file, fc_dir, run_info_yaml=None):
    with open(config_file) as in_handle:
        config = yaml.load(in_handle)
    assert config["algorithm"]["num_cores"] == "messaging", \
           "This script is used with configured 'messaging' parallelization"
    cluster = globals()[config["distributed"]["cluster_platform"]]
    workers_needed = _needed_workers(get_run_info(fc_dir, config, run_info_yaml)[-1])
    print "Starting cluster workers"
    jobids = start_workers(cluster, workers_needed, config, config_file)
    try:
        print "Running analysis"
        run_analysis(config_file, fc_dir, run_info_yaml, cluster, config)
    finally:
        print "Cleaning up cluster workers"
        stop_workers(cluster, jobids)

def start_workers(cluster, workers_needed, config, config_file):
    # we can manually specify workers or dynamically get as many as needed
    num_workers = config["distributed"].get("num_workers", None)
    if num_workers is None:
        cores_per_host = config["distributed"].get("cores_per_host", 1)
        if cores_per_host == 0:
            raise ValueError("Need to set num_workers if cores_per_host is determined dynamically")
        num_workers = int(math.ceil(float(workers_needed) / cores_per_host))
    program_cl = [config["analysis"]["worker_program"], config_file]
    args = config["distributed"]["platform_args"].split()
    jobids = [cluster.submit_job(args, program_cl) for _ in range(num_workers)]
    while not(cluster.are_running(jobids)):
        time.sleep(5)
    return jobids

def run_analysis(config_file, fc_dir, run_info_yaml, cluster, config):
    args = config["distributed"]["platform_args"].split()
    program_cl = [config["analysis"]["process_program"], config_file, fc_dir]
    if run_info_yaml:
        program_cl.append(run_info_yaml)
    jobid = cluster.submit_job(args, program_cl)
    try:
        _monitor_analysis(cluster, jobid)
    except:
        stop_workers(cluster, [jobid])
        raise

def _monitor_analysis(cluster, jobid):
    # wait for job to start
    while not(cluster.are_running([jobid])):
        time.sleep(5)
    # wait for job to finish
    while cluster.are_running([jobid]):
        time.sleep(5)

def stop_workers(cluster, jobids):
    for jobid in jobids:
        cluster.stop_job(jobid)

def _needed_workers(run_info):
    """Determine workers needed to run multiplex flowcells in parallel.
    """
    names = []
    for lane in run_info["details"]:
        for multiplex in lane.get("multiplex", [{"barcode_id": ""}]):
            names.append((lane.get("name", ""), lane["description"], multiplex["barcode_id"]))
    return len(set(names))

if __name__ == "__main__":
    main(*sys.argv[1:])
