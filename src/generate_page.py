from markdown_to_blocks import markdown_to_blocks
from block_types import (
    block_to_block_type,
    BLOCK_TYPE_HEADING)
from block_to_html import block_to_html, markdown_to_html_node


def extract_title(markdown):
    # print(f"extracting title from markdown: {markdown}")
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            heading_block = block.split(" ")
            return " ".join(heading_block[1:])


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}")
    md_content = ""
    template_content = ""
    with open(from_path, "r", encoding="utf-8") as markdown, open(template_path, "r", encoding="utf-8")as html_template:
        md_content = markdown.read()
        template_content = html_template.read()
        markdown.close()
        html_template.close()

    my_header = extract_title(md_content)
    template_title = template_content.replace("{{ Title }}", my_header)
    markdown_to_html = markdown_to_html_node(md_content)
    final_template = template_title.replace(
        "{{ Content }}", markdown_to_html.to_html())

    with open(dest_path, "w+", encoding="utf-8") as final_html:
        final_html.write(final_template)
        final_html.close()
