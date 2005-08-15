# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

"""
examine all plugins and elements and output xml documentation for them
used as part of the plugin documentation build
"""

import sys
import os
import gst

INDENT_SIZE = 2

# all templates
ELEMENT_TEMPLATE = """<element>
  <name>%(name)s</name>
  <longname>%(longname)s</longname>
  <class>%(class)s</class>
  <description>%(description)s</description>
  <author>%(author)s</author>
</element>"""

PLUGIN_TEMPLATE = """<plugin>
  <name>%(name)s</name>
  <description>%(description)s</description>
  <filename>%(filename)s</filename>
  <basename>%(basename)s</basename>
  <version>%(version)s</version>
  <license>%(license)s</license>
  <package>%(package)s</package>
  <origin>%(origin)s</origin>
  <elements>
%(elements)s
  </elements>
</plugin>"""

def xmlencode(line):
    """
    Replace &, <, and >
    """
    line = "&amp;".join(line.split("&"))
    line = "&lt;".join(line.split("<"))
    line = "&gt;".join(line.split(">"))
    return line

def get_offset(indent):
    return " " * INDENT_SIZE * indent

def output_element_factory(elf, indent=0):
    print  "ELEMENT", elf.get_name()
    d = {
        'name':        xmlencode(elf.get_name()),
        'longname':    xmlencode(elf.get_longname()),
        'class':       xmlencode(elf.get_klass()),
        'description': xmlencode(elf.get_description()),
        'author':      xmlencode(elf.get_author()),
    }
    block = ELEMENT_TEMPLATE % d
    
    offset = get_offset(indent)
    return offset + ("\n" + offset).join(block.split("\n"))


def output_plugin(plugin, indent=0):
    print "PLUGIN", plugin.get_name()
    version = ".".join([str(i) for i in plugin.get_version()])
    
    elements = []
    for feature in plugin.get_feature_list():
        if isinstance(feature, gst.ElementFactory):
            elements.append(output_element_factory(feature, indent + 2))
        
    filename = plugin.get_filename()
    basename = filename
    if basename:
        basename = os.path.basename(basename)
    d = {
        'name':        xmlencode(plugin.get_name()),
        'description': xmlencode(plugin.get_description()),
        'filename':    filename,
        'basename':    basename,
        'version':     version,
        'license':     xmlencode(plugin.get_license()),
        'package':     xmlencode(plugin.get_package()),
        'origin':      xmlencode(plugin.get_origin()),
        'elements': "\n".join(elements),
    }
    block = PLUGIN_TEMPLATE % d
    
    offset = get_offset(indent)
    return offset + ("\n" + offset).join(block.split("\n"))

def main():
    if sys.argv[1]:
        os.chdir(sys.argv[1])

    all = gst.registry_pool_plugin_list()
    for plugin in all:
        filename = "plugin-%s.xml" % plugin.get_name()
        handle = open(filename, "w")
        handle.write(output_plugin(plugin))
        handle.close()

main()
