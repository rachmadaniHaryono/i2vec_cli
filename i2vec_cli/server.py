import os
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
)
from send2trash import send2trash

from i2vec_cli.requests_session import Session
from i2vec_cli.__main__ import get_print_result
from i2vec_cli.utils import user_data_dir, thumb_folder
from i2vec_cli import models


app = Flask(__name__)


def convert_raw_to_flask_template(raw_input):
    """convert raw tags into better flask template tags."""
    prediction = raw_input['prediction']
    result = []
    for key in prediction:
        namespace = 'tag-type-general'
        if key == 'character':
            namespace = 'tag-type-character'
        elif key == 'copyright':
            namespace = 'tag-type-copyright'
        elif key == 'general':
            pass
        elif key == 'rating':
            text = 'rating:{}'.format(prediction['rating'][0][0])
            result.append({'class': namespace, 'text': text})
            continue
        else:
            log.debug('Unknown key', key=key)
        if not prediction[key]:
            continue
        for item, _ in prediction[key]:
            result.append({'class': namespace, 'text': item})
    return result


@app.route('/upload', methods=['POST'])
def upload_file():
    db_path = os.path.join(user_data_dir, 'main.db')
    models.database.init(db_path)
    session = Session()
    path = request.files['file']
    path.save(path.filename)
    tags = get_print_result(
        path=path.filename, db_path=db_path, format='dict', session=session)
    entries = convert_raw_to_flask_template(tags)
    send2trash(path.filename)
    return render_template('upload_result.html', entries=entries)


@app.route('/')
def index():
    db_path = os.path.join(user_data_dir, 'main.db')
    models.database.init(db_path)
    img_matches = [x for x in models.Image.select()]
    return render_template('index.html', entries=img_matches)


@app.route('/thumb/<path:filename>')
def thumbnail(filename):
    return send_from_directory(thumb_folder, filename)


def main():
    """main."""
    app.run()


if __name__ == '__main__':
    main()
