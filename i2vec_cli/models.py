import inspect
import os

from peewee import *
import peewee

from i2vec_cli.utils import user_data_dir, thumb_folder


database = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class Image(BaseModel):
    sha256 = CharField(unique=True)
    md5 = CharField()

    @property
    def thumb_filename(self):
        return '{}.jpg'.format(self.sha256)

    @property
    def thumb_exist(self):
        thumb_path = os.path.join(thumb_folder, thumb_filename)
        if os.path.isfile(thumb_path):
            return True
        return False


class TagRelationship(BaseModel):
    image = ForeignKeyField(Image, related_name='tags')
    name = CharField()
    confidence = FloatField()
    group = CharField()


def save_result(db, sha256, md5, prediction):
    database.init(db)
    im = Image(sha256=sha256, md5=md5)
    im.save()
    for group in prediction:
        for tag_set in prediction[group]:
            tr = TagRelationship(image=im, name=tag_set[0], confidence=tag_set[1], group=group)
            tr.save()


def load_result(db, sha256=None, md5=None):
    if sha256 is None and md5 is None:
        raise ValueError('At lease one checksum required.')
    database.init(db)
    sha256_res = {}
    md5_res = {}
    if sha256 is not None:
        im = Image.get(Image.sha256==sha256)
        tags = [x for x in im.tags]
        for tag in tags:
            sha256_res.setdefault(tag.group, []).append([tag.name, tag.confidence])
        if md5 is None:
            return sha256_res
    if md5 is not None:
        im = Image.get(Image.md5==md5)
        tags = [x for x in im.tags]
        for tag in tags:
            md5_res.setdefault(tag.group, []).append([tag.name, tag.confidence])
        if sha256 is None:
            return md5_res
    if sha256 is not None and md5 is not None and md5_res != sha256_res:
        raise ValueError('Mismatch sha256 and md5checksum')
    elif sha256 is not None and md5 is not None and md5_res == sha256_res:
        return sha256_res
    else:
        raise ValueError('Unknown condition')


def init_all_tables():
    peewee.create_model_tables([Image, TagRelationship])
