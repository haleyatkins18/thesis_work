#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 08:20:52 2025

@author: haleyatkins
"""

import os
import subprocess

# Define list of directories and reference genome files to process
directories = [
    "/media/catherine/ExtraDrive1/Haley/mapped_output_109_pro_147",
    "/media/catherine/ExtraDrive1/Haley/mapped_output_1162_9W",
    "/media/catherine/ExtraDrive1/Haley/mapped_output_1362_vB"
]

references = [
    "/media/catherine/ExtraDrive1/Haley/109_pro147.gb",
    "/media/catherine/ExtraDrive1/Haley/vB_1362.gb",
    "/media/catherine/ExtraDrive1/Haley/9W_1162.gb"
]

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

def run_breseq(sample, r1, r2, reference, output_directory):
    """Runs breseq for a sample against the reference genome."""
    subprocess.run(["breseq", "-r", reference, "-o", output_directory, r1, r2], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 

# Main execution
if __name__ == "__main__":
    # Define the base output directory where results will be grouped by reference genome
    base_output_directory = "breseq_results_by_reference"
    os.makedirs(base_output_directory, exist_ok=True)

    # Loop through each directory-reference pair
    for directory, reference in zip(directories, references):
        # Extract the reference name (without extension) to use as the reference group
        reference_name = os.path.basename(reference).split('.')[0]

        # Create a subdirectory for each reference under the base output directory
        reference_output_directory = os.path.join(base_output_directory, reference_name)
        os.makedirs(reference_output_directory, exist_ok=True)

        # Create a subdirectory for each directory under the corresponding reference subdirectory
        directory_output_base = os.path.join(reference_output_directory, os.path.basename(directory))
        os.makedirs(directory_output_base, exist_ok=True)

        print("Processing directory: " + directory + " with reference: " + reference)
        
        # Process each paired read file for the current directory and reference genome
        for sample, r1, r2 in find_paired_reads(directory):
            # Create a unique output directory for each sample under the directory-reference subdirectory
            sample_output_directory = os.path.join(directory_output_base, sample)
            os.makedirs(sample_output_directory, exist_ok=True)
            
            # Run breseq for each sample
            run_breseq(sample, r1, r2, reference, sample_output_directory)
        
        print("All samples processed for directory: " + directory + " with reference: " + reference)
        
    print("All directories processed!")