from flask import send_file


def download_file(file_path):
    file = send_file(file_path, as_attachment=True)
    return file