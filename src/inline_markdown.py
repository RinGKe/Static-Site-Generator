from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for o in old_nodes:
        if o.text_type == "image" or o.text_type == "link":
            new_nodes.append(o)
        elif delimiter not in o.text:
            new_nodes.append(o)
        else:
            splits = o.text.split(delimiter)
            if len(splits) < 3 or not len(splits) % 2:
                raise Exception("Invalid markdown syntax: missing closing delimiter!")
            for i, s in enumerate(splits):
                if i % 2:
                    new_nodes.append(TextNode(text=s, text_type=text_type))
                else:
                    new_nodes.append(TextNode(text=s, text_type=TextType.TEXT))
    return new_nodes
