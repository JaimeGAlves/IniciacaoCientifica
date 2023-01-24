import time
import sys
import requests
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


token = "YOUR_TOKEN_HERE"


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


if __name__ == "__main__":
    
    fasta_file = filedialog.askopenfilename(initialdir = "desktop", title = "Select fasta file", filetypes = (("fasta files", "*.fasta"), ("all files", "*.*")))

    f = open(fasta_file, "r").read()

    project_id = start_automodel_from_fasta_file(f)

    # Fetch the bulk download of results from the parameter "download_url"
    print("Fetch the results from: ", get_generated_files_from_project_id(project_id))