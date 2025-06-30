import os
import sys
from Bio import SeqIO

#function to translate nucleotide seqs to aa seqs
def translate_fasta(input_fasta, output_fasta):
    #parse each sequence record in the input FASTA file
    for record in SeqIO.parse(input_fasta, "fasta"):
        #translate the nucleotide sequence into a protein sequence
        protein_sequence = record.seq.translate()
        
        #write the translated protein sequence to the output FASTA file
        with open(output_fasta, "w") as out_file:
            out_file.write(">" + record.id + "\n")              
            out_file.write(str(protein_sequence) + "\n")        
        
        #confirm translation
        print("Translated " + input_fasta + " and saved to " + output_fasta + ".")


#FASTA file as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python translate_fasta.py input_file.fasta")
    sys.exit(1)

input_fasta = sys.argv[1]

#create the output filename  with '.aa.fasta'
output_fasta = input_fasta.replace(".fasta", ".aa.fasta")

#run the translation function
translate_fasta(input_fasta, output_fasta)
