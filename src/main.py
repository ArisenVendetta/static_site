from textnode import TextNode, TextType
from nodehelper import markdown_to_html_node
import pprint
import os
import shutil

FILE_LIST = {

}

def copy_files_from_source_to_destination(source_directory: str, destination_directory: str) -> None:
    # print(f'DBG_src: {os.path.abspath(source_directory)}')
    # print(f'DBG_dst: {os.path.abspath(destination_directory)}')
    if not os.path.exists(source_directory):
        raise FileNotFoundError("source directory doesn't exist")
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory, exist_ok=True)
    else:
        print(f'attempting to purge existing destination directory: {os.path.abspath(destination_directory)}')
        shutil.rmtree(destination_directory, ignore_errors=True)
        if os.path.exists(destination_directory):
            raise Exception('unable to delete/clear destination directory, manually clear it and re-run script')
        os.makedirs(destination_directory)
        print('destination directory purge successful')

    existing_directories = os.listdir(source_directory)
    for found in existing_directories:
        path = os.path.join(source_directory, found)
        dest = os.path.join(destination_directory, found)
        if os.path.isdir(path):
            copy_files_from_source_to_destination(path, dest)
        else:
            print(f"moving '{path}' -> '{dest}'")
            shutil.copy2(path, dest)

def main():
    copy_files_from_source_to_destination('static/', 'public/')


main()