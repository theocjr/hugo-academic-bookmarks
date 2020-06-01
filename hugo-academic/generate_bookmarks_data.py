#!/usr/bin/env python3


"""
Auxiliar code used to generate JSON file from YAML file to be consumed by Go
templates. Run this code before the static content generation by hugo binary.

Run instructions:
    ./generate_bookmarks_data.py \
        --bookmarks_filename data/bookmarks.yaml \
        --bookmarks_by_tags_filename data/bookmarks_by_tags.json \
        --tags_directory content/bookmarks/tags/
"""


import argparse
import logging
import os
import yaml
import unicodedata
import json
import glob
import time


def command_line_parsing():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('--bookmarks_filename', '-b',
                        required=True,
                        help='Filename with bookmarks (YAML format).')
    parser.add_argument('--bookmarks_by_tags_filename', '-t',
                        required=True,
                        help='Filename to output bookmarks by tags mapping (JSON format).')
    parser.add_argument('--tags_directory',
                        required=True,
                        help='Directory to output Markdown tag files.')
    parser.add_argument('--debug', '-d',
                        action='store_true',
                        default=False,
                        help='Print debug information.')
    return parser.parse_args()


if __name__ == '__main__':
    # parsing arguments
    args = command_line_parsing()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')

    with open(args.bookmarks_filename, mode='rt', encoding='utf-8') as fd:
        bookmarks = yaml.load(fd, Loader=yaml.FullLoader)

    url_set = set()
    for bookmark in bookmarks:
        if bookmark['url'] in url_set:
            logging.warning('Repeated bookmark:\n{}'.format(bookmark))
        else:
            url_set.add(bookmark['url'])

    bookmarks_by_tags = {}
    for bookmark in bookmarks:
        bookmark['tags'].sort()
        for tag in bookmark['tags']:
            if tag not in bookmarks_by_tags:
                safe_name = tag.replace(' ', '_')
                safe_name = unicodedata.normalize('NFD', safe_name).encode('ascii', 'ignore').decode('utf-8')
                bookmarks_by_tags[tag] = { 'name': tag,
                                           'safe_name': safe_name,
                                           'bookmarks': [ bookmark ],
                                         }
            else:
                bookmarks_by_tags[tag]['bookmarks'].append(bookmark)
    with open(args.bookmarks_by_tags_filename, mode='wt', encoding='utf-8') as fd:
        json.dump(bookmarks_by_tags, fd, sort_keys=True)

    md_filenames = glob.glob(os.path.join(args.tags_directory, '*.md'))
    for md_filename in md_filenames:
        os.remove(md_filename)
    md_content = { 'layout': 'tag', 'date': time.strftime("%Y-%m-%d") }
    for tag in bookmarks_by_tags:
        md_content['title'] = 'Bookmarks for tag {}'.format(tag)
        md_content['name'] = tag
        with open(os.path.join(args.tags_directory, '{}.md'.format(bookmarks_by_tags[tag]['safe_name'])), mode='wt', encoding='ascii') as fd:
            fd.write('---\n')
            yaml.dump(md_content, fd)
            fd.write('---\n')

