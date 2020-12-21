# swe-compass

SWE-Compass is a analysis service which mines the most desired ability of the software engineering industry from lots of job description samples on several well-known talent recruitment websites, such as LinkedIn and Glassdoor.

## Prerequisites
- docker 20.10.0, build 7287ab3
- docker-compose 1.27.4, build 40524192
- elasticsearch 7.10.1
- poetry 1.1.4
- python 3.8

## Getting Started

### Setup Workspace Environment
All necessary modules could be installed by poetry.
```
$ poetry install
```

### Run Elasticsearch Cluster
For advanced details of orchestration please refer to `docker-compose.yml`.
```
$ docker-compose up -d
```

### Start Scraping
Start scraping data from the target websites.
```
$ poetry run python main.py
```

### Check the Results
Take an overview of your index.
```
$ curl -X GET http://localhost:9200/_cat/indices\?v
```
Or fetch the specified document by id.
```
$ url -X GET http://localhost:9200/job_description/_doc/{ID}
```
And clean all data with the index.
```
$ curl -X DELETE http://localhost:9200/job_description
```

## Configuration
All configrations are placed at `scraper/scraper/settings.py` currently. Here are some critical sections you may interested in:

- **Item Pipeline**

    Remember to turn off ElasticsearchPipeline if your cluste is not ready, or you may encounter a connection error.
```
ITEM_PIPELINES = {
    "scraper.pipelines.ScraperPipeline": 300,
    "scraper.pipelines.ElasticsearchPipeline": 400,
}
```

- **Scraper Workload**

    The numbers of the page count are stand for how many search result pages should the spider process, not the total amount of job posts. The actual amount of the job posts to scrape would be multiplied by the batch query size of different website.
```
# Scraper workload
LINKEDIN_SCRAPER_PAGECOUNT = 5
GLASSDOOR_SCRAPER_PAGECOUNT = 3
```

## Contributors
[RainrainWu](https://github.com/RainrainWu)