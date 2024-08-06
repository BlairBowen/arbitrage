from lxml import html, etree


if __name__ == "__main__":

    with open('/home/bowenbv/Code/arbitrage_tool/arbitrage_tool/sportsbook_scraper/test.html', 'r') as file:
        content = file.read()
    html_content = content
    tree = html.fromstring(html_content)
    print(etree.tostring(tree, pretty_print=True, encoding='unicode'))
    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(etree.tostring(tree, pretty_print=True, encoding='unicode'))