import gzip
import os
import shutil
import sys
import time
from datetime import datetime

import requests

from config import swissmodel_token


def start_automodel_from_fasta_file(fasta_file):
    fasta_file = fasta_file.split("\n")

    header = fasta_file[0]

    sequence = ""

    for i in range(1, len(fasta_file)):
        sequence += fasta_file[i]

    if len(sequence) < 30:
        print("Error: The target sequence must be longer than 30 residues.")
        sys.exit()

    response = requests.post(
        "https://swissmodel.expasy.org/automodel",
        headers={"Authorization": f"Token {swissmodel_token}"},
        json={
            "target_sequences": sequence,
            "project_title": header
        })

    if response.status_code not in [200, 202]:
        print(response.text)
        sys.exit()

    project_id = response.json()["project_id"]

    return {"project_id": project_id, "project_name": header}


def get_generated_files_from_project_id(project_id):
    while True:
        # Update the status from the server
        response = requests.get(
            f"https://swissmodel.expasy.org/project/{project_id}/models/summary/",
            headers={"Authorization": f"Token {swissmodel_token}"})

        # Update the status
        status = response.json()["status"]

        print('Job status is now', status)

        if status in ["COMPLETED", "FAILED"]:
            break

        time.sleep(10)

    files_url = []

    response_object = response.json()
    if response_object['status'] == 'COMPLETED':
        for model in response_object['models']:
            files_url.append(model['coordinates_url'])

    return files_url


def get_pdb_file_from_project_id(project_id):
    # Download the files
    for file_url in get_generated_files_from_project_id(project_id):
        file_name = file_url.split("/")[-1]
        print("Downloading", file_name)

        response = requests.get(file_url, stream=True)
        with open("tmp/" + file_name, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)

        return file_name


def extract_pdb_file_from_gz_file(file):
    with gzip.open(file, 'rb') as f_in:
        with open('tmp/model.pdb', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print("Finished extracting the pdb file")

    # remove the gz file
    os.remove("tmp/01.pdb.gz")


def convert_pdb_to_mol2():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    os.system(f"obabel -ipdb tmp/model.pdb -omol2 -O files/{timestamp}_model.mol2")
    print("Finished converting the pdb file to a mol2 file")
    os.remove("tmp/model.pdb")
    
    return f"{timestamp}_model.mol2"


def convert_pdb_to_mol2_with_pybel():
    from pybel import readfile

    for mol in readfile("pdb", "model.pdb"):
        mol.write("mol2", "model.mol2", overwrite=True)

    print("Finished converting the pdb file to a mol2 file")


# if __name__ == "__main__":
    
#     fasta_file = filedialog.askopenfilename(initialdir = "desktop", title = "Select fasta file", filetypes = (("fasta files", "*.fasta"), ("all files", "*.*")))

#     f = open(fasta_file, "r").read()

#     project_id = start_automodel_from_fasta_file(f)

#     # Fetch the bulk download of results from the parameter "download_url"
#     # print("Fetch the results from: ", get_generated_files_from_project_id(project_id))

#     # Download the files
#     get_pdb_file_from_project_id(project_id)

#     # extract the pdb file from the gz file
#     extract_pdb_file_from_gz_file()

#     # convert the pdb file to a mol2 file
#     convert_pdb_to_mol2()


def upload_file_to_dropbox(filename):
    print("Uploading the file to dropbox")
    import dropbox
    ACCESS_TOKEN = "sl.BkskrTx1yK6EOxsddr70C0TEJ_e9tr3THUTi2cJwpxoYIZxYOLovLQApBvDqwCOUwgJf5utzpmq_2PFYm7s3pT31HHg8uVmOMrnreABH1JqG848mQW6ZPum5nwyCKCRG59VYuxjeYm8LJ9KmvKD25Vs"
    APP_KEY = "sgc2ifib8wc6fm6"
    APP_SECRET = "wmxtkc46z6lytgt"

    try:
        dbx = dropbox.Dropbox(oauth2_access_token=ACCESS_TOKEN, app_key=APP_KEY, app_secret=APP_SECRET)

        with open("files/" + filename, "rb") as f:
            uploaded_file = dbx.files_upload(f.read(), f"/{filename}")

        print("Finished uploading the file to dropbox")
            #return file link
        return dbx.sharing_create_shared_link_with_settings(uploaded_file.path_display).url.replace("dl=0", "dl=1")
    except Exception as e:
        print(e)
        return None
