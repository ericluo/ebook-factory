import os
from ebooklib import epub
import markdown

mds_path = os.path.curdir
# Create a new epub book
book = epub.EpubBook()

# Convert multiple markdown files to chapters
def convert_mds_to_chapters():
    # Loop through all markdown files in the folder
    md_files = enumerate(filter(lambda x: x.endswith('.md'), os.listdir(mds_path)))
    for i, md_file_name in md_files:
        f = os.path.join(mds_path, md_file_name)
        with open(f, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()
        html_content = markdown.markdown(md_content, extensions=['extra'])
        chapter_title = os.path.splitext(os.path.basename(md_file_name))[0]
        chapter = epub.EpubHtml(title=f'Chapter {i+1} {chapter_title}', 
                                file_name=f'chapter_{i+1}.xhtml',
                                content = html_content)

        book.add_item(chapter) 
        # Add the chapter to the table of contents
        book.toc.append(epub.Link(chapter.file_name, chapter.title, chapter.id))

        # Add the chapter to the spine of the book
        book.spine.append(chapter)
    
# Convert multiple markdown files to a single epub book
def convert_mds_to_epub(input_dir, out_file):
    global mds_path 
    mds_path = input_dir
    epub_file = out_file

    # Set the title of the book
    book.set_title(os.path.splitext(os.path.basename(epub_file))[0])
    book.set_language('zh')
    # Add a table of contents
    book.toc = []

    cover_file = 'cover.jpg'
    book.set_cover(cover_file, content=os.path.join(mds_path, cover_file))
    book.add_author('Eric Luo')

    # from pygments.formatters import HtmlFormatter
    # style = HtmlFormatter().get_style_defs('.highlight')
    # style_item = epub.EpubItem(uid="code_style", file_name="code.css", media_type="text/css", content=style)
    # book.add_item(style_item)
    # css = epub.EpubItem(uid='style_nav', file_name='style/code.css', media_type='text/css')
    # content = open('style/code.css', 'r', encoding='utf-8').read()
    # css.set_content(content)
    # book.add_item(css)

    convert_mds_to_chapters()

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Save the book to the epub file
    from plugins.embedimage import EmbedImage
    from plugins.highlightcode import HighlightCode
    epub.write_epub(epub_file, book, {"plugins": [EmbedImage(), HighlightCode()]})

if __name__ == "__main__":
    # convert_mds_to_epub(r"E:/workspace/ebooks/notes", '伯克希尔股东大会笔记.epub')
    import argparse, sys
    parser = argparse.ArgumentParser(description='Convert multiple markdown files to a single epub book')
    parser.add_argument('input_dir', type=str, help='the input directory containing markdown files')
    parser.add_argument('out_file', type=str, help='the output epub file name')
    args = parser.parse_args()
    try:
        if not os.path.exists(args.input_dir):
            raise FileNotFoundError(f"Input directory {args.input_dir} not found.")
        if os.path.exists(args.out_file):
            os.remove(args.out_file)
    except Exception as e:
        print(f"Error accessing file: {e}")
        sys.exit()

    convert_mds_to_epub(args.input_dir, args.out_file)
