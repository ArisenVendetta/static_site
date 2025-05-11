from textnode import TextNode, TextType
from nodehelper import markdown_to_blocks
import pprint

def main():
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    pprint.pp(markdown_to_blocks(md))


main()