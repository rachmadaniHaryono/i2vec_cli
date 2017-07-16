"""test module."""

from i2vec_cli.server import convert_raw_to_flask_template

def test_convert_raw_to_hydrus():
    raw_input = {
        'height': 500,
        'prediction': {
            'character': [],
            'copyright': [],
            'general': [
                ['1girl', 0.9456192255020142],
                ['monochrome', 0.8776167035102844],
                ['breasts', 0.8765498399734497],
                ['solo', 0.7575669288635254],
                ['nipples', 0.51136714220047],
                ['hat', 0.5044781565666199],
                ['large breasts', 0.2942590117454529],
                ['shirt lift', 0.18467438220977783]
            ],
            'rating': [
                ['questionable', 0.5886136293411255],
                ['explicit', 0.21928244829177856],
                ['safe', 0.0848841667175293]
            ]
        },
        'size': 17383,
        'url': 'static/uploads/dB3KpWCpLf.png',
        'width': 500
    }
    exp_res = [
        {'class': 'tag-type-general', 'text': 'rating:questionable'},
        {'class': 'tag-type-general', 'text': '1girl'},
        {'class': 'tag-type-general', 'text': 'monochrome'},
        {'class': 'tag-type-general', 'text': 'breasts'},
        {'class': 'tag-type-general', 'text': 'solo'},
        {'class': 'tag-type-general', 'text': 'nipples'},
        {'class': 'tag-type-general', 'text': 'hat'},
        {'class': 'tag-type-general', 'text': 'large breasts'},
        {'class': 'tag-type-general', 'text': 'shirt lift'}
    ]
    res = convert_raw_to_flask_template(raw_input)
    assert len(res) == len(exp_res)
    for item in exp_res:
        assert item in res
