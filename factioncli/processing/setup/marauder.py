import os
import requests
import zipfile
from pathlib import Path
from factioncli.processing.config import get_config


def download_marauder(access_token=None):
    config = get_config()
    marauder_path = os.path.join(config["FACTION_PATH"], "agents\Marauder")
    path = Path(marauder_path)
    path.mkdir(parents=True, exist_ok=True)

    marauder_destination = os.path.join(marauder_path, "Marauder.zip")
    marauder_url = "https://api.github.com/repos/maraudershell/Marauder/zipball"

    if access_token:
        headers = {'Authorization': 'token {0}'.format(access_token)}
        r = requests.get(marauder_url, headers=headers, allow_redirects=True)
    else:
        r = requests.get(marauder_url, allow_redirects=True)
    with open(marauder_destination, 'wb') as f:
        f.write(r.content)

    zip_ref = zipfile.ZipFile(marauder_destination, 'r')
    zip_ref.extractall(marauder_path)