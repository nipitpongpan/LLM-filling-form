import json
from fillpdf import fillpdfs

def read_json_current_form(json_file_current_form):
    with open(json_file_current_form, 'r') as file:
        current_form = json.load(file)

    return current_form

def write_json_and_pdf_form(current_form, json_file_current_form):
    with open(json_file_current_form, 'w') as file:
        json.dump(current_form, file, indent=4)

    fillpdfs.write_fillable_pdf("template/i-765_decrypt (1).pdf", "result/i-765_decrypt (1).pdf", current_form)
