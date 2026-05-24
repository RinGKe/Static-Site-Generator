import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    splits = markdown.split("\n\n")
    splits = [x.strip() for x in splits]
    splits = [x for x in splits if x]
    return splits


def block_to_block_type(block):
    lines = block.splitlines()

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if (
        (lines[0].startswith("```") or lines[0].startswith("~~~"))
        and (lines[-1].rstrip() == "```" or lines[-1].rstrip() == "~~~")
        and (len(lines) > 1)
    ):
        return BlockType.CODE

    if all(re.match(r"^> ?", x) for x in lines):
        return BlockType.QUOTE

    if all(re.match(r"^- ", x) for x in lines):
        return BlockType.UNORDERED_LIST

    if all(x.startswith(f"{i + 1}. ") for i, x in enumerate(lines)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def block_type_to_html(type: BlockType, block):
    match type:
        case BlockType.PARAGRAPH:
            return
        case BlockType.HEADING:
            return
        case BlockType.CODE:
            return
        case BlockType.QUOTE:
            return
        case BlockType.UNORDERED_LIST:
            return
        case BlockType.ORDERED_LIST:
            return


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for b in blocks:
        type = block_to_block_type(b)
        node = block_type_to_html(type, block)
