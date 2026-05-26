import re
from enum import Enum

from src.htmlnode import *
from src.inline_markdown import *


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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_type_to_html(x) for x in blocks]
    return ParentNode(tag="div", children=children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(x) for x in text_nodes]
    return html_nodes


def block_type_to_html(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            block = " ".join(block.splitlines())
            return ParentNode(tag="p", children=text_to_children(block))

        case BlockType.HEADING:
            num = len(block) - len(block.lstrip("#"))
            block = " ".join(block.strip("#").strip().splitlines())
            return ParentNode(tag=f"h{num}", children=text_to_children(block))

        case BlockType.CODE:
            block = block.strip("`").lstrip("\n")
            code_node = text_node_to_html_node(
                TextNode(
                    text=block,
                    text_type=TextType.CODE,
                )
            )
            return ParentNode(tag="pre", children=[code_node])

        case BlockType.QUOTE:
            lines = [x.strip(">").strip() for x in block.splitlines()]
            block = " ".join(lines)
            return ParentNode(tag="blockquote", children=text_to_children(block))

        case BlockType.UNORDERED_LIST:
            wraps = [
                ParentNode(tag="li", children=text_to_children(x[2:]))
                for x in block.splitlines()
            ]
            return ParentNode(tag="ul", children=wraps)

        case BlockType.ORDERED_LIST:
            wraps = [
                ParentNode(tag="li", children=text_to_children(x[3:]))
                for x in block.splitlines()
            ]
            return ParentNode(tag="ol", children=wraps)
