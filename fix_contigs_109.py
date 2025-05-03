#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 10:27:04 2025

@author: haleyatkins
"""

def merge_fasta_to_one_contig(input_fasta, output_fasta, new_header="merged_contig_109"):
    sequence = ""

    with open(input_fasta, "r") as infile:
        for line in infile:
            if line.startswith(">"):
                continue  
            sequence += line.strip()
    with open(output_fasta, "w") as outfile:
        outfile.write(">" + new_header + "\n")
        
        for i in range(0, len(sequence), 60):
            outfile.write(sequence[i:i+60] + "\n")

merge_fasta_to_one_contig("/Users/haleyatkins/Desktop/109_assemble_contigs.fasta", "/Users/haleyatkins/Desktop/109_merge_contigs.fasta")