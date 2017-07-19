"""test module."""
from i2vec_cli.requests_session import convert_raw_to_hydrus


def test_convert_raw_to_hydrus(example_json_resp):
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
    res = convert_raw_to_hydrus(example_json_resp)
    assert res == exp_res
