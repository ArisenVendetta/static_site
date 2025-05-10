from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def convert_text_node_to_html_node(node: TextNode):
    match node.text_type:
        case TextType.TEXT:
            return LeafNode(None, node.text)
        case TextType.BOLD:
            return LeafNode('b', node.text)
        case TextType.ITALIC:
            return LeafNode('i', node.text)
        case TextType.CODE:
            return LeafNode('code', node.text)
        case TextType.LINK:
            return LeafNode('a', node.text, {'href': node.url})
        case TextType.IMAGE:
            return LeafNode('img', None, {'src': node.url, 'alt': node.text})
    raise Exception(f'invalid node type ({node.text_type.value})')

def split_text_nodes_by(nodes: list[TextNode], delimiter: str, text_type: TextType):
    updated_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            updated_nodes.append(node)
            continue

        split_content = node.text.split(delimiter)
        if len(split_content) < 3:
            updated_nodes.append(node)
            continue

        for i in range(0, len(split_content)):
            new_type = text_type
            if i % 2 == 0:
                new_type = node.text_type
            if i == len(split_content)-1:
                new_type = node.text_type
            new_node = TextNode(split_content[i], new_type)
            updated_nodes.append(new_node)
    return updated_nodes