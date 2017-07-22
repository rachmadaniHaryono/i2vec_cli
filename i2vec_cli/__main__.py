#!/usr/bin/env python3
"""get tag from http://demo.illustration2vec.net/."""
# note:
# - error 'ERROR: Request Entity Too Large' for file 1.1 mb
# <span style="color:red;">ERROR: Request Entity Too Large</span>
from collections import OrderedDict
from pathlib import Path
from pprint import pformat
import imghdr
import logging
import os
import shutil
import time
import urllib
import hashlib

import click
import requests
import structlog
import peewee
from PIL import Image

from i2vec_cli import models
from i2vec_cli.requests_session import Session, convert_raw_to_hydrus
from i2vec_cli.sha256 import sha256_checksum
from i2vec_cli.utils import user_data_dir, thumb_folder


def is_url(path):
    """Return True if path is url, False otherwise."""
    scheme = urllib.parse.urlparse(path).scheme
    if scheme in ('http', 'https'):
        return True
    return False


def is_ext_equal(file_ext, imghdr_ext):
    """compare file extension with result from imghdr_ext."""
    if not imghdr_ext:
        return False
    if file_ext.lower() == '.{}'.format(imghdr_ext):
        return True
    if file_ext.lower() in ('.jpg', '.jpeg') and imghdr_ext == 'jpeg':
        return True
    return False


def download(url, no_clobber):
    """download url.

    Args:
        url: URL to be downloaded.
        no_clobber: Skip download if file already exist.

    Returns:
        Downloaded filename or existing file if `no_clobber` is `True`
    """
    log = structlog.getLogger()

    basename = os.path.basename(url)
    if os.path.isfile(basename) and no_clobber:
        return basename

    response = requests.get(url, stream=True)
    with open(basename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    name, ext = os.path.splitext(basename)
    imghdr_ext = imghdr.what(basename)
    ext_equal = is_ext_equal(file_ext=ext, imghdr_ext=imghdr_ext)

    if not imghdr_ext:
        log.debug("imghdr can't recognize file", file=basename)
        return basename
    else:
        new_basename = '{}.{}'.format(name, imghdr_ext)
        new_basename_exist = os.path.isfile(new_basename)

    if ext_equal:
        log.debug('Extension is equal', file_ext=ext, imghdr_ext=imghdr_ext)
        return basename
    elif not ext_equal:
        if new_basename_exist and not no_clobber:
            log.debug('Replace existing file', old=basename, new=new_basename)
            shutil.move(basename, new_basename)
        elif not new_basename_exist:
            log.debug('Rename file ext', file=basename, new_ext=imghdr_ext)
            shutil.move(basename, new_basename)
        else:
            log.debug('Not replace/rename file', no_clobber=no_clobber, new_basename=new_basename)
        return new_basename
    else:
        log.debug(
            'Unknown condition',
            file=basename,
            ext_equal=ext_equal,
            new_basename_exist=new_basename_exist,
            imghdr_ext=imghdr_ext
        )
    # just return base name if any error happen
    return basename


def validate_close_delay(ctx, param, value):
    """validate close delay."""
    try:
        value = int(value)
    except Exception as e:
        raise click.BadParameter(
            'Error when validate close delay: value={}, error={}'.format(value, e))
    if value >= -1:
        return value
    else:
        raise click.BadParameter('Close delay have to be bigger or equal than -1')


def delay_close(close_delay):
    """delay when closing the program."""
    log = structlog.getLogger()
    if close_delay == -1:
        click.pause()
    elif close_delay == 0:
        log.debug('No close delay')
    elif close_delay > 0:
        time.sleep(close_delay)
    else:
        log.error('Invalid close delay', v=close_delay)


def md5_checksum(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def create_thumbnail(path, thumb_path):
    """create thumbnail."""
    size = 320, 320
    try:
        im = Image.open(path)
        im.thumbnail(size)
        im.save(thumb_path, "JPEG")
    except IOError:
        raise IOError("cannot create thumbnail for", path)


def get_print_result(path, db_path, format, session):
    """get print result."""
    # compatibility
    p = path

    sha256 = sha256_checksum(p)
    md5 = md5_checksum(p)
    thumb_path = os.path.join(user_data_dir, 'thumb', '{}.jpg'.format(sha256))
    try:
        load_res = models.load_result(db=db_path, sha256=sha256, md5=md5)
    except models.Image.DoesNotExist:
        load_res = None
    if load_res:
        tags = {'prediction': load_res}
    else:
        tags = session.get_tags(path=p)
        try:
            models.save_result(
                db=db_path, sha256=sha256, md5=md5, prediction=tags['prediction'])
        except peewee.IntegrityError as e:
            log.debug(str(e))
        except keyError as e:
            log.debug(str(tags))
    if not os.path.isfile(thumb_path):
        create_thumbnail(p, thumb_path)

    if format == 'dict':
        return tags
    if format == 'hydrus':
        return convert_raw_to_hydrus(tags)
    else:
        return pformat(tags['prediction'])


@click.command()
@click.option('--format', type=click.Choice(['raw', 'hydrus']), default='raw')
@click.option('-d', '--debug', is_flag=True, help="Enable debug.")
@click.option('-nc', '--no-clobber', is_flag=True, help="Skip download url when file exist.")
@click.option(
    '--close-delay', default=0, help="Close delay of the program.", callback=validate_close_delay)
@click.option(
    '--driver', default=None, help="Driver for browser (deprecated).",
    type=click.Choice(['firefox', 'phantomjs', 'chrome', 'zope.testbrowser', 'django']))
@click.option('--dump-html', is_flag=True, help="Dump html table for debugging (deprecated).")
@click.argument('path', nargs=-1)
def main(format, path, debug, no_clobber, close_delay, driver=None, dump_html=False):
    """get tag from illustration2vec."""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    structlog.configure_once(logger_factory=structlog.stdlib.LoggerFactory())
    log = structlog.getLogger()

    if not path:
        raise ValueError('PATH required.')

    # init folder
    os.makedirs(user_data_dir, exist_ok=True)
    os.makedirs(thumb_folder, exist_ok=True)

    # database
    db_path = os.path.join(user_data_dir, 'main.db')
    if not os.path.isfile(db_path):
        Path(db_path).touch()
    models.database.init(db_path)
    try:
        models.init_all_tables()
    except peewee.OperationalError:
        log.debug('Table already created')

    session = Session(driver=driver)
    try:
        for p in path:
            if os.path.isfile(p):
                print('path:{}'.format(os.path.basename(p)))
            elif is_url(p):
                print('url:{}'.format(p))
                p = download(p, no_clobber=no_clobber)
            else:
                log.error('Unknown path format or path is not exist', path=p)
                continue
            result = get_print_result(
                path=p, db_path=db_path, format=format, session=session)
            print(result)
    finally:
        delay_close(close_delay)
        if hasattr(session, 'browser'):
            session.browser.quit()


if __name__ == '__main__':
    main()
