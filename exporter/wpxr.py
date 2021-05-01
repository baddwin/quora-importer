import os

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

BASE_URL = 'https://id.quora.com'


class Wpxr(Export):

    def execute(self, data: dict) -> None:
        print('Memproses...')
        html = data['html']

        # FILENAME = "output/wp.xml"
        filename = os.path.join(data['path'], 'wp.xml')  # todo name with timestamp
        # Creates the <rss> root node
        root = create_root_node()
        # Creates the <channel> node and fills the website's information
        channel = create_channel_node(root, 'My Posts from Quora', BASE_URL, 'id_ID')

        # todo loop
        # Adding a picture
        post_id = 1
        for images in html['images']:
            date = parser.parse(images['date'], tzinfos={"PDT": "UTC-7"})
            date_local = date.astimezone(tzoffset('WIB', 7 * 3600))  # todo choice
            date_gmt = date.astimezone(tzoffset(None, 0)).strftime('%Y-%m-%d %H:%M:%S')
            img_url = images['url']
            img_item = create_item_node(
                    parent=channel,
                    post_id="{0}".format(post_id),
                    title=images['name'],
                    link=img_url,
                    post_name=images['name'],
                    status="publish",
                    post_type="attachment",
                    date=date_local.strftime('%Y-%m-%d %H:%M:%S'),
                    date_gmt=date_gmt)

            # logo_path = "{0}/{1}/{2}".format('2020', '04', "picture")
            img_path = "{0}/{1}/{2}".format(date_local.year, date_local.month, images['name'])
            create_text_node(img_item, WP + "attachment_url", CDATA(img_url))
            create_post_meta_node(img_item, "_wp_attached_file", img_path)
            guid = ET.SubElement(img_item, "guid", isPermalink="true")
            guid.text = img_url
            post_id += 1

        # Adding a post
        # post_id = 1
        for content in html['html']:
            date = parser.parse(content['Creation time'], tzinfos={"PDT": "UTC-7"})
            date_local = date.astimezone(tzoffset('WIB', 7 * 3600)).strftime('%Y-%m-%d %H:%M:%S')  # todo choice
            date_gmt = date.astimezone(tzoffset(None, 0)).strftime('%Y-%m-%d %H:%M:%S')
            # slug = slugify(content['Question'], lowercase=False)
            slug = super().get_slug(content['Question'])
            item = create_item_node(
                    parent=channel,
                    post_id="{0}".format(post_id),
                    title=content['Question'],
                    link="{0}/{1}".format(BASE_URL, slug),
                    post_name=slug,
                    status="pending",
                    post_type="post",
                    date=date_local,
                    date_gmt=date_gmt)
            artikel, excerpt = '', ''
            for konten in content['Content']:
                artikel += str(konten)
                if not excerpt:
                    excerpt = konten.text

            create_text_node(item, CONTENT + "encoded", CDATA(artikel))
            create_text_node(item, EXCERPT + "encoded", CDATA(excerpt))
            post_id += 1

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
