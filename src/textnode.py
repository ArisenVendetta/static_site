from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italics"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: 'TextNode'):
        if other is None or not isinstance(other, TextNode): 
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
    
