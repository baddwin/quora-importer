"""Utility functions to create a WXR file for Wordpress.
(c) axeleroy
https://gist.github.com/axeleroy/b5bfe66c365c5d70fdaeb6d9845411cb
"""

import os

from lxml import etree as ET
from lxml.etree import CDATA

# XML namespaces declarations
DC_NS = "http://purl.org/dc/elements/1.1/"
WP_NS = "http://wordpress.org/export/1.2/"
CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"
EXCERPT_NS = "http://wordpress.org/export/1.2/excerpt/"

NSMAP = {
    "dc": DC_NS,
    "wp": WP_NS,
    "content": CONTENT_NS,
    "excerpt": EXCERPT_NS
}
# To make use of namespaces easier
DC = "{{{0}}}".format(DC_NS)
WP = "{{{0}}}".format(WP_NS)
CONTENT = "{{{0}}}".format(CONTENT_NS)
EXCERPT = "{{{0}}}".format(EXCERPT_NS)


def create_root_node():
    # Passing the namespaces map in order to use tags such as <wp:author>
    root = ET.Element("rss", version="2.0", nsmap=NSMAP)
    return root


def create_text_node(parent, name, content):
    node = ET.SubElement(parent, name)
    node.text = content
    return node


def create_channel_node(root_node, website_title, website_root, language):
    channel_node = ET.SubElement(root_node, "channel")
    create_text_node(channel_node, "title", website_title)
    create_text_node(channel_node, "link", website_root)
    create_text_node(channel_node, "language", language)
    create_text_node(channel_node, WP + "wxr_version", "1.2")
    create_text_node(channel_node, WP + "base_site_url", website_root)
    create_text_node(channel_node, WP + "base_blog_url", website_root)

    wp_author = ET.SubElement(channel_node, WP + 'author')
    create_text_node(wp_author, WP + "author_id", "1")
    create_text_node(wp_author, WP + "author_login", CDATA("author"))
    create_text_node(wp_author, WP + "author_email", CDATA("author@domain.tld"))
    create_text_node(wp_author, WP + "author_display_name", CDATA("author"))

    create_text_node(channel_node, "generator", "https://wordpress.org/?v=5.2")
    return channel_node


def create_item_node(*, parent, post_id, title, link, post_name, status, post_type, date, date_gmt):
    item = ET.SubElement(parent, 'item')
    create_text_node(item, "title", title)
    create_text_node(item, "link", link)
    create_text_node(item, DC + "creator", CDATA("author"))
    create_text_node(item, "description", "")
    create_text_node(item, WP + "post_id", post_id)
    create_text_node(item, WP + "post_date", CDATA(date))
    create_text_node(item, WP + "post_date_gmt", CDATA(date_gmt))
    create_text_node(item, WP + "comment_status", CDATA("closed"))
    create_text_node(item, WP + "ping_status", CDATA("closed"))
    create_text_node(item, WP + "post_name", CDATA(post_name))
    create_text_node(item, WP + "status", CDATA(status))
    create_text_node(item, WP + "post_parent", "0")
    create_text_node(item, WP + "menu_order", "0")
    create_text_node(item, WP + "post_type", CDATA(post_type))
    create_text_node(item, WP + "post_password", CDATA(""))
    create_text_node(item, WP + "is_sticky", "0")
    return item


def create_post_meta_node(parent, key, value):
    post_meta = ET.SubElement(parent, WP + "postmeta")
    create_text_node(post_meta, WP + "meta_key", CDATA(key))
    create_text_node(post_meta, WP + "meta_value", CDATA(value))


def serialize_array(array):
    string = 'a:{0}:{{'.format(len(array) // 2)
    for el in array:
        string += 's:{0}:"{1}";'.format(len(el), el)
    string += '}'
    return string


def write_xml(root_node, filename):
    tree = ET.ElementTree(root_node)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        tree.write(filename, pretty_print=True, encoding='utf-8', xml_declaration=True)

    except Exception as e:
        print(f'error writing file: {e}')
