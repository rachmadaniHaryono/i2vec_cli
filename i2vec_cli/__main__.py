#!/usr/bin/env python3
"""get tag from http://demo.illustration2vec.net/."""
# note:
# - error 'ERROR: Request Entity Too Large' for file 1.1 mb
# <span style="color:red;">ERROR: Request Entity Too Large</span>
from pprint import pprint
import os

import click
import selenium
from splinter import Browser
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
            self.log.error('Error', e=e)
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


@click.command()
@click.argument('path', nargs=-1)
def main(path):
    """get tag from illustration2vec."""
    session = Session()
    try:
        for p in path:
            print('path:{}'.format(os.path.basename(p)))
            tags = session.get_tags(path=p)
            pprint(tags)
    finally:
        session.browser.quit()


if __name__ == '__main__':
    main()
