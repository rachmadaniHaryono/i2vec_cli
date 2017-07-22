import os

from appdirs import user_data_dir

user_data_dir = user_data_dir('i2vec_cli', 'rachmadaniHaryono')
thumb_folder = os.path.join(user_data_dir, 'thumb')
