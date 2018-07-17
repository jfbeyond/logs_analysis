# Logs Analysis

This is a python application that connects to a databse called 'news' run in a Vagrant environment.

## Goal

As one of the projects of the BackEnd learning in SQL and python, in this project, it is asked to solve some questions given a database that contains tables with information of articles, authors and logs of views in a period of one month.
The object of the project is to solve the three following questions:

### 1. What are the most popular three articles of all time?

### 2. Who are the most popular article authors of all time?

### 3. On which days did more than 1% of requests lead to errors?

## How is it done?

In order to answer the previous questions, SQL (PSQL) and Python will be utilized.
SQL to construct the queries to extract the desired information and python to connect to the database with the raw data and present the final report.

1. Most popular three articles: This is found through a combined SQL statement. It is observed that the 'article' and 'log' tables have some the 'slug' information in common.
The articles are then filtered down by calling out their titles with number of views in descending order.

2. Most popular authors of all time: To solve this question, a view is created (totals) containing the number of views por article by using their slug (view creation below):

create view totals as  select slug, count(*) 
as reads from articles,(select path as artpath from log) as subq 
where artpath = concat('/article/',slug) group by slug;

Then, a query is performed to extract the total of views per author given that they might have written more than one article.

3. Which days present more than 1% of errors in the requests?: This is a bit more complex question, however it can be solved by creating first a view (datelogs) with a table having the total number of requests and failed requests per day (view creation below):

create view datelogs as select date(time) as logdate, count(*)
filter (where status = '404 NOT FOUND') as numfails, count(*) 
as trequests from log group by logdate order by logdate asc";

NOTE: Views are already incorporated in python file. They're here just to show how they were created.

Then, using this view (datelogs) a query is to calculate the percentage of failed requests (failed requests/total requests)*100 every day filtering down those that exceed 1%.

To run the application, please go a virtual machine window where the 'news' database is located (and loaded) and run logs_analysis.py.
The answers to the three aforementioned questions will be printed in the terminal window.

Just give it a try!

## Authors

* **Jhon Diaz** - [jfbeyond](https://github.com/jfbeyond)

## Acknowledgments

* Udacity
