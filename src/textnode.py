from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        text = self.text == other.text
        text_type = self.text_type.value == other.text_type.value
        url = self.url == other.url
        return text == text_type == url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
