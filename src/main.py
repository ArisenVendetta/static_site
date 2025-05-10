from textnode import TextNode, TextType
from nodehelper import text_to_textnodes
import pprint

def main():
    pprint.pp(text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"))


main()