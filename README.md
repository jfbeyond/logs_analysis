# Logs Analysis

This is a python application that connects to a databse called 'news' run in a Vagrant environment.

## Goal

As one of the projects of the BackEnd lessons in SQL and python, in this project, it is asked to answer some questions given a database that contains tables with information of articles, authors and logs of said articles views in a period of one month.

The project's goal is to solve the three following questions:

### 1. What are the most popular three articles of all time?

### 2. Who are the most popular article authors of all time?

### 3. On which days did more than 1% of requests lead to errors?

## How is it done?

SQL (PSQL) and Python will be utilized to solve the questions.
SQL to construct the queries to extract the desired information, and Python to connect to the database with the raw data and present the final report.

1. Most popular three articles: This is found through a combined SQL statement. It is observed that the 'article' and 'log' tables have the 'slug' information in common, which is manipulated with the 'concat' function.
The articles are then filtered down by calling out their titles with number of views in descending order.

2. Most popular authors of all time: To solve this question, a view is created (totals) containing the number of views por article by using their slug (view creation below):

create view totals as  select slug, count(*) 
as reads from articles,(select path as artpath from log) as subq 
where artpath = concat('/article/',slug) group by slug;

Then, a query is performed to extract the total of views per author given that they might have written more than one article.

3. Which days present more than 1% of errors in the requests?: This is a bit more complex question, however, it can be solved by creating first a view (datelogs) with a table having the total number of requests and failed requests per day (view creation below):

create view datelogs as select date(time) as logdate, count(*)
filter (where status = '404 NOT FOUND') as numfails, count(*) 
as trequests from log group by logdate order by logdate asc";

Then, using this view (datelogs) a query is to calculate the percentage of failed requests (failed requests/total requests)*100 every day filtering down those that exceed 1%.

NOTE: Views are already incorporated in the python file. They're shown here just to indicate how they are created.

To run the application, please go to the folder in a virtual machine window (vagrant) where the 'news' database is located (and loaded) and put the file logs_analysis.py in it. 
Type run logs_analysis.py to start the application. The answers to the three aforementioned questions will be printed in the terminal window.

Give it a try!

## Authors

* **Jhon Diaz** - [jfbeyond](https://github.com/jfbeyond)

## Acknowledgments

* Udacity
