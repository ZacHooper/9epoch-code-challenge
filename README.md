# 9epoch-code-challenge

## Objectives
**Populate a small database on AWS with Python & analyse the data**

1. Using a free tier AWS account, host and launch a small postgresql database in the cloud to store your project data. 
2. Using python frameworks such as requests and beautiful soup, build a small app that can scrape news articles from a news website (CNN, ABC, etc) on a variety of topics. Take care with this python code and try to design the small app in a way that is easy to maintain and is error-tolerant. The code for the app should be hosted on github. Please do not push any secrets to the repo.
3. Scrape >200 news articles with your app and store this data in a new table created in your new AWS database, take care with the schema of the table.
4. In a jupyter/colab notebook query the news data in your database. You can use sql-alchemy and psycopg2 libraries to connect to your database. Run some aggregate queries on your news data and display the results in the notebook. 
5. Send us your github repo, credentials for your small database and your python notebook so that we can inspect your python code, database schema & SQL queries.

## Explanation of Work

My general goal of this project was to simulate the creation of a pipeline that would be scraping this news site daily. The `abcArticles.py` script would be the script used in the scheduler to run this script daily. 

ABC was used as the news website to scrape. Their "Just In" page provides a continuous list of all their most recent articles. Inspecting that page reveals a useful endpoint of their API: `https://www.abc.net.au/news-web/api/loader/justinstories`. This endpoint returns a JSON object containing all the just in stories and useful metadata for each article. 

### Scraping the website

The scraper first queries this endpoint for the 200 most recent articles and saves the details to a DataFrame. The scraper then loops through the returned articles and queries for the actual articles page, where it then scrapes the content, key points and tags from the raw HTML. 

### Sentiment Analysis

The pre-trained sentiment analysis tool ["VADER"](https://github.com/cjhutto/vaderSentiment) was used to analyse the title and key points of the articles. 

> The use of the pre-trained model simulates the data science team passing on their models to me for deployment in the pipeline

### Database

A Postgresql database was used to store the scraped articles. The schema of the `abc_articles` table is as follows:

| Column Label         | Data Type | Notes                        |
|----------------------|-----------|------------------------------|
| id                   | serial    | Primary Key & Auto Increment |
| title                | text      |                              |
| author               | text[]    |                              |
| description          | text      |                              |
| published            | timestamp |                              |
| last_updated         | timestamp |                              |
| tags                 | text[]    |                              |
| content              | text      |                              |
| key_points           | text[]    |                              |
| title_sentiment      | numeric   |                              |
| key_points_sentiment | numeric   |                              |

Following the scraping and sentiment analysis the data was inserted into the database above. The articles were processed 25 at a time to reduce on RAM requirements.

### Analysis

The database was queried using the Python library [`sqlalchemy`](https://www.sqlalchemy.org). All the returned results were visualised using a Pandas DataFrame. 

Several aggregations were completed with most notable being the sentiment comparison of the title and key points for each author and each tag associated with the articles scraped. 

## Installation

To use this scraper clone this repo.

```bash
git clone https://github.com/ZacHooper/9epoch-code-challenge.git
```

Move into the newly created directory and create a new file called `.env`. 

The `.env` file will contain the details to your database. Please populate with your details accordingly.
```bash
POSTGRES_USER="user"
POSTGRES_PASSWORD="password"
POSTGRES_HOST="ec2-x-x-x-x.ap-the-moon-1.compute.amazonaws.com"
POSTGRES_DATABASE_NAME="database"
```

Create a new Python virtual environment

```bash
python3 -m venv venv
```

Install the required dependencies

```bash
pip install -r requirements.txt
```

Run the script

```bash
python abcArticles.py
```

The script will scrape the 200 most recent articles from the abc.com.au and add them to your database. You can then use the jupyter notebook `abc_article_analysis.ipynb` to complete the analysis. 