import os
from pathlib import Path
from block_markdown import markdown_to_block
from markdown_to_html import markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

def extract_title(markdown: str):
    mds = markdown_to_block(markdown)
    if not mds[0].startswith("# "):
        raise ValueError("Markdown has no header")
    return mds[0][2:]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"{from_path} does not exist")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file {template_path} does not exist")

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(from_path, "r") as f:
        content = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    node = markdown_to_html_node(content)
    html = node.to_html()

    title = extract_title(content)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    with open(dest_path, "w") as f:
        f.write(template)

    
