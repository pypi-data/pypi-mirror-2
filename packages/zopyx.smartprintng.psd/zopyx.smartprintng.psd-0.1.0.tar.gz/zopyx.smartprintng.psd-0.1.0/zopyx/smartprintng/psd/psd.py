################################################################
# zopyx.smartprintng.psd
# (C) 2010, ZOPYX Ltd, All rights reserved
################################################################

"""
PSD to PrinceXML converter based on psdparse:
http://www.telegraphics.com.au/svn/psdparse
"""

import os
import re
import sys
import shutil
import commands
import tempfile
import optparse
from lxml import etree


def _c(value, unit):
    if unit == 'pt':
        return '%spt' % value
    elif unit == 'mm':
        return '%2.1fmm' % (float(value) / 11.81)
    else:
        raise ValueError('Unsupported unit: %s' % unit)

def parse_psd(filename, options):

    output_directory = options.output_directory
    if not output_directory:
        output_directory = tempfile.mktemp()

    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory)

    # external PSD to XML parser
    cmd = 'psdparse -e -r --xmlout --pngdir "%s" --writepng "%s"' % (output_directory, filename)
    status, xml = commands.getstatusoutput(cmd)

    # cleanup XML and store it 
    xml = re.sub('(&#.*?;)', '', xml)
    file(os.path.join(output_directory, 'source.xml'), 'w').write(xml)
    tree = etree.fromstring(xml)

    css_out = file(os.path.join(output_directory, 'styles.css'), 'w')
    html_out = file(os.path.join(output_directory, 'index.html'), 'w')

    print >>html_out, '<html>'
    print >>html_out, '<head>'
    print >>html_out, '<link rel="stylesheet" type="text/css" href="styles.css"/>'
    print >>html_out, '</head>'
    print >>html_out, '<body>'

    # determine page size
    page_width = _c(tree.attrib['COLUMNS'], options.units)
    page_height = _c(tree.attrib['ROWS'], options.units)

    print >>css_out, '@page { size: %s %s}' % (page_width, page_height)
    print >>css_out, '@page { margin: 0 0 0 0}'
    if options.outline:
        print >>css_out, '.layer {border: 1pt dashed grey;}'
    print >>css_out

    print 'Page: %s x %s' % (page_width, page_height)

    for num, layer in enumerate(tree.iterfind('.//LAYER')):

        name = layer.attrib['NAME']
        top = _c(layer.attrib['TOP'], options.units)
        left = _c(layer.attrib['LEFT'], options.units)
        bottom = _c(layer.attrib['BOTTOM'], options.units)
        right = _c(layer.attrib['RIGHT'], options.units)
        width = _c(layer.attrib['WIDTH'], options.units)
        height = _c(layer.attrib['HEIGHT'], options.units)

        print 'Layer (%s): %s/%s -> %s/%s' % (name, top, left, right, bottom)

        if width == page_width and height == page_height:
            print '...omitted (background layer)'
            continue

        # check for text node(s)
        text = []
        for node in layer.iterfind('.//Text'):
            node_text = node.text
            node_text  = node_text.replace('\n', '<br/>')
            text.append(node_text)

        # check for images (PNG node)
        bg_image = None
        png_node = layer.find('.//PNG')
        if png_node is not None:
            bg_image = png_node.attrib['FILE']

        # Figure out fonts

        fonts = []
        for node in layer.iterfind('.//FontSet//Name'):
            if not node.text in fonts:
                fonts.append(node.text)

        # HTML DIV
        print >>html_out, '<!-- layer: %s -->' % name 
        print >>html_out, '<div class="layer" id="content-%d">' % num
        if text:
            print >>html_out, (' '.join(text)).encode('utf-8', 'ignore')
        print >>html_out, '</div>'
        print >>html_out

        # CSS
        print >>css_out, '/* layer: %s */' % name 
#        print >>css_out, '#content-%d::before { ' % num
#        print >>css_out, '     content: "content-%d";' % num
#        print >>css_out, '     color: blue;'
#        print >>css_out, '}'
#        print
        print >>css_out, '#content-%d {' % num
        print >>css_out, '    position: absolute;'
        print >>css_out, '    left: %s;' % left;
        print >>css_out, '    top: %s;' % top;
        print >>css_out, '    width: %s;' % width;
        print >>css_out, '    height: %s;' % height;
        if bg_image and not text:
            print >>css_out, '    background-image: url("%s");' % os.path.basename(bg_image)
        if text:
            print >>css_out, '    font-size: 11pt;'
        if fonts:
            print >>css_out, '    font-family: %s;' % ', '.join(['"%s"' % font for font in fonts])

        print >>css_out, '}'
        print >>css_out

    print >>html_out, '</body>'
    print >>html_out, '</html>'

    html_out.close()
    css_out.close()
    return os.path.abspath(output_directory)

def main():

    usage = "usage: %prog [options] psd-file"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-o', '--output-directory', action='store', default='converted',
                      dest='output_directory',
                      help='Output directory')
    parser.add_option('-u', '--units', action='store', default='pt',
                      dest='units',
                      help='Unit (pt(default) or mm)')
    parser.add_option('-l', '--outline', action='store_true', default=False,
                      dest='outline',
                      help='Outline boxes')

    options, args = parser.parse_args()
    if not args:
        raise RuntimeError('No PSD given')

    return parse_psd(args[0], options)


if __name__ == '__main__':
    main()
