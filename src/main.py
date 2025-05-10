from textnode import TextNode, TextType
from nodehelper import split_text_nodes_by


def main():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_text_nodes_by([node], "`", TextType.CODE)
    print(new_nodes)


main()