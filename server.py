import os
from datetime import datetime

from fastapi import FastAPI, File, UploadFile

from util import (convert_pdb_to_mol2, extract_pdb_file_from_gz_file,
                  get_generated_files_from_project_id,
                  get_pdb_file_from_project_id,
                  start_automodel_from_fasta_file)

app = FastAPI()

@app.get("/")
def read_root():
    return {"ok": True}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # save file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"

    with open("tmp/" + filename, "wb") as buffer:
        buffer.write(file.file.read())

    f = open("tmp/" + filename, "r").read()

    project_id = start_automodel_from_fasta_file(f)

    # Fetch the bulk download of results from the parameter "download_url"
    print("Fetch the results from: ", get_generated_files_from_project_id(project_id))

    # Download the files
    get_pdb_file_from_project_id(project_id)

    # extract the pdb file from the gz file
    extract_pdb_file_from_gz_file("tmp/01.pdb.gz")

    # convert the pdb file to a mol2 file
    convert_pdb_to_mol2()

    os.remove("tmp/" + filename)

    return {"message": "File successfully converted to mol2"}
