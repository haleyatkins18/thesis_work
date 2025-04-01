#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 20:08:37 2025

@author: haleyatkins
"""

import os
import subprocess

# Define input directory containing FASTQ files
directory = "/media/catherine/ExtraDrive1/Haley/mapped_output_109_pro_147"

# Define reference genome file path
reference = "/media/catherine/ExtraDrive1/Haley/109_pro147.gb"

# Output base directory
output_base = "breseq_results"
os.makedirs(output_base, exist_ok=True)

def find_paired_reads(directory):
    """Finds and returns paired-end FASTQ file paths."""
    # List of fastq files matching _mapped_1*.fq.gz and _mapped_2*.fq.gz
    fastq_files = sorted([f for f in os.listdir(directory) if f.endswith("_mapped_1*.fq.gz") or f.endswith("_mapped_2*.fq.gz")])
    paired_reads = []

    # Use a set to store already processed sample names
    processed_samples = set()

    for r1 in fastq_files:
        # r1 will end with _mapped_1*.fq.gz
        r1_path = os.path.join(directory, r1)
        
        # Get the base sample name by removing the part that corresponds to '_mapped_1*.fq.gz'
        sample_name = r1.split('_mapped_')[0]
        
        if sample_name in processed_samples:
            continue  # Skip if already processed
        
        # Generate the corresponding r2 file path
        r2 = r1.replace("_mapped_1", "_mapped_2")
        r2_path = os.path.join(directory, r2)

        # Check if both r1 and r2 exist
        if os.path.exists(r2_path):
            paired_reads.append((sample_name, r1_path, r2_path))
            processed_samples.add(sample_name)  # Mark the sample as processed
       

    return paired_reads

def run_breseq(sample, r1, r2, reference):
    """Runs breseq for a sample against the reference genome."""
    # Directly run breseq without creating an output directory or printing a message
    subprocess.run(["breseq", "-r", reference, "-o", sample, r1, r2], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 

# Main execution
if __name__ == "__main__":
    print("Processing directory: " + directory)
    for sample, r1, r2 in find_paired_reads(directory):
        run_breseq(sample, r1, r2, reference)
    print("All samples processed!")