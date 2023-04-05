from ebooklib import epub
from ebooklib.plugins.base import BasePlugin
from ebooklib.utils import parse_html_string

from urllib.parse import urlparse

from pathlib import Path

class EmbedImage(BasePlugin):
    def html_before_write(self, book, chapter):
        from lxml import etree

        try:
            tree = parse_html_string(chapter.content)
        except:
            return

        root = tree.getroottree()

        if len(root.find('body')) != 0:
            body = tree.find('body')

            for _img_node in body.xpath('//img'):
                src = _img_node.get('src', '')
                u = urlparse(src)
                suffix = Path(u.path).suffix

                if u.scheme != '':
                    try:
                        import requests
                        _img_content = requests.get(src).content
                    except Exception as e:
                        print(f"Error accessing image file {src}: {e}")
                        continue
                else:
                    try:
                        _img_content = Path(src).read_bytes()
                    except FileNotFoundError:
                        print(f"Image file {src} not found.")
                        continue
                    except Exception as e:
                        print(f"Error accessing image file {src}: {e}")
                        continue


                img = epub.EpubImage(media_type='image/jpeg', content=_img_content)
                book.add_item(img)

                img.file_name = f"images/{img.id}{suffix}"
                _img_node.set('src', img.file_name)
                chapter.content = etree.tostring(tree, pretty_print=True, encoding='utf-8')        