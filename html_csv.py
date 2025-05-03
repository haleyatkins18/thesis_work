#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 10:57:22 2025

@author: haleyatkins
"""

from bs4 import BeautifulSoup
import csv

#need to extract mutation predictions from HTML file and save to CSV
def extract_mutation_predictions_to_csv(html_file, csv_file):
    #open and read the HTML file
    with open(html_file, 'r') as file:
        html_content = file.read()

    #parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    #find table with the header "Predicted mutations"
    mutation_table = None
    tables = soup.find_all('table')
    
    for table in tables:
        header = table.find('th', string="Predicted mutations")
        if header:
            mutation_table = table
            break  #stop once we find the relevant table
    
    if mutation_table is None:
        print("Mutation predictions table not found.")
        return
    
    #extract rows from the table 
    rows = mutation_table.find_all('tr')[1:]  #skip the header row
    
    #open CSV file for writing
    with open(csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        #write the header for the CSV file
        csvwriter.writerow(['evidence', 'position', 'mutation', 'frequency', 'annotation', 'gene', 'description'])
        
        #extract data from each row and write it to the CSV
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 7:  #ensure the row has 7 columns (corresponding to the header)
                data = [col.get_text(strip=True) for col in columns]
                csvwriter.writerow(data)
    
    print(f"Mutation predictions saved to {csv_file}")

#main execution
if __name__ == "__main__":
    html_file = '/Users/haleyatkins/Desktop/109_pop/collected_outputs/D1_C/index.html'
    csv_file = '/Users/haleyatkins/Desktop/109_pop/collected_outputs/D1_C_pop_mutation_predictions.csv'  
    
    #extract mutation predictions and save to CSV
    extract_mutation_predictions_to_csv(html_file, csv_file)