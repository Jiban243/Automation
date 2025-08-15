import os
import pandas as pd
from ip3 import automate_data_loader
from ip10 import run_gnps_workflow
from ip11 import automate_data_deletion

tsv_folder = 'org'
tsv_file_paths = sorted([
    os.path.join(tsv_folder, file)
    for file in os.listdir(tsv_folder)
    if file.endswith('.tsv')
])

print(f"Found {len(tsv_file_paths)} TSV files in '{tsv_folder}' folder.")
print(tsv_file_paths)
mzxml_file = "mzxml_file_paths.txt"

USERNAME = "alkesh"      
PASSWORD = "jkqr459svn"  

for file in tsv_file_paths:
    df = pd.read_csv(file, sep='\t')

    if 'filename' not in df.columns:
        print(f"'filename' column missing in {file}")
        continue

    massive_ids = df['filename'].str.split('/').str[0].unique()
    data = df['filename'].str.split('/').str[1]

    with open(mzxml_file, "w") as f:
        for item in data:
            f.write(f"{item}\n")

    automate_data_loader(massive_ids=massive_ids, USERNAME=USERNAME, PASSWORD=PASSWORD)

    job_name = os.path.splitext(os.path.basename(file))[0]
    # print(job_name)
    # print(file)
    # exit()
    run_gnps_workflow(username=USERNAME, password=PASSWORD, tsv_filename=job_name+".tsv", job_title=job_name)

    automate_data_deletion(USERNAME=USERNAME, PASSWORD=PASSWORD)
