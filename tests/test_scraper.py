from bs4 import BeautifulSoup
import pytest
from scraper import abc_scraper
import responses
import json
from requests.exceptions import HTTPError

@pytest.fixture
def mock_endpoints():
    res = responses.RequestsMock()
    res.start()
    return res

@pytest.fixture
def example_article_list():
    with open('tests/example_article_list.json', 'r') as infile:
        data = json.load(infile)
        return data

@pytest.fixture
def example_article_from_list(example_article_list):
    return example_article_list['collection'][0]  

@pytest.fixture
def example_article_from_list2(example_article_list):
    return example_article_list['collection'][1]  

@pytest.fixture
def example_article():
    with open('tests/example_article.html', 'r') as infile:
        data = json.load(infile)
        return data

def test_get_article_list_success(mock_endpoints, example_article_list):
    mock_endpoints.add(responses.GET, f"https://www.abc.net.au/news-web/api/loader/justinstories", json=example_article_list, status=200)
    r = abc_scraper.get_list_articles()
    assert mock_endpoints.calls[0].request.params == {"offset": "0", "size": "25", "total": "250"}

def test_get_article_success(mock_endpoints):
    mock_endpoints.add(responses.GET, f"https://www.abc.net.au/news/2022-04-29/un-chief-condemns-ukraine-attack/101026522", status=200)
    soup = abc_scraper.get_article_soup("/news/2022-04-29/un-chief-condemns-ukraine-attack/101026522")
    assert isinstance(soup, BeautifulSoup)

def test_get_article_fail(mock_endpoints):
    mock_endpoints.add(responses.GET, f"https://www.abc.net.au/news/2022-04-29/un-chief-condemns-ukraine-attack/101026522", status=404)
    with pytest.raises(HTTPError) as r_error:
        r = abc_scraper.get_article_soup("/news/2022-04-29/un-chief-condemns-ukraine-attack/101026522")

def test_parse_article_list(example_article_list):
    articles = abc_scraper.parse_article_list(example_article_list)
    assert isinstance(articles, list)

def test_parse_article(example_article_from_list):
    clean_article = abc_scraper.clean_article(example_article_from_list)
    assert list(clean_article.keys()) == ["title", "link", "author", "description", "published", "last_updated"]
    assert clean_article == {
        "title": "US seeks $4 million from former Trump campaign director Paul Manafort",
        "link": "/news/2022-04-29/us-seeks-4-million-from-former-donald-trump-campaign-director-/101026626",
        "author": None,
        "description": "Prosecutors say Paul Manafort failed to disclose more than 20 offshore bank accounts he ordered opened in the United Kingdom, Cyprus, St Vincent and the Grenadines.",
        "published": "2022-04-29T05:45:22+00:00",
        "last_updated": None
    }
    
def test_get_title(example_article_from_list):
    assert abc_scraper.get_title(example_article_from_list) == "US seeks $4 million from former Trump campaign director Paul Manafort"

def test_get_link(example_article_from_list):
    assert abc_scraper.get_link(example_article_from_list) == "/news/2022-04-29/us-seeks-4-million-from-former-donald-trump-campaign-director-/101026626"

def test_get_description(example_article_from_list):
    assert abc_scraper.get_description(example_article_from_list) == "Prosecutors say Paul Manafort failed to disclose more than 20 offshore bank accounts he ordered opened in the United Kingdom, Cyprus, St Vincent and the Grenadines."

def test_get_first_published(example_article_from_list):
    assert abc_scraper.get_published(example_article_from_list) == "2022-04-29T05:45:22+00:00"

def test_get_last_updated(example_article_from_list, example_article_from_list2):
    assert abc_scraper.get_last_updated(example_article_from_list) == None
    assert abc_scraper.get_last_updated(example_article_from_list2) == "2022-04-29T05:46:57+00:00"

def test_get_authors(example_article_from_list, example_article_from_list2):
    assert abc_scraper.get_authors(example_article_from_list) == None
    assert abc_scraper.get_authors(example_article_from_list2) == ["Luke Radford", "Warwick Long"]

