"""test module."""
from i2vec_cli.server import convert_raw_to_flask_template

def test_convert_raw_to_hydrus(example_json_resp):
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
    res = convert_raw_to_flask_template(example_json_resp)
    assert len(res) == len(exp_res)
    for item in exp_res:
        assert item in res
