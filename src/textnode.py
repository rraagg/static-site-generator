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
    if text_node.text_type == TEXT_TYPE_TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TEXT_TYPE_BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TEXT_TYPE_ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TEXT_TYPE_CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TEXT_TYPE_LINK:
        return LeafNode("a", text_node.text, text_node.url)
    if text_node.text_type == TEXT_TYPE_IMAGE:
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


def split_nodes_images(nodes):
    new_nodes_list = []
    for node in nodes:
        if node.text_type != TEXT_TYPE_TEXT:
            new_nodes_list.append(node)
            continue
        current_text = node.text
        split_images = extract_markdown_images(current_text)
        if len(split_images) == 0:
            new_nodes_list.append(node)
            continue
        for image in split_images:
            current_text_list = current_text.split(
                f"![{image[0]}]({image[1]})", 1)
            if len(current_text_list) != 2:
                raise ValueError("Invalid image")
            if current_text_list[0] != "":
                new_nodes_list.append(
                    TextNode(current_text_list[0], TEXT_TYPE_TEXT))
            new_nodes_list.append(
                TextNode(image[0], TEXT_TYPE_IMAGE, image[1]))
            current_text = current_text_list[1]
        if current_text != "":
            new_nodes_list.append(TextNode(current_text, TEXT_TYPE_TEXT))
    return new_nodes_list


def split_nodes_links(nodes):
    new_nodes_list = []
    for node in nodes:
        if node.text_type != TEXT_TYPE_TEXT:
            new_nodes_list.append(node)
            continue
        current_text = node.text
        split_links = extract_markdown_links(current_text)
        if len(split_links) == 0:
            new_nodes_list.append(node)
            continue
        for link in split_links:
            current_text_list = current_text.split(
                f"[{link[0]}]({link[1]})", 1)
            if len(current_text_list) != 2:
                raise ValueError("Invalid Link")
            if current_text_list[0] != "":
                new_nodes_list.append(
                    TextNode(current_text_list[0], TEXT_TYPE_TEXT))
            new_nodes_list.append(TextNode(link[0], TEXT_TYPE_LINK, link[1]))
            current_text = current_text_list[1]
        if current_text != "":
            new_nodes_list.append(TextNode(current_text, TEXT_TYPE_TEXT))
    return new_nodes_list


def text_to_textnodes(text):
    textnodes = []
    node = TextNode(text, TEXT_TYPE_TEXT)
    original_node_list = [node]
    textnodes = split_delimiter(original_node_list, "**", TEXT_TYPE_BOLD)
    textnodes = split_delimiter(textnodes, "*", TEXT_TYPE_ITALIC)
    textnodes = split_delimiter(textnodes, "`", TEXT_TYPE_CODE)
    textnodes = split_nodes_images(textnodes)
    textnodes = split_nodes_links(textnodes)
    return textnodes
