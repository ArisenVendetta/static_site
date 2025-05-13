import os
import sys
import shutil
from pathlib import Path
from nodehelper import markdown_to_html_node

SITE_PATH = sys.argv[1] if len(sys.argv) > 1 else '/'

def copy_files_from_source_to_destination(source_directory: str, destination_directory: str) -> None:
    if not os.path.exists(source_directory):
        raise FileNotFoundError(f"source_directory doesn't exist: {source_directory}")
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


def extract_title(markdown: str) -> str:
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return line.lstrip('#').strip()
    raise Exception('no header found in provided markdown')


def generate_page(from_path: str, template_path: str, destination_path: str, delete_dest_if_exists: bool = False) -> None:
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"from_path doesn't exist: {from_path}")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"template_path doesn't exist: {template_path}")
    if os.path.exists(destination_path):
        if not delete_dest_if_exists:
            raise FileNotFoundError(f"destination_path doesn't exist: {destination_path}")
        os.remove(destination_path)
    dest_path = Path(destination_path)
    if not os.path.exists(dest_path.parent):
        print(f'Creating directory: {dest_path.parent}')
        dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("Attempting to generate new page:")
    print(f"\tfrom:\t\t{os.path.abspath(from_path)}")
    print(f"\ttemplate:\t{os.path.abspath(template_path)}")
    print(f"\tdest:\t\t{os.path.abspath(destination_path)}")

    source_content = open_and_read_content(from_path)
    template_content = open_and_read_content(template_path)
    title = extract_title(source_content)
    page_content = markdown_to_html_node(source_content).to_html()
    updated_content = template_content.replace('{{ Title }}', title).replace('{{ Content }}', page_content)
    updated_content = updated_content.replace('href="/', f'href="{SITE_PATH}').replace('src="/', f'src="{SITE_PATH}')
    with open(destination_path, 'w+') as output:
        output.write(updated_content)

def generate_pages_recursive(from_path: str, template_path: str, destination_path: str) -> None:
    source_path = Path(from_path)
    content_files = os.listdir(source_path.absolute())
    for content_file in content_files:
        content_path = Path(os.path.join(from_path, content_file))
        if os.path.isdir(content_path.absolute()):
            generate_pages_recursive(content_path, template_path, os.path.join(destination_path, content_file))
        else:
            template_path = Path(template_path)
            output_path = Path(os.path.join(destination_path, f'{content_path.stem}.html'))
            if os.path.isdir(content_path.absolute()):
                continue
            generate_page(content_path.absolute(), template_path.absolute(), output_path.absolute())
    
def open_and_read_content(source_file: str) -> str:
    if not os.path.exists(source_file):
        raise FileNotFoundError(f"source_file doesn't exist: {source_file}")
    
    content = ''
    with open(source_file, mode='rt', newline='\n') as md:
        content = md.read()
    if len(content) < 1:
        raise Exception(f'from_path is empty, unable to generate page: {source_file}')
    return content


def main():
    copy_files_from_source_to_destination('static/', 'docs/')
    generate_pages_recursive('content/', 'template.html', 'docs/')


if __name__ == '__main__':
    main()