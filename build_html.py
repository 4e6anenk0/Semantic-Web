from lxml.etree import parse, XSLT

# building html

def html_building():
    dom = parse('xml_gen_update.xml')
    xslt = parse('components/style.xslt')
    transform = XSLT(xslt)
    newdom = transform(dom)
    return newdom

new_html = html_building()

f = open('new.html', 'w')
f.write(str(new_html))
f.close