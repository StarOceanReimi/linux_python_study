from lxml import etree
from lxml.cssselect import CSSSelector
from prettytable import PrettyTable
XML_PATH='book.xml'

tree = etree.parse(XML_PATH)

def get_book_titles_by_xpath():
    title_xpath = tree.xpath('//title')
    return [e for e in title_xpath]

def get_book_titles_by_css():
    title_sel = CSSSelector('title')
    return [e for e in title_sel(tree)]

def _show_text(root, elname):
    return root.xpath(elname)[0].text

def show_simple_table():
    """show a prettytable table contains bookname, 
    publish date, and price according retriving
    data from book.xml
    """
    book_xpath = tree.xpath('//book')
    pt = PrettyTable(['BookName', 'Author', 'Publish Date', 'Price'])
    pt.align.update(dict.fromkeys(['BookName', 'Author'], 'l'))
    map_fuc = lambda ctx: lambda name: _show_text(ctx, name)
    for book in book_xpath:
        pt.add_row(map(map_fuc(book), ['title', 'author', 'publish_date', 'price']))
    print pt

if __name__ == "__main__":
    show_simple_table()
