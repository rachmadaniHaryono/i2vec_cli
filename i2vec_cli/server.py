from flask import (
    Flask,
    render_template,
    request,
)

from i2vec_cli.requests_session import Session


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
    session = Session()
    path = request.files['file']
    path.save(path.filename)
    tags = session.get_tags(path=path.filename)
    entries = convert_raw_to_flask_template(tags)
    return render_template('upload_result.html', entries=entries)


def main():
    """main."""
    app.run()


if __name__ == '__main__':
    main()
