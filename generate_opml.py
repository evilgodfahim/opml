import csv
import sys
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def channel_id_to_rss(channel_id):
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

def generate_opml(input_csv, output_opml):
    channel_ids = []

    with open(input_csv, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                channel_id = row[0].strip()
                # Skip header row if present
                if channel_id.lower() == "channel id":
                    continue
                if channel_id:
                    channel_ids.append(channel_id)

    # Build OPML XML
    opml = Element('opml', version='2.0')

    head = SubElement(opml, 'head')
    title = SubElement(head, 'title')
    title.text = 'YouTube RSS Feeds'
    date_created = SubElement(head, 'dateCreated')
    date_created.text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    body = SubElement(opml, 'body')
    outline_group = SubElement(body, 'outline', text='YouTube Channels', title='YouTube Channels')

    for channel_id in channel_ids:
        rss_url = channel_id_to_rss(channel_id)
        feed_title = f"YouTube: {channel_id}"
        SubElement(outline_group, 'outline',
                   type='rss',
                   text=feed_title,
                   title=feed_title,
                   xmlUrl=rss_url,
                   htmlUrl=f"https://www.youtube.com/channel/{channel_id}")

    # Pretty print
    xml_str = minidom.parseString(tostring(opml, encoding='unicode')).toprettyxml(indent='  ')
    # Remove extra xml declaration added by toprettyxml
    lines = xml_str.split('\n')
    if lines[0].startswith('<?xml'):
        lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_str = '\n'.join(lines)

    with open(output_opml, 'w', encoding='utf-8') as f:
        f.write(xml_str)

    print(f"✅ Generated OPML with {len(channel_ids)} channels → {output_opml}")

if __name__ == '__main__':
    input_csv = sys.argv[1] if len(sys.argv) > 1 else 'subscriptions.csv'
    output_opml = sys.argv[2] if len(sys.argv) > 2 else 'youtube_feeds.opml'
    generate_opml(input_csv, output_opml)
