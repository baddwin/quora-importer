import os
from bs4.element import PageElement

from exporter.base import Export
# Import LXML to manipulate XML files
from lxml import etree as ET
from lxml.etree import CDATA
from dateutil import parser
from dateutil.tz import tzoffset

# Import wordpress specific nodes
from exporter.wxr_utils import WP
from exporter.wxr_utils import CONTENT
from exporter.wxr_utils import EXCERPT

from exporter.wxr_utils import create_root_node
from exporter.wxr_utils import create_channel_node
from exporter.wxr_utils import create_item_node
from exporter.wxr_utils import create_text_node
from exporter.wxr_utils import create_post_meta_node
from exporter.wxr_utils import serialize_array
from exporter.wxr_utils import write_xml

HOME_ROOT = "https://domainku.tld"


class Wpxr(Export):

    def execute(self, data: dict) -> None:
        print('Memproses...')
        html = data['html']

        # FILENAME = "output/wp.xml"
        filename = os.path.join(data['path'], 'wp.xml')
        # Creates the <rss> root node
        root = create_root_node()
        # Creates the <channel> node and fills the website's information
        channel = create_channel_node(root, 'My awesome website', HOME_ROOT, 'id_ID')

        # todo loop
        # Adding a picture
        # logo_url = "https://domain.tld/path/to/picture.jpg"
        # logo_item = create_item_node(
        #         parent=channel,
        #         post_id="{0}".format(10),
        #         title="logo",
        #         link=logo_url,
        #         post_name="logo",
        #         status="publish",
        #         post_type="attachment",
        #         date=date_local,
        #         date_gmt=date_gmt)
        #
        # logo_path = "{0}/{1}/{2}".format('2020', '04', "picture")
        # create_text_node(logo_item, WP + "attachment_url", CDATA(logo_url))
        # create_post_meta_node(logo_item, "_wp_attached_file", logo_path)
        # guid = ET.SubElement(logo_item, "guid", isPermalink="false")
        # guid.text = logo_url

        # todo loop
        # Adding a post
        for content in html:
            date = parser.parse(content['Creation time:'], tzinfos={"PDT": "UTC-7"})
            date_local = date.astimezone(tzoffset('WIB', 7 * 3600)).strftime('%Y-%m-%d %H:%M:%S')
            date_gmt = date.astimezone(tzoffset(None, 0)).strftime('%Y-%m-%d %H:%M:%S')
            slug = "my-article" # todo
            item = create_item_node(
                    parent=channel,
                    post_id="{0}".format(11),
                    title=content['Question:'],
                    link="{0}/{1}".format(HOME_ROOT, slug),
                    post_name=slug,
                    status="draft",
                    post_type="post",
                    date=date_local,
                    date_gmt=date_gmt)
            artikel = ''
            for konten in content['Content:']:
                artikel += str(konten)

            create_text_node(item, CONTENT + "encoded", CDATA(artikel))
            # create_text_node(item, EXCERPT + "encoded", CDATA("<p>Article excerpt</p>")) # todo trim subset

        # todo loop
        # Adding a category to the post
        # NB: you can add more than one category
        # cat_node = ET.SubElement(item, 'category')
        # cat_node.set("domain", "category")
        # cat_node.set("nicename", "category-slug")
        # cat_node.text = CDATA("Category name")

        # todo loop
        # Adding a tag to the post
        # NB: you can add more than one tag
        # cat_node = ET.SubElement(item, 'category')
        # cat_node.set("domain", "post-tag")
        # cat_node.set("nicename", "tag-slug")
        # cat_node.text = CDATA("Tag name")

        # Add the picture as thumbnail
        # create_post_meta_node(item, "_thumbnail_id", "{0}".format(10))

        # Save files
        write_xml(root, filename)
