"""test module."""

from i2vec_cli.requests_session import convert_raw_to_hydrus

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
        '1girl',
        'monochrome',
        'breasts',
        'solo',
        'nipples',
        'hat',
        'large breasts',
        'shirt lift',
        'rating:questionable',
    ]
    exp_res = '\n'.join(sorted(exp_res))
    res = convert_raw_to_hydrus(raw_input)
    assert res == exp_res
