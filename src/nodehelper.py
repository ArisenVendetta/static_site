from blocknode import BlockNode, BlockType, HeaderNode, CodeNode, QuoteNode, ListNode
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, ImageNode
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
            return ImageNode(node.url, node.text)
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


def split_nodes_links(nodes: list[TextNode]) -> list[TextNode]: #not sure why but when pattern is loaded from constants.py it fails to match anything
    return split_nodes(nodes, 
                       extract_markdown_links, 
                       r'((?<!!)\[[^\]]+\]\([^\)]+\))', # so for now, keeping pattern locally
                       TextType.LINK) 


def split_nodes_images(nodes: list[TextNode]) -> list[TextNode]: #not sure why but when pattern is loaded from constants.py it fails to match anything
    return split_nodes(nodes, 
                       extract_markdown_images, 
                       r'(!\[[^\]]+\]\([^\)]+\))', # so for now, keeping pattern locally
                       TextType.IMAGE) 


def split_nodes(nodes: list[TextNode], extraction_func, pattern: str, resulting_node_type: TextType) -> list[TextNode]:
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
    return remove_empty_textnodes(nodes)

def remove_empty_textnodes(nodes: list[TextNode]) -> list[TextNode]:
    truncated_list = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            truncated_list.append(node)
        else:
            if node.text is None or len(node.text) < 1:
                continue
            truncated_list.append(node)
    return truncated_list


def extract_markdown_images(content: str) -> tuple[str, str]: #not sure why but when pattern is loaded from constants.py it fails to match anything
    return re.findall(r'!\[([^\]]+)\]\(([^\)]+)\)', content)  # so for now, keeping pattern locally


def extract_markdown_links(content: str) -> tuple[str, str]: #not sure why but when pattern is loaded from constants.py it fails to match anything
    return re.findall(r'(?<!!)\[([^\]]+)\]\(([^\)]+)\)', content) # so for now, keeping pattern locally


def markdown_to_blocks(markdown: str) -> list[BlockNode]:
    blocks = [BlockNode(block.strip(), BlockType.PARAGRAPH) for block in markdown.split('\n\n') if block.strip() != '']
    return blocks


def block_to_blocktype(block: BlockNode) -> BlockNode:
    if block is None:
        raise ValueError('provided block is nonetype')
    
    is_header = check_if_block_is_header(block)
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
    pattern = '^- ' if not ordered else '^\d+\. '
    for line in block.lines:
        if re.match(pattern, line) is None:
            return False
    return True

def detect_empty_node(node: HTMLNode) -> bool:
    if node is None:
        return True
    if node.tag == '' or node.tag == None:
        if node.value == '' or node.value == None:
            return True
    return False


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = [block_to_blocktype(block) for block in markdown_to_blocks(markdown)]
    children = []
    for block in blocks:
        output = None
        if isinstance(block, HeaderNode):
            output = ParentNode(f'h{block.header_size}', [convert_text_node_to_html_node(node) for node in text_to_textnodes(block.content)])
        elif isinstance(block, CodeNode):
            code = LeafNode('code', block.content)
            output = ParentNode('pre', [code])
        elif isinstance(block, ListNode):
            list_items = []
            for line in block.lines:
                child_nodes = [convert_text_node_to_html_node(node) for node in text_to_textnodes(line)]
                list_items.append(ParentNode('li', child_nodes))
            output = ParentNode('ol' if block.block_type == BlockType.ORDERED_LIST else 'ul', list_items)
        elif isinstance(block, QuoteNode):
            child_nodes = [convert_text_node_to_html_node(node) for node in text_to_textnodes(block.content)]
            output = ParentNode('blockquote', child_nodes)
        else:
            child_nodes = []
            text_nodes = text_to_textnodes(block.content.replace('\n', ' '))
            for node in text_nodes:
                htmlnode = convert_text_node_to_html_node(node)
                if isinstance(htmlnode, LeafNode):
                    if (htmlnode.tag == None or htmlnode.tag == '') and (htmlnode.value == None or htmlnode.value == ''):
                        print(f'Empty leafnode found ({htmlnode})')
                        continue
                child_nodes.append(htmlnode)
            output = ParentNode('p', child_nodes)
        if detect_empty_node(output):
            print(output)
        else:
            children.append(output)

    return ParentNode('div', children)
