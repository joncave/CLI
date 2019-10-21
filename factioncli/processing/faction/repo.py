import os
import requests
import zipfile
import tempfile
import shutil
from pathlib import Path
import subprocess

from factioncli.processing.cli import log
from factioncli.processing.cli.printing import print_output


def clone_github_repo(branch, repo_name, output_dir):
    print_output("Cloning {0} to {1}".format(repo_name, output_dir))
    command = "git clone --single-branch --branch {0} https://github.com/{1} {2}".format(branch, repo_name, output_dir)
    subprocess.call(command, shell=True)


def download_github_repo(repo_name, output_dir, alone_dir, access_token=None):
    print_output("Downloading module: {0}".format(repo_name))
    log.debug("Access Token: {0}".format(access_token))
    url = "https://api.github.com/repos/{0}/zipball".format(repo_name)
    temporary_zip = tempfile.NamedTemporaryFile(suffix=".zip")
    log.debug("Temporary File: {0}".format(temporary_zip.name))
    if access_token:
        log.debug("Adding Github PAT Header")
        headers = {'Authorization': 'token {0}'.format(access_token)}
        log.debug("Downloading Zip")
        r = requests.get(url, headers=headers, allow_redirects=True)
    else:
        print_output("Downloading Zip")
        r = requests.get(url, allow_redirects=True)

    log.debug("Writing Zip")
    print_output("Writing Zip File {0}".format(temporary_zip.name))
    temporary_zip.write(r.content)

    log.debug("Opening Zip")
    print_output("Opening Zip File {0}".format(temporary_zip.name))
    zip_ref = zipfile.ZipFile(temporary_zip.name, 'r')

    temporary_dir = tempfile.mkdtemp()
    log.debug("Creating Temporary Dir: {0}".format(temporary_dir))
    print_output("Creating Temporary Dir: {0}".format(temporary_dir))

    log.debug("Extracting Zip")
    print_output("Extracting Zip File {0}".format(temporary_zip.name))
    zip_ref.extractall(temporary_dir)

    log.debug("Buildling source folder")

    repo_path = repo_name.replace('/', '-')
    source_path = os.path.join(temporary_dir, "{0}-{1}".format(repo_path, zip_ref.comment.decode()))

    log.debug("Checking for source path: {0}".format(source_path))
    print_output("Checking for source path: {0}".format(source_path))
    if not os.path.exists(source_path):
        source_path = temporary_dir

    log.debug("Source Path: {0}".format(source_path))
    log.debug("Creating output directory: {0}".format(output_dir))

    print_output("Source Path: {0}".format(source_path))
    print_output("Creating output directory: {0}".format(output_dir))

    path = Path(output_dir)
    if path.exists():
        log.debug("Cleaning out {0}".format(output_dir))
        print_output("Cleaning out {0}".format(output_dir))
        shutil.rmtree(output_dir, ignore_errors=True)

    # path.mkdir(parents=True, exist_ok=True)

    module_files = os.listdir(source_path)
    print_output("Moving files to {0}".format(output_dir))
    for module_file in module_files:
        module_file_path = os.path.join(source_path, module_file)
        log.debug("Moving {0}".format(module_file_path))
        print_output("Moving {0}".format(module_file_path))
        shutil.move(module_file_path, output_dir)

    zip_ref.close()
    temporary_zip.close()
    shutil.rmtree(temporary_dir, ignore_errors=True)
