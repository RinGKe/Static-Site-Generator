import re

from src.textnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for o in old_nodes:
        if o.text_type != TextType.TEXT:
            new_nodes.append(o)
            continue
        splits = o.text.split(delimiter)
        if not len(splits) % 2:
            raise Exception("Invalid markdown syntax: missing closing delimiter!")
        for i, s in enumerate(splits):
            if s == "":
                continue
            if i % 2:
                new_nodes.append(TextNode(text=s, text_type=text_type))
            else:
                new_nodes.append(TextNode(text=s, text_type=TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_images(old_nodes):
    new_nodes = []
    for o in old_nodes:
        if o.text_type != TextType.TEXT:
            new_nodes.append(o)
            continue
        matches = extract_markdown_images(o.text)
        if not matches:
            new_nodes.append(o)
            continue
        splits = re.split(r"(!\[.*?\]\(.*?\))", o.text)
        for s in splits:
            if s == "":
                continue
            for m in matches:
                if s == f"![{m[0]}]({m[1]})":
                    new_nodes.append(
                        TextNode(text=m[0], text_type=TextType.IMAGE, url=m[1])
                    )
                    break
            else:
                new_nodes.append(TextNode(text=s, text_type=TextType.TEXT))
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for o in old_nodes:
        if o.text_type != TextType.TEXT:
            new_nodes.append(o)
            continue
        matches = extract_markdown_links(o.text)
        if not matches:
            new_nodes.append(o)
            continue
        splits = re.split(r"(?<!!)(\[.*?\]\(.*?\))", o.text)
        for s in splits:
            if s == "":
                continue
            for m in matches:
                if s == f"[{m[0]}]({m[1]})":
                    new_nodes.append(
                        TextNode(text=m[0], text_type=TextType.LINK, url=m[1])
                    )
                    break
            else:
                new_nodes.append(TextNode(text=s, text_type=TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text=text, text_type=TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_images(new_nodes)
    new_nodes = split_nodes_links(new_nodes)
    return new_nodes
