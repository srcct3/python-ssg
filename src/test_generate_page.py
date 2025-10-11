import unittest

from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title_single_line(self):
        md = "# title"
        res = extract_title(md)
        self.assertEqual(res, "title")

    def test_extract_title_multy_line(self):
        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)
        """
        res = extract_title(md)
        self.assertEqual(res, "Tolkien Fan Club")

    def test_extract_title_no_tile(self):
        with self.assertRaises(ValueError) as context:
            extract_title("No title")
        self.assertEqual(str(context.exception), "Markdown has no header")
