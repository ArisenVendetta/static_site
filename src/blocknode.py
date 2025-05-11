from enum import Enum
from textnode import TextNode
from nodehelper import text_to_textnodes

class BlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class BlockNode:
    def __init__(self, content: str, block_type: BlockType = BlockType.PARAGRAPH):
        self.content = content
        self.block_type = block_type
        self.lines = content.split('\n')

    def __repr__(self):
        return f'BlockNode({self.content}, {self.block_type.value})'
    
    def __eq__(self, other: 'BlockNode'):
        if other is None or not isinstance(other, BlockNode):
            return False
        if self.content == other.content and self.block_type == other.block_type:
            return True
        return False


class HeaderNode(BlockNode):
    def __init__(self, content: str, header_size: int):
        super().__init__(content, BlockType.HEADING)
        self.header_size = header_size


class CodeNode(BlockNode):
    def __init__(self, content: str):
        super().__init__(content.strip('```'), BlockType.CODE)


class QuoteNode(BlockNode):
    def __init__(self, content: str):
        super().__init__('\n'.join([line.lstrip('>') for line in content.split('\n')]), BlockType.QUOTE)


class ListNode(BlockNode):
    def __init__(self, content: str, ordered: bool):
        self.prefix = '. ' if ordered else '- '
        self.block_type = BlockType.ORDERED_LIST if ordered else BlockType.UNORDERED_LIST
        super().__init__('\n'.join([line.lstrip(self.prefix) for line in content.split('\n')], self.block_type))