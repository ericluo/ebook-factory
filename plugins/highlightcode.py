from ebooklib.plugins.base import BasePlugin
from ebooklib.utils import parse_html_string


from ebooklib import epub

class HighlightCode(BasePlugin):    
    def __init__(self):
        pass

    def html_before_write(self, book, chapter):
        from lxml import etree, html

        from pygments import highlight
        from pygments.formatters import HtmlFormatter

        try:
            tree = parse_html_string(chapter.content)
        except:
            return

        root = tree.getroottree()

        had_source = False

        if len(root.find('body')) != 0:
            body = tree.find('body')
            # check for embeded source
            # for source in body.xpath('//pre[contains(@class,"source-")]'):
            for source in body.xpath('//code[contains(@class,"language-")]'):
                css_class = source.get('class')

                source_text = (source.text or '') + ''.join([html.tostring(child) for child in source.iterchildren()])

                if 'language-python' in css_class:
                    from pygments.lexers import PythonLexer

#                    _text =  highlight(source_text, PythonLexer(), HtmlFormatter(linenos="inline"))
                    _text =  highlight(source_text, PythonLexer(), HtmlFormatter())

                if 'language-css' in css_class:
                    from pygments.lexers import CssLexer

                    _text =  highlight(source_text, CssLexer(), HtmlFormatter())

                _parent = source.getparent()
                _parent.replace(source, etree.XML(_text))

                had_source = True

        if had_source:
            # create a new link element
            from pygments.formatters import HtmlFormatter
            highlight_style = HtmlFormatter().get_style_defs('.highlight')

            # add the link element to the head of an existing tree
            head = root.find('head')
            if head is None:
                html = root.getroot()
                html.insert(0, etree.Element('head'))
            head = root.find('head')
            style = etree.SubElement(head, 'style')
            style.text = highlight_style
            
            chapter.content = etree.tostring(tree, pretty_print=True, encoding='utf-8')     