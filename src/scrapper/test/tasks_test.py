from unittest import mock
from unittest.mock import PropertyMock

import pytest

from scrapper import Link
from scrapper import scrappe_url

@mock.patch("requests.get")
@pytest.mark.parametrize(
    "test_input, expected",
    [("google.com","http://google.com"), ("http://google.com", "http://google.com")]
)
def test_scrappe_url(mock_request, test_input, expected,client):

    type(mock_request.return_value).status_code = PropertyMock(return_value=200)
    print(type(mock_request.return_value))
    with open("test/abc.html", "r") as html:
        mock_html=html.read()

    type(mock_request.return_value).text = PropertyMock(return_value=mock_html)

    scrappe_url(url=test_input)
    mock_request.assert_called_once_with(expected)
    # with app.app_context():
    record=Link.query.first()
    if  record is None:
        raise RuntimeError("unable to find first record")
    else:
        assert record.link == "http://www.interia.pl"

