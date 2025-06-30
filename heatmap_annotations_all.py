import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from Bio.Seq import Seq
import numpy as np

# CSV files to compare across days
csv_files = {
    "D1": "/Users/haleyatkins/Desktop/109_pop/collected_outputs/D1_C_pop_mutation_predictions.csv",
    "D5": "/Users/haleyatkins/Desktop/109_pop/collected_outputs/D10_C_pop_mutation_predictions.csv",
    "D10": "/Users/haleyatkins/Desktop/109_pop/collected_outputs/D15_A_pop_mutation_predictions.csv",
    "D20": "/Users/haleyatkins/Desktop/109_pop/collected_outputs/D20_A_pop_mutation_predictions.csv",
    "D15": "/Users/haleyatkins/Desktop/109_pop/collected_outputs/D15_A_pop_mutation_predictions.csv",
    "D25": "/Users/haleyatkins/Desktop/109_pop/collected_outputs/D25_A_pop_mutation_predictions.csv",
    "D30": "/Users/haleyatkins/Desktop/109_pop/collected_outputs/D30_A_pop_mutation_predictions.csv"
    # Add more as needed
}

def is_nonsynonymous(annotation):
    if not isinstance(annotation, str):
        return False
    if '(' in annotation and '→' in annotation:
        try:
            codon_change = annotation.split('(')[1].split(')')[0]
            from_codon, to_codon = codon_change.split('→')
            from_aa = str(Seq(from_codon).translate())
            to_aa = str(Seq(to_codon).translate())
            return from_aa != to_aa
        except:
            return True
    return True

def convert_frequency(frequency):
    if isinstance(frequency, str) and '%' in frequency:
        return float(frequency.replace('%', '').strip())
    return float(frequency)

# Collect CV data for each timepoint
cv_data = {}

for day, path in csv_files.items():
    if not os.path.exists(path):
        print(f"Missing file: {path}")
        continue

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    
    df['frequency'] = df['frequency'].apply(convert_frequency)
    df_filtered = df[df['frequency'] != 100.0]
    df_filtered = df_filtered[df_filtered['annotation'].str.contains('intergenic', case=False, na=False) == False]
    df_filtered = df_filtered[df_filtered['annotation'].apply(is_nonsynonymous)]

    # Group by gene description and calculate CV
    gene_group = df_filtered.groupby('description').agg({
        'frequency': ['mean', 'std']
    }).reset_index()
    
    gene_group.columns = ['description', 'mean_frequency', 'std_dev']
    gene_group['CV'] = (gene_group['std_dev'] / gene_group['mean_frequency']) * 100
    
    # Store in dict
    for _, row in gene_group.iterrows():
        gene = row['description']
        cv = row['CV']
        if gene not in cv_data:
            cv_data[gene] = {}
        cv_data[gene][day] = cv

# Convert to DataFrame
cv_df = pd.DataFrame.from_dict(cv_data, orient='index').sort_index()
cv_df = cv_df.sort_index(axis=1)  # Sort columns (D15, D30, D60...)

cv_df_filled = cv_df.fillna(0)

# Reorder columns manually BEFORE clustering if col_cluster=False
cv_df_filled = cv_df_filled[['D1', 'D5', 'D10', 'D15', 'D20', 'D25', 'D30']]

# Generate clustermap first (without annotations)
g = sns.clustermap(
    cv_df_filled,
    cmap='rocket_r',
    linewidths=0.5,
    cbar_kws={'label': 'CV (%)'},
    figsize=(14, 18),
    col_cluster=False,  # Keep your custom order
    row_cluster=True,
    vmin=0,
    vmax=100
)

# Get reordered data based on dendrograms
reordered_data = cv_df_filled.iloc[g.dendrogram_row.reordered_ind, :]

# Make annotation matrix match the reordered data
high_cv_threshold = 80
annot_data = reordered_data.round(1).astype(str)
annot_data[reordered_data > high_cv_threshold] = annot_data[reordered_data > high_cv_threshold] + " *"

# Redraw the clustermap with correctly aligned annotations
plt.close()  # Close previous incorrect plot
g = sns.clustermap(
    reordered_data,
    cmap='rocket_r',
    annot=annot_data.values,
    fmt='',
    linewidths=0.5,
    cbar_kws={'label': 'CV (%)'},
    figsize=(14, 18),
    col_cluster=False,
    row_cluster=True,
    vmin=0,
    vmax=100
)

# Labeling
plt.suptitle("Clustered Heatmap of Gene Mutation CV Across Days Host A E. coli C", y=1.05, fontsize=16)
g.ax_heatmap.set_xlabel("Day")
g.ax_heatmap.set_ylabel("Gene Description")

# Save and show
plt.savefig('/Users/haleyatkins/Desktop/109_pop/heatmaps/gene_mutation_cv_clustered_heatmap_A_1162.png', dpi=300, bbox_inches='tight')
plt.show()
