"""Module representing TextNodes"""

import re
from htmlnode import LeafNode

TEXT_TYPE_TEXT = "text"
TEXT_TYPE_BOLD = "bold"
TEXT_TYPE_ITALIC = "italic"
TEXT_TYPE_CODE = "code"
TEXT_TYPE_LINK = "link"
TEXT_TYPE_IMAGE = "image"


class TextNode:
    """Class representing TextNode"""

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text == TEXT_TYPE_TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text == TEXT_TYPE_BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text == TEXT_TYPE_ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text == TEXT_TYPE_CODE:
        return LeafNode("code", text_node.text)
    if text_node.text == TEXT_TYPE_LINK:
        return LeafNode("a", text_node.text, text_node.url)
    if text_node.text == TEXT_TYPE_IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Not a valid text type: {text_node.text}")


def split_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    for node in old_nodes:
        if node.text_type != TEXT_TYPE_TEXT:
            new_node_list.append(node)
            continue
        text_list = node.text.split(delimiter)
        if len(text_list) % 2 == 0:
            raise ValueError("Invalid Markdown Syntax")
        for idx, text in enumerate(text_list):
            if text == "":
                continue
            if idx % 2 == 0:
                new_node = TextNode(text, TEXT_TYPE_TEXT)
            else:
                new_node = TextNode(text, text_type)
            new_node_list.append(new_node)
    return new_node_list


def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images


def extract_markdown_links(text):
    links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return links


def split_nodes_image(nodes):
    split_images = extract_markdown_images(nodes[0].text)
    if len(split_images) == 0:
        return nodes
    if len(nodes) > 1:
        new_nodes_list = nodes[1:]
    current_nodes_list = nodes[0].text.split(
        f"![{split_images[0][0]}]({split_images[0][1]})", 1
    )
    if len(current_nodes_list) > 1 and current_nodes_list[1] != "":
        new_nodes_list = [TextNode(current_nodes_list[1], TEXT_TYPE_TEXT)]
    new_nodes_list.extend(
        [
            TextNode(current_nodes_list[0], TEXT_TYPE_TEXT),
            TextNode(split_images[0][0], TEXT_TYPE_IMAGE, split_images[0][1]),
        ]
    )
    return split_nodes_image(new_nodes_list)


def split_nodes_links(nodes):
    split_links = extract_markdown_links(nodes[0].text)
    if len(split_links) == 0:
        return nodes
    if len(nodes) > 1:
        new_nodes_list = nodes[1:]
    current_nodes_list = nodes[0].text.split(
        f"[{split_links[0][0]}]({split_links[0][1]})", 1
    )
    if len(current_nodes_list) > 1 and current_nodes_list[1] != "":
        new_nodes_list = [TextNode(current_nodes_list[1], TEXT_TYPE_TEXT)]
    new_nodes_list.extend(
        [
            TextNode(current_nodes_list[0], TEXT_TYPE_TEXT),
            TextNode(split_links[0][0], TEXT_TYPE_LINK, split_links[0][1]),
        ]
    )
    return split_nodes_links(new_nodes_list)
