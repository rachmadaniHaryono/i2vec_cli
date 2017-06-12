"""test main."""


def test_convert_raw_to_hyrus():
    """test."""
    raw_input = [
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
    ]
    exp_output = [
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
    from i2vec_cli.__main__ import convert_raw_to_hydrus
    result = convert_raw_to_hydrus(raw_input)
    assert result == '\n'.join(exp_output)
