#!/usr/bin/env python3
"""get tag from http://demo.illustration2vec.net/."""
# note:
# - error 'ERROR: Request Entity Too Large' for file 1.1 mb
# <span style="color:red;">ERROR: Request Entity Too Large</span>
from collections import OrderedDict
from pprint import pprint
import logging
import os

from splinter import Browser
import click
import selenium
import structlog

from html_table_parser import HTMLTableParser


class Session:
    """session."""

    def __init__(self):
        """init."""
        self.log = structlog.getLogger()
        try:
            self.browser = Browser()
        except OSError as e:
            self.log.debug('Expected init browser error', e=e)
            self.browser = Browser()
        self.browser.visit('http://demo.illustration2vec.net/')

    def get_tags(self, path):
        """get tags."""
        input_tags = self.browser.find_by_xpath("//input[contains(@id, 'ajax-upload-id')]")
        try:
            input_tags[0].type(path)
        except selenium.common.exceptions.ElementNotVisibleException as e:
            self.log.error('Error', e=e)
            input_tags[1].type(path)
        bb_tag = self.browser.find_by_css('.box-body')[1]
        p = HTMLTableParser()
        p.feed(bb_tag.html.strip())
        return p.tables


def convert_tag_dict_to_string(dict_input):
    """convert tag dict to string."""
    # compatibility
    dict_result = dict_input

    log = structlog.getLogger()

    for key in dict_result:
        if key == 'Character Tag':
            tag = '\n'.join(['character:{}'.format(x) for x in dict_result[key]])
            if not tag:
                continue
            yield tag
        elif key == 'Copyright Tag':
            tag = '\n'.join(['series:{}'.format(x) for x in dict_result[key]])
            if not tag:
                continue
            yield tag
        elif key == 'Rating':
            if dict_result[key]:
                tag = 'rating:{}'.format(dict_result[key][0])
                yield tag
            else:
                log.debug('Rating tag', v=dict_result[key])
        else:
            if key != 'General Tag':
                # log unknown key
                log.debug('Unknown key', v=key)
            tag = '\n'.join([x for x in dict_result[key]])
            if not tag:
                continue
            yield tag


def convert_raw_to_hydrus(raw_input):
    """convert raw format to hydrus format."""
    # convert list to dict with category as key.
    dict_result = OrderedDict()
    for table in raw_input:
        row_text = []
        for row in table[1:]:
            row_text.append(row[1])
        dict_result[table[0][1]] = row_text

    result = list(convert_tag_dict_to_string(dict_result))

    return '\n'.join(result).strip()


@click.command()
@click.option('--format', type=click.Choice(['raw', 'hydrus']), default='raw')
@click.option('-d', '--debug', is_flag=True, help="Enable debug.")
@click.argument('path', nargs=-1)
def main(format, path, debug):
    """get tag from illustration2vec."""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    structlog.configure_once(logger_factory=structlog.stdlib.LoggerFactory())
    log = structlog.getLogger()

    session = Session()
    try:
        for p in path:
            print('path:{}'.format(os.path.basename(p)))
            tags = session.get_tags(path=p)
            log.debug('tags', v=tags)
            if format == 'hydrus':
                res = convert_raw_to_hydrus(tags)
                print(res)
            else:
                pprint(tags)
    finally:
        session.browser.quit()


if __name__ == '__main__':
    main()
