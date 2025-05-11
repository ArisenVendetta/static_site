from blocknode import BlockNode, BlockType, HeaderNode, CodeNode, QuoteNode, ListNode
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import re
from constants import *
import pprint


def convert_text_node_to_html_node(node: TextNode) -> HTMLNode:
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


def split_text_nodes_by(nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
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


def split_nodes_links(nodes: list[TextNode]): #not sure why but when pattern is loaded from constants.py it fails to match anything
    return split_nodes(nodes, 
                       extract_markdown_links, 
                       r'((?<!!)\[[^\]]+\]\([^\)]+\))', # so for now, keeping pattern locally
                       TextType.LINK) 


def split_nodes_images(nodes: list[TextNode]): #not sure why but when pattern is loaded from constants.py it fails to match anything
    return split_nodes(nodes, 
                       extract_markdown_images, 
                       r'(!\[[^\]]+\]\([^\)]+\))', # so for now, keeping pattern locally
                       TextType.IMAGE) 


def split_nodes(nodes: list[TextNode], extraction_func, pattern: str, resulting_node_type: TextType):
    updated_nodes = []

    if len(pattern) < 1 or pattern is None:
        raise ValueError(f'pattern is required for finding appropriate markdown images/links')

    if resulting_node_type not in [TextType.LINK, TextType.IMAGE]:
        raise ValueError(f'invalid resulting_node_type, must be LINK or IMAGE')

    for node in nodes:
        if node.text_type != TextType.TEXT:
            updated_nodes.append(node)
            continue

        found_links = extraction_func(node.text)
        if len(found_links) < 1:
            updated_nodes.append(node)
            continue

        # use regex to split the string based on the same pattern used to extract the markdown links
        sections = re.split(pattern, node.text)
        for section in sections:
            if len(section) < 1 or section is None:
                continue
            
            add_text = True
            for link in found_links:
                original = f'[{link[0]}]({link[1]})'
                if resulting_node_type == TextType.IMAGE:
                    original = f'!{original}'
                if section == original:
                    updated_nodes.append(TextNode(link[0], resulting_node_type, link[1]))
                    add_text = False
                    break
            if add_text:
                updated_nodes.append(TextNode(section, TextType.TEXT))
    
    return updated_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_text_nodes_by(nodes.copy(), '**', TextType.BOLD)
    nodes = split_text_nodes_by(nodes.copy(), '_', TextType.ITALIC)
    nodes = split_text_nodes_by(nodes.copy(), '`', TextType.CODE)
    nodes = split_nodes_links(nodes.copy())
    nodes = split_nodes_images(nodes.copy())
    return nodes


def extract_markdown_images(content: str) -> tuple[str, str]: #not sure why but when pattern is loaded from constants.py it fails to match anything
    return re.findall(r'!\[([^\]]+)\]\(([^\)]+)\)', content)  # so for now, keeping pattern locally


def extract_markdown_links(content: str) -> tuple[str, str]: #not sure why but when pattern is loaded from constants.py it fails to match anything
    return re.findall(r'(?<!!)\[([^\]]+)\]\(([^\)]+)\)', content) # so for now, keeping pattern locally


def markdown_to_blocks(markdown: str) -> list[BlockNode]:
    blocks = [BlockNode(block.strip(), BlockType.PARAGRAPH) for block in markdown.split('\n\n')]
    return blocks


def block_to_blocktype(block: BlockNode) -> BlockNode:
    if block is None:
        raise ValueError('provided block is nonetype')
    
    is_header = check_if_block_is_header(block.content)
    if is_header[0]:
        return HeaderNode(block.content, is_header[1])
    elif check_if_block_is_code(block):
        return CodeNode(block.content)
    elif check_if_block_is_quote(block):
        return QuoteNode(block.content)
    elif check_if_block_is_list(block, ordered=False):
        return ListNode(block.content, ordered=False)
    elif check_if_block_is_list(block, ordered=True):
        return ListNode(block.content, ordered=True)
    else:
        return block
        

def check_if_block_is_header(block: BlockNode) -> tuple[bool, int]:
    line_sections = block.content.split(' ')
    if line_sections[0].startswith('#'):
        return (True, len(line_sections[0]))
    return (False, -1)


def check_if_block_is_code(block: BlockNode) -> bool:
    return block.content.startswith('```') and block.content.endswith('```')


def check_if_block_is_quote(block: BlockNode) -> bool:
    for line in block.lines:
        if line.startswith('>') == False:
            return False
    return True


def check_if_block_is_list(block: BlockNode, ordered: bool) -> bool:
    prefix = '. ' if ordered else '- ' 
    for line in block.lines:
        if line.startswith(prefix) == False:
            return False
    return True


def markdown_to_html_node(markdown: str):
    blocks = [block_to_blocktype(block) for block in markdown_to_blocks(markdown)]
    
