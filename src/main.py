import os
import shutil
from pathlib import Path

from markdown_blocks import extract_title, markdown_to_html_node

target = "./public"
source = "./static"


def main():
    if os.path.exists(target):
        shutil.rmtree(target)
        print(f"DELETING: {target}")
    os.mkdir(target)
    print(f"COPYING: {source} -> {target} ...")
    copy_files(target, source)

    print("Generating content...")
    generate_pages_recursive("./content", "./template.html", "./public")


def copy_files(tar_dir, cur_dir):
    for file in os.listdir(cur_dir):
        cur_path = os.path.join(cur_dir, file)
        tar_path = os.path.join(tar_dir, file)
        print(f"  * {cur_path} -> {tar_path}")
        if os.path.isfile(cur_path):
            shutil.copy(cur_path, tar_path)
        else:
            os.mkdir(tar_path)
            copy_files(tar_path, cur_path)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for file in os.listdir(dir_path_content):
        cur_path = os.path.join(dir_path_content, file)
        tar_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(cur_path):
            file_path = Path(tar_path).with_suffix(".html")
            generate_page(cur_path, template_path, file_path)
        else:
            generate_pages_recursive(cur_path, template_path, tar_path)


def generate_page(from_path: str, template_path: str, dest_path: str | Path) -> None:
    if not os.path.isfile(from_path):
        return f'Error: File not found or is not a regular file: "{from_path}"'

    print(f"  * {from_path} {template_path} -> {dest_path}")

    with open(from_path) as file:
        content = file.read()
    with open(template_path) as file:
        template = file.read()
    html_string = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    html_page = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_string
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(html_page)


main()
