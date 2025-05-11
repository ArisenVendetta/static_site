from textnode import TextNode, TextType
from nodehelper import markdown_to_html_node
import pprint

def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    print(markdown_to_html_node(md).to_html())

    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    print(markdown_to_html_node(md).to_html())


main()