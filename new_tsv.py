import pandas as pd
import os

# Define the species prefix (change this for different species)
species_prefix = "Synechocystis sp."

# Reading the input Excel file
input_file = "microbe_masst_table_metadata.xlsx"
df = pd.read_excel(input_file)

# Filtering for rows where attribute_Taxaname_file contains the species prefix
bacteria_df = df[df['attribute_Taxaname_file'].str.contains(species_prefix, na=False)]

# Creating the new DataFrame with required columns
result_df = pd.DataFrame(columns=['filename', 'Attribute_group'])

# Processing the data according to the rules
result_df['filename'] = bacteria_df['Filename']
result_df['Attribute_group'] = bacteria_df.apply(
    lambda row: 'blank' if row['attribute_Taxa_NCBI'] == '' 
    else 'QC' if row['attribute_Taxa_NCBI'] == 'QC' 
    else row['attribute_Taxaname_file'], 
    axis=1
)

# Saving the output to a TSV file with dynamic filename
output_file = f"{species_prefix.replace(' ', '_')}_specific_metadata.tsv"
result_df.to_csv(output_file, sep='\t', index=False)

print(f"TSV file '{output_file}' has been created successfully.")