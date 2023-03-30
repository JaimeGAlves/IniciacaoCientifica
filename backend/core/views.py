from django.shortcuts import render

import gzip
import os
import shutil
import sys
import time
import requests

token = "775f34af6f76fc32a515ca859f208ba3205ad088"


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
        headers={"Authorization": f"Token {token}"},
        json={
            "target_sequences": sequence,
            "project_title": header
        })

    if response.status_code not in [200, 202]:
        print(response.text)
        sys.exit()

    project_id = response.json()["project_id"]

    return project_id

def start_automodel(request):
    if request.method == 'POST' and request.FILES['fasta_file']:
        fasta_file = request.FILES['fasta_file']
        content = fasta_file.read()
        project_id = start_automodel_from_fasta_file(content)

        # redirecionar para página de resultados
        return redirect('result', project_id=project_id)

    # Se a solicitação não foi POST, exibir o formulário de carregamento
    return render(request, 'core/home.html')


def get_generated_files_from_project_id(project_id):
    while True:
        # Update the status from the server
        response = requests.get(
            f"https://swissmodel.expasy.org/project/{project_id}/models/summary/",
            headers={"Authorization": f"Token {token}"})

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
        with open(file_name, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)

        print("Finished downloading", file_name)


def extract_pdb_file_from_gz_file():
    with gzip.open('01.pdb.gz', 'rb') as f_in:
        with open('model.pdb', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print("Finished extracting the pdb file")


def convert_pdb_to_mol2():
    os.system("obabel -ipdb model.pdb -omol2 -O model.mol2")
    print("Finished converting the pdb file to a mol2 file")


if __name__ == "__main__":
    
    fasta_file = filedialog.askopenfilename(initialdir = "desktop", title = "Select fasta file", filetypes = (("fasta files", "*.fasta"), ("all files", "*.*")))

    f = open(fasta_file, "r").read()

    project_id = start_automodel_from_fasta_file(f)

    # Fetch the bulk download of results from the parameter "download_url"
    # print("Fetch the results from: ", get_generated_files_from_project_id(project_id))

    # Download the files
    get_pdb_file_from_project_id(project_id)

    # extract the pdb file from the gz file
    extract_pdb_file_from_gz_file()

    # convert the pdb file to a mol2 file
    convert_pdb_to_mol2()
# Create your views here.
def home(request):
    context = {
    }
    return render(request, 'core/home.html', context)