from ebooklib import epub
from ebooklib.plugins.base import BasePlugin
from ebooklib.utils import parse_html_string

from urllib.parse import urlparse

from pathlib import Path

class EmbedImage(BasePlugin):
    def html_before_write(self, book, chapter):

        def get_img_content(uri):
            u = urlparse(uri)
            if u.scheme != '':
                import requests
                return requests.get(uri).content
            else:
                return Path(uri).read_bytes()

        from lxml import etree
        try:
            tree = parse_html_string(chapter.content)
        except etree.XMLSyntaxError as e:
            print(f"Error parsing HTML content: {e}")
            return

        root = tree.getroottree()

        if root.find('body'):
            body = tree.find('body')

            for _img_node in body.xpath('//img'):
                src = _img_node.get('src', '')
                try:
                    _img_content = get_img_content(src)
                except Exception as e:
                    print(f"Error accessing image file {src}: {e}")
                    continue

                img = epub.EpubImage(media_type='image/jpeg', content=_img_content)
                book.add_item(img)

                img.file_name = f"images/{img.id}{Path(src).suffix}"
                _img_node.set('src', img.file_name)
                chapter.content = etree.tostring(tree, pretty_print=True, encoding='utf-8')        