import os
import logging
from htmlnode import extract_title, markdown_to_html_node

logging.basicConfig(level=logging.DEBUG)


def generate_page(base_path: str, from_path: str, template_path: str, dest_path: str):
    logging.info(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )

    markdown_source = open(from_path, "r").read()
    template = open(template_path, "r").read()
    content = markdown_to_html_node(markdown_source).to_html()
    title = extract_title(markdown_source)

    logging.info(f"title: {title}")

    template = template.replace("{{ Content }}", content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("href='/", f"href='{base_path}/")
    template = template.replace("src='/", f"src='{base_path}/")

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    open(dest_path, "w").write(template)


def generate_pages_recursive(
    base_path: str, dir_path_content: str, template_path: str, dest_dir_path: str
):
    # crawl every entry in the content directory
    # for earch markdown file found, generate a new html file. It should be written in the
    # same directory structure
    print(f"dir_path_content: {dir_path_content}")
    print(f"dest_dir_path: {dest_dir_path}")

    # validate that dir_path_content is a directory and exists
    if not os.path.isdir(dir_path_content):
        raise Exception(f"dir_path_content is not a directory: {dir_path_content}")

    list_of_files = os.listdir(dir_path_content)
    print(f"list_of_files: {list_of_files}")
    for f in list_of_files:
        abs_path = os.path.join(dir_path_content, f)
        if os.path.isdir(abs_path):
            print(f"dir: {f}")
            generate_pages_recursive(
                base_path,
                abs_path,
                template_path,
                os.path.join(dest_dir_path, f),
            )
        else:
            print(f"file: {abs_path}")
            print(f"f of file: {f}")
            rename_ext = f.replace("md", "html")
            generate_page(
                base_path,
                abs_path,
                template_path,
                os.path.join(dest_dir_path, rename_ext),
            )
