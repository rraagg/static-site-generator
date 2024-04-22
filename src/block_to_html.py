from block_types import (
    BLOCK_TYPE_UNORDERED_LIST,
    BLOCK_TYPE_ORDERED_LIST,
    BLOCK_TYPE_QUOTE,
    BLOCK_TYPE_CODE,
    BLOCK_TYPE_PARAGRAPH,
    BLOCK_TYPE_HEADING,
)

from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes
from markdown_to_blocks import markdown_to_blocks
from block_types import block_to_block_type


def block_to_html(block, block_type):
    if block_type == BLOCK_TYPE_PARAGRAPH:
        return paragraph_to_html(block)
    if block_type == BLOCK_TYPE_HEADING:
        return heading_to_html(block)
    if block_type == BLOCK_TYPE_QUOTE:
        return quote_to_html(block)
    if block_type == BLOCK_TYPE_CODE:
        return code_to_html(block)
    if block_type == BLOCK_TYPE_ORDERED_LIST:
        return ordered_list_to_html(block)
    if block_type == BLOCK_TYPE_UNORDERED_LIST:
        return unordered_list_to_html(block)


def paragraph_to_html(block):
    nodes_list = text_to_textnodes(block)
    html_nodes = []
    for node in nodes_list:
        html_nodes.append(text_node_to_html_node(node))
    return ParentNode("p", html_nodes)


def heading_to_html(block):
    nodes_list = block.split(" ")
    heading_size = len(nodes_list[0])
    html_nodes = []
    text_nodes = text_to_textnodes(" ".join(nodes_list[1:]))
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return ParentNode(f"h{heading_size}", html_nodes)

def quote_to_html(block):
    nodes_list = block.split("\n")
    quote_text_list = []
    for idx, current_node in enumerate(nodes_list):
        if current_node == "":
            continue
        quote_list = current_node.split(">")
        if idx == len(nodes_list) - 1:
            quote_text_list.append(quote_list[1].strip())
        else:
            quote_text_list.append(quote_list[1].strip() + "\n")
    return LeafNode("blockquote", "".join(quote_text_list))


def code_to_html(block):
    nodes_list = block.split("```")
    return ParentNode("pre", [LeafNode("code", nodes_list[1].strip())])


def ordered_list_to_html(block):
    nodes_list = block.split("\n")
    list_items_list = []
    for current_node in nodes_list:
        item_text_list = current_node.split(" ")
        html_nodes = []
        text_nodes = text_to_textnodes(" ".join(item_text_list[1:]))
        for node in text_nodes:
            html_nodes.append(text_node_to_html_node(node))
        list_items_list.append(ParentNode("li", html_nodes))
    return ParentNode("ol", list_items_list)


def unordered_list_to_html(block):
    nodes_list = block.split("\n")
    list_items_list = []
    for current_node in nodes_list:
        item_text_list = current_node.split(" ")
        html_nodes = []
        text_nodes = text_to_textnodes(" ".join(item_text_list[1:]))
        for node in text_nodes:
            html_nodes.append(text_node_to_html_node(node))
        list_items_list.append(ParentNode("li", html_nodes))
    return ParentNode("ul", list_items_list)


def markdown_to_html_node(markdown):
    blocks_list = markdown_to_blocks(markdown)
    nodes_list = []
    for block in blocks_list:
        block_type = block_to_block_type(block)
        if block_type == BLOCK_TYPE_PARAGRAPH:
            nodes_list.append(paragraph_to_html(block))
        if block_type == BLOCK_TYPE_HEADING:
            nodes_list.append(heading_to_html(block))
        if block_type == BLOCK_TYPE_QUOTE:
            nodes_list.append(quote_to_html(block))
        if block_type == BLOCK_TYPE_CODE:
            nodes_list.append(code_to_html(block))
        if block_type == BLOCK_TYPE_ORDERED_LIST:
            nodes_list.append(ordered_list_to_html(block))
        if block_type == BLOCK_TYPE_UNORDERED_LIST:
            nodes_list.append(unordered_list_to_html(block))
    return ParentNode("div", nodes_list)
