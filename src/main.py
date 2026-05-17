from functions import *
from htmlnode import *
from textnode import *


def main():
    node = TextNode("This is some anchor text", TextType.LINK, "http://www.boot.dev")
    print(node)


main()
