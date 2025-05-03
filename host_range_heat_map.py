#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 21:32:20 2025

@author: haleyatkins
"""
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


file_path = "/Users/haleyatkins/Desktop/phages_host_range.csv" 
df = pd.read_csv(file_path, index_col=0, dtype=str)  

df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.replace({"no plaque": 0, "plaque": 1, "plaque*": 1.5}, inplace=True)
df = df.apply(pd.to_numeric)

plt.figure(figsize=(12, 10))

ax = sns.heatmap(df, annot=False, cmap="coolwarm", linewidths=0.5, cbar=True)


ax.set_xticks(range(len(df.columns)))
ax.set_xticklabels(df.columns, rotation=90, fontsize=10)  # Rotate for better visibility
ax.set_yticks(range(len(df.index)))
ax.set_yticklabels(df.index, rotation=0, fontsize=10)


cbar = ax.collections[0].colorbar
cbar.set_label("host range")  
cbar.ax.tick_params(labelsize=10)
plt.title("Phages Host Range")
plt.xlabel("Phages")
plt.ylabel("Bacterial Strains")


file_out = 'host_range.png'
plt.savefig(file_out, dpi=300, bbox_inches='tight')
plt.show()
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap, BoundaryNorm

# Load and clean data
file_path = "/Users/haleyatkins/Desktop/phages_host_range.csv" 
df = pd.read_csv(file_path, index_col=0, dtype=str)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.replace({"no plaque": 0, "plaque": 1, "plaque*": 1.5}, inplace=True)
df = df.apply(pd.to_numeric)

# Define discrete colormap
colors = ['lightblue', 'red', 'blue']  # customize as needed
cmap = ListedColormap(colors)
bounds = [0, 0.75, 1.25, 2]  # Bins: 0, ~1, ~1.5
norm = BoundaryNorm(bounds, cmap.N)

# Plot
plt.figure(figsize=(14, 20))
ax = sns.heatmap(df, annot=False, cmap=cmap, norm=norm, linewidths=0.5, cbar=True)

# Ticks/labels
ax.set_xticks(range(len(df.columns)))
ax.set_xticklabels(df.columns, rotation=90, fontsize=10)
ax.set_yticks(range(len(df.index)))
ax.set_yticklabels(df.index, rotation=0, fontsize=10)

# Colorbar with discrete ticks
cbar = ax.collections[0].colorbar
cbar.set_ticks([0.375, 1, 1.75])  # Midpoints of each bin
cbar.set_ticklabels(['No Plaque', 'Plaque', 'Pseudoplaque'])
cbar.ax.tick_params(labelsize=10)
cbar.set_label("Plaque Presence")

# Title and labels
plt.title("Phages Host Range")
plt.xlabel("Phages")
plt.ylabel("Bacterial Strains")

# Save
file_out = 'host_range.png'
plt.savefig(file_out, dpi=300, bbox_inches='tight')
plt.show()