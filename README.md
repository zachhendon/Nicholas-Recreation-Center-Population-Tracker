# Nicholas Recreation Center Population Tracker
A python application, automated by AWS, that scrapes data, analyzes it, and sends a weekly report on the status of the gym busyness.
## Purpose
The goal is to determine the best times to go to the Nicholas Recreation Center (UW Madison's campus gym). They provide a [live usage tracker website](https://recwell.wisc.edu/liveusage/) that they update roughly every hour, however it only displays current population data. To make educated decisions on when to go to the gym, I want to collect a history of the data so that I can analyze micro and macro patterns. 
## Description
### Scraping the data
The main tools that I used to retrieve the data from the website were the python libraries BeautifulSoup4 and requests. One of the main obstacles of scraping data from this website was its dynamic nature. If I sent a simple request to the link, I would get back an HTML block, but the values would all be default (0). I explored scraping with automated browser tools such as Selenium and Pupeteer, but eventually settled on a more grounded solution. By inspecting the webpage we can determine where this data is coming from and make a direct request to this new source. This also makes the application faster since the program doesn't have to boot up an entire browser every time it runs. It also makes the project easier to deploy and more lightweight (chromium is a large file).
### Storing the data
The data is then extracted from the request using BeautifulSoup. It is immediately exported to a MySQL database. The database information is stored in a [config.json](config-sample.json) file and needs to be configured to the database. 
### Automating this process
Using Docker and the AWS/Python3.9 base image, the application is exported to AWS and stored in its Elastic Container Registry. The MySQL database is hosted by its Relational Database Service (RDS). The main program is [DataGatherer.py](DataGatherer.py) and is automatically run in AWS Lambda. The Lambda function runs the pushed container every 30 minutes, appending the newly scraped data to the MySQL RDS database.
## Status
The immediate next step is to add further parameters to the tables. Adding more variables (temperature/weather, game day/week, etc.) will allow for more in-depth analysis. While some of this analysis may be currently too advanced for me, collecting this data will allow me to come back to it when I am more knowledgeable in math and statistics.

The next step will be to analyze the data. I will primarily focus on analyzing the best times of day and best days of the week to go to the gym. I may come back to some of the more advanced topics at a later date. 

Finally, I wish to produce a weekly report. This will initially be very bare-bones. In the future, I am looking into generating a pdf report using HTML and CSS.