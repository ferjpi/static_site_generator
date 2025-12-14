from os import mkdir, path
import shutil
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


def move_content(source, destination):
    source_path = path.abspath(source)
    destination_path = path.abspath(destination)

    print(f"Moving {source_path} to {destination_path}")
    if not path.exists(source_path) and not path.isdir(source_path):
        logging.error(f"Source path {source_path} does not exist")
        sys.exit(1)

    if path.exists(destination_path) and path.isdir(destination_path):
        logging.info(f"Removing {destination_path}")
        shutil.rmtree(destination_path)

    logging.info(f"Creating {destination_path}")
    mkdir(destination_path)

    logging.info(f"Copying {source_path} to {destination_path}")
    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
