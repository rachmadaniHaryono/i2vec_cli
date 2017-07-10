from html_table_parser import HTMLTableParser
from splinter import Browser
import selenium
import structlog


def dump_html_to_file(html):
    """dump html."""
    filename = '{}.html'.format(time.strftime("%Y%m%d-%H%M%S"))
    with open(filename, 'w') as ff:
        ff.write(html)
    print('HTML table dumped: {}'.format(filename))


def convert_tag_dict_to_string(dict_input):
    """convert tag dict to string."""
    # compatibility
    dict_result = dict_input

    log = structlog.getLogger()

    for key in dict_result:
        if key == 'Character Tag':
            tag = '\n'.join(['character:{}'.format(x) for x in dict_result[key]]).strip()
            if not tag:
                continue
            yield tag
        elif key == 'Copyright Tag':
            tag = '\n'.join(['series:{}'.format(x) for x in dict_result[key]]).strip()
            if not tag:
                continue
            yield tag
        elif key == 'Rating':
            if dict_result[key]:
                tag = 'rating:{}'.format(dict_result[key][0]).strip()
                yield tag
            else:
                log.debug('Rating tag', v=dict_result[key])
        else:
            if key != 'General Tag':
                # log unknown key
                log.debug('Unknown key', v=key)
            tag = '\n'.join([x for x in dict_result[key]]).strip()
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


class Session:
    """session."""

    def __init__(self, driver=None):
        """init."""
        self.log = structlog.getLogger()
        driver = [] if driver is None else [driver]
        try:
            self.browser = Browser(*driver)
        except OSError as e:
            self.log.debug('Expected init browser error', e=e)
            self.browser = Browser(*driver)
        self.browser.visit('http://demo.illustration2vec.net/')

    def get_tags(self, path, dump_html=False):
        """get tags."""
        input_tags = self.browser.find_by_xpath("//input[contains(@id, 'ajax-upload-id')]")
        real_path = os.path.realpath(path)
        try:
            input_tags[0].type(real_path)
        except selenium.common.exceptions.ElementNotVisibleException as e:
            self.log.error('Error', e=e)
            if len(input_tags) > 1:
                input_tags[1].type(real_path)
            else:
                self.log.error('Input tag not found.')
        bb_tag = self.browser.find_by_css('.box-body')[1]
        if dump_html:
            dump_html_to_file(bb_tag.html)
        p = HTMLTableParser()
        p.feed(bb_tag.html.strip())
        return p.tables

    def get_hydrus_tags(self, path, dump_html=False):
        tags = self.get_hydrus_tags(path=path, dump_html=dump_html_to_file)
        return convert_raw_to_hydrus(tags)
