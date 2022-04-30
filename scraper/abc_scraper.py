import requests
import bs4
import json

def get_list_articles(offset: int = 0, size: int = 25, total: int = 250):
    """Get's a JSON document containing a collection of the articles on the "just in" page of the ABC website. 

    Args:
        offset (int, optional): Moves the "size" cursor by 1 through the total list of articles. Defaults to 0.
        size (int, optional): How many articles are returned in the JSON payload. Defaults to 25.
        total (int, optional): How many articles are queried for. Defaults to 250.

    Returns:
        JSON : The raw JSON response of the article
    """
    payload = {
        "offset": offset,
        "size": size,
        "total": total
    }
    r = requests.get("https://www.abc.net.au/news-web/api/loader/justinstories", params=payload)
    return r.json()

def get_article_soup(link: str):
    """Get's an article and turns it into Beautifulsoup ready for further investigation.

    Args:
        link (str): link to the news article

    Returns:
        BeautifulSoup: A BeautifulSoup object
    """
    print(f"Getting article: https://www.abc.net.au{link}")
    r = requests.get(f"https://www.abc.net.au{link}")
    if not r.ok:
        r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    return soup

get_title = lambda article: article['title']['children'].strip()
get_link = lambda article: article['link']['to']

def get_authors(article):
    """Get's list of authors for article. If none found returns None object"""
    authors = article['newsBylineProps']['authors']
    if authors is None:
        return None
    return [author['name'] for author in authors]

get_description = lambda article: article['synopsis']
get_published = lambda article: article['timestamp']['dates']['firstPublished']['labelDate']

def get_last_updated(article):
    """Get's the last updated timestamp from JSON object"""
    if article['timestamp']['dates']['lastUpdated'] is None:
        return None
    else:
        return article['timestamp']['dates']['lastUpdated']['labelDate'] 

def clean_article(article):
    """Parses the individual JSON objects from the article list
    Dictionary output will be the following
    {
        "title": str,
        "link": str,
        "author": list,
        "description": str,
        "published": str,
        "last_updated": str
    }
    """
    return {
        "title": get_title(article),
        "link": get_link(article),
        "author": get_authors(article),
        "description": get_description(article),
        "published": get_published(article),
        "last_updated": get_last_updated(article)
    }

def parse_article_list(article_list: dict):
    """Parses the initial article JSON list.

    Args:
        article_list (dict): JSON object of articles

    Returns:
        list: List of articles as dict objects
    """
    dirty_articles = article_list['collection']
    articles = [clean_article(article) for article in dirty_articles]
    return articles

def get_tags(soup: bs4.BeautifulSoup):
    """Get the meta tags of the article

    Args:
        soup (bs4.BeautifulSoup): A bs4 soup of the article

    Returns:
        list: meta tags for the article
    """
    meta_tags = soup.find_all('meta', property='article:tag')
    tags = [meta.get('content') for meta in meta_tags]
    return tags

# used to clean unicode spaces in page
clean_spaces = lambda text: text.replace(u'\xa0', u' ')

def get_content(soup: bs4.BeautifulSoup):
    """Get's the content from the article and returns it as a long string

    Args:
        soup (bs4.BeautifulSoup): BS4 parsed article

    Returns:
        str: content of the article
    """
    container_div = soup.find('div', {"class": "_2jYh0"})
    # Build Filter
    aside_pullquote = lambda tag: tag.get('data-component') == "Pullquote"
    p_tags = lambda tag: tag.name == 'p' and tag.parent.name == 'div' and not tag.has_attr('data-component')
    h2_tags = lambda tag: tag.name == 'h2' and tag.parent.name == 'div'
    # Get relevant content
    text_tags = container_div.find_all([aside_pullquote, p_tags, h2_tags])
    texts = [clean_spaces(text_tag.text).strip() for text_tag in text_tags]
    content = "\n\n".join(texts)
    with open('delete_me.txt', 'w') as outfile:
        outfile.write(content)
    return content

def get_key_points(soup: bs4.BeautifulSoup):
    """Get's the key points for the article

    Args:
        soup (bs4.BeautifulSoup): bs4 parsed article

    Returns:
        list: key points for the article
    """
    key_points_section = soup.find({'section': {'data-component': 'KeyPoints'}})
    # Handle if no key points for article
    if key_points_section is None:
        return None
    key_points_li = key_points_section.find_all('li')
    key_points = [clean_spaces(key_point.text) for key_point in key_points_li]
    return key_points

if __name__ == "__main__":
    articles = get_list_articles()
    clean_articles = parse_article_list(articles)
    
    article = clean_articles[0]
    print(article)
    soup = get_article_soup(article['link'])
    tags = get_tags(soup)
    content = get_content(soup)
    key_points = get_key_points(soup)
    article['tags'] = tags
    article['content'] = content
    article['key_points'] = key_points
    print(article)