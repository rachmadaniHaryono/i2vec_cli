"""test main."""
import pytest

@pytest.mark.skip(reason="splinter is not used anymore")
@pytest.mark.parametrize("raw_input, exp_output", [
    (
        [
            [
                ['#', 'General Tag', 'Confidence', ''],
                ['1.', 'chibi', '', '78.5%'],
                ['2.', 'no humans', '', '37.5%'],
                ['3.', 'cat ears', '', '29.6%'],
            ],
            [
                ['#', 'Character Tag', '', ''],
                ['1.', 'gilgamesh', '', '56.0%'],
                ['2.', 'beatrice', '', '40.8%'],
                ['3.', 'kotomine kirei', '', '24.8%']
            ],
            [
                ['#', 'Copyright Tag', '', ''],
                ['1.', 'fate (series)', '', '80.1%'],
                ['2.', 'fate/zero', '', '65.8%'],
                ['3.', 'umineko no naku koro ni', '', '24.6%'],
                ['4.', 'disney', '', '0.686%']],
            [
                ['#', 'Rating', '', ''],
                ['1.', 'safe', '', '93.6%'],
                ['2.', 'questionable', '', '4.74%']
            ]
        ],
        [
            'chibi',
            'no humans',
            'cat ears',
            'character:gilgamesh',
            'character:beatrice',
            'character:kotomine kirei',
            'series:fate (series)',
            'series:fate/zero',
            'series:umineko no naku koro ni',
            'series:disney',
            'rating:safe',
        ]
    ),
    (
        [
            [['#', 'General Tag', 'Confidence', '']],
            [['#', 'Character Tag', '', '']],
            [['#', 'Copyright Tag', '', '']],
            [['#', 'Rating', '', '']]
        ],
        []
    ),
])
def test_convert_raw_to_hyrus(raw_input, exp_output):
    """test."""
    from i2vec_cli.splinter_session import convert_raw_to_hydrus
    result = convert_raw_to_hydrus(raw_input)
    assert result == '\n'.join(exp_output)


@pytest.mark.parametrize('file_ext, imghdr_ext, exp_output', (
    ('.jpg', 'jpeg', True),
    ('.jpeg', 'jpeg', True),
    ('.JPEG', 'jpeg', True),
    ('.PNG', 'png', True),
    ('.png', 'png', True),
    ('.png', 'jpeg', False),
    ('.png', None, False),
))
def test_is_ext_equal(file_ext, imghdr_ext, exp_output):
    """test."""
    from i2vec_cli.__main__ import is_ext_equal
    assert exp_output == is_ext_equal(file_ext, imghdr_ext)
