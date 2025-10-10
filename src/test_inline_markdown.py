import unittest
from inline_markdown import extract_markdown_images, split_nodes_delimiter, extract_markdown_link


from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestImageAndUrl(unittest.TestCase):
    def test_image_extract_basic(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        res = extract_markdown_images(text)
        self.assertListEqual(res, expected)

    def test_image_extract_multi_line(self):
        text = """
        Here’s some markdown:
        ![cat](https://example.com/cat.png)
        Some text in between.
        ![doggo](https://example.com/dog.jpg)
        """
        expected = [("cat", "https://example.com/cat.png"), ("doggo", "https://example.com/dog.jpg")]

        res = extract_markdown_images(text)
        self.assertListEqual(res, expected)

    def test_incomplete_img(self):
        text = "This link is missing a closing parenthesis [broken](https://broken.com"
        expected = []
        res = extract_markdown_images(text)
        self.assertListEqual(res, expected)

    def test_image_extract_longer_alt_text(self):
        text = "Meet ![my favorite dog, Rex!](https://pets.com/rex.png) and ![cute cat 😺](https://pets.com/cat.png)"
        expected = [("my favorite dog, Rex!", "https://pets.com/rex.png"), ("cute cat 😺", "https://pets.com/cat.png")]
        res = extract_markdown_images(text)
        self.assertListEqual(res, expected)

    def test_image_extract_ignore_non_image(self):
        text = "Check out [this site](https://example.com) and ![this meme](https://memes.com/meme.jpg)"
        expected = [("this meme", "https://memes.com/meme.jpg")]
        res = extract_markdown_images(text)
        self.assertListEqual(res, expected)

    def test_image_extract_ignore_mixed_content(self):

        text = """
        Regular text, ![first](http://img.com/1.png)
        Another one ![second](http://img.com/2.png)
        Inline [link](http://example.com) and ![third image](http://img.com/3.png)
        """
        expected = [
          ("first", "http://img.com/1.png"),
          ("second", "http://img.com/2.png"),
          ("third image", "http://img.com/3.png")
        ]
        res = extract_markdown_images(text)
        self.assertListEqual(res, expected)

    def test_url_basic(self):
        text = "This is [Google](https://google.com) and [GitHub](https://github.com)"
        expected = [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        res = extract_markdown_link(text)
        self.assertListEqual(res, expected)

    def test_url_mult_line(self):
        text = """
        Here's a paragraph with
        [a link](http://example.com)
        and another [second link](https://example.org/test).
        """
        expected = [("a link", "http://example.com"), ("second link", "https://example.org/test")]
        res = extract_markdown_link(text)
        self.assertListEqual(res, expected)

    def test_url_long_text(self):
        text = "Visit [my awesome site 😎](https://mysite.io) or [cool-tools!](https://tools.dev)"
        expected = [("my awesome site 😎", "https://mysite.io"), ("cool-tools!", "https://tools.dev")]
        res = extract_markdown_link(text)
        self.assertListEqual(res, expected)

    def test_ignore_image(self):
        text = "An image ![alt text](https://img.com/img.png) and a link [real link](https://example.com)"
        expected = [("real link", "https://example.com")]
        res = extract_markdown_link(text)
        self.assertListEqual(res, expected)

    def test_incomplete_url(self):
        text = "This link is missing a closing parenthesis [broken](https://broken.com"
        expected = []
        res = extract_markdown_link(text)
        self.assertListEqual(res, expected)

    def test_complex_url_mix(self):
        text = """
        [Home](https://site.com)
        Some text ![image](https://img.com/img.jpg)
        [Docs](https://site.com/docs)
        and [Contact Us](mailto:contact@site.com)
        """
        expected = [
            ("Home", "https://site.com"),
            ("Docs", "https://site.com/docs"),
            ("Contact Us", "mailto:contact@site.com"),
        ]
        res = extract_markdown_link(text)
        self.assertListEqual(res, expected)

if __name__ == "__main__":
    unittest.main()
