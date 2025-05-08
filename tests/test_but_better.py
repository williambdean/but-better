import pytest

import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from but_better import parse_youtube_url, is_url


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://www.youtube.com/watch?v=abcdefg", "abcdefg"),
        ("https://www.youtube.com/watch?v=abcdefg&list=abc&index=3", "abcdefg"),
    ],
)
def test_parse_youtube_url(url, expected):
    assert parse_youtube_url(url) == expected


@pytest.mark.parametrize(
    "value",
    [
        "https://www.youtube.com/watch?v=abcdefg",
        "http://www.youtube.com/watch?v=abcdefg",
    ],
)
def test_is_url_matches(value):
    assert is_url(value)


@pytest.mark.parametrize(
    "value",
    [
        "not_a_url",
        "abcdefg",
        "<your-youtube-id>",
    ],
)
def test_is_url_does_not_match(value):
    assert not is_url(value)
