import logging
from webdav3.client import Client
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    logging.basicConfig(
        filename="photo_classifier.log", encoding="utf-8", level=logging.INFO
    )
    options = {
        "webdav_hostname": os.getenv("NEXTCLOUD_DAV_ENDPOINT"),
        "webdav_login": os.getenv("NEXTCLOUD_USERNAME"),
        "webdav_password": os.getenv("NEXTCLOUD_PASSWORD"),
    }
    client = Client(options)
    file_list = client.list(os.getenv("NEXTCLOUD_FOLDER"))
    with NamedTemporaryFile("w") as temp_file:
        client.download_sync(
            remote_path="Notes/file_mapping.md",
            local_path=temp_file.name,
        )

        with open(temp_file.name) as f:
            data = [x.strip().split(" -> ") for x in f.read().split("\n")]
        
    for row in data:
        selected_files = [x for x in file_list if row[0] in x]

        for f in selected_files:
            try:
                client.move(remote_path_from=f"{os.getenv('NEXTCLOUD_FOLDER')}{f}", remote_path_to=f"/Fotos/Top/{row[1]}/{f}", overwrite=True)
            except Exception as e:
                logging.error(e)
                continue

if __name__ == "__main__":
    main()
