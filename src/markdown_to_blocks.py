def markdown_to_blocks(markdown):
    lines_list = markdown.split("\n")
    block_strings_list = []
    current_block = []
    for line in lines_list:
        new_line = line.strip()
        if new_line == "" and len(current_block) == 0:
            continue
        if new_line == "" and len(current_block) == 1:
            block_strings_list.append(current_block[0])
            current_block.clear()
            continue
        if len(current_block) == 0:
            current_block.append(new_line)
        else:
            current_block[0] = current_block[0] + "\n" + new_line
    if len(current_block) == 1:
        block_strings_list.append(current_block[0])
    return block_strings_list
