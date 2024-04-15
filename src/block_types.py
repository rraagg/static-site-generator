import re

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_UNORDERED_LIST = "unordered_list"
BLOCK_TYPE_ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    heading_pattern = "#{1,6} ."
    code_pattern = "^`{3}.*`{3}$"
    quote_pattern = "^>.*"
    unordered_list_pattern = "^[*-].*"
    ordered_list_pattern = "^[1][.]"
    if len(re.findall(heading_pattern, block)) != 0:
        return BLOCK_TYPE_HEADING
    if len(re.findall(code_pattern, block)) != 0:
        return BLOCK_TYPE_CODE
    if len(re.findall(quote_pattern, block)) != 0:
        if validate_block(block, BLOCK_TYPE_QUOTE):
            return BLOCK_TYPE_QUOTE
    if len(re.findall(unordered_list_pattern, block)) != 0:
        if validate_block(block, BLOCK_TYPE_UNORDERED_LIST):
            return BLOCK_TYPE_UNORDERED_LIST
    if len(re.findall(ordered_list_pattern, block)) != 0:
        if validate_block(block, BLOCK_TYPE_ORDERED_LIST):
            return BLOCK_TYPE_ORDERED_LIST
    return BLOCK_TYPE_PARAGRAPH


def validate_block(block, block_type):
    block_list = block.split("\n")
    if block_type == BLOCK_TYPE_QUOTE:
        for current_block in block_list:
            if current_block[0] != ">":
                return False
    if block_type == BLOCK_TYPE_UNORDERED_LIST:
        for current_block in block_list:
            if current_block[0] not in ["*", "-"]:
                return False
    if block_type == BLOCK_TYPE_ORDERED_LIST:
        for idx, current_block in enumerate(block_list):
            block_item = idx + 1
            next_block_item_list = current_block.split(".")
            if next_block_item_list[0] != str(block_item):
                return False
    return True
