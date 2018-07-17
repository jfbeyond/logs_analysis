#!/usr/bin/python2.7

import psycopg2

DBNAME = "news"
db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# First query to extract the articles with their number of views, organized
# by descendent number
c.execute("select title,count(*) as num from articles,\
    (select path as artpath from log) as subq\
    where artpath = concat('/article/',slug) group by title order by\
    num desc limit 3")
popular = c.fetchall()
print
print "1. What are the three most popular articles of all time?"
print

for row in popular:
    print row[0], 'with a total of', row[1], 'views'

# Second question
# Create view that summarizes number of views per article by using 'slug'
c.execute("create view totals as  select slug, count(*) \
    as reads from articles,(select path as artpath from log) as subq \
    where artpath = concat('/article/',slug) group by slug")

# Query to get the authors with the most number of views, given that they
# might have written many articles
c.execute("select name, sum(totals.reads) as reads from articles, \
    authors, totals where articles.slug = totals.slug AND \
    authors.id = articles.author group by name order by reads desc")

popular_authors = c.fetchall()
print
print "2. Who are the most popular article authors of all time?"
print
for row in popular_authors:
    print row[0], 'with a total of', row[1], 'views'

# Third  question
# Create view for table containing number of total and failed requests per day
c.execute("create view datelogs as select date(time) as logdate, count(*) \
    filter (where status = '404 NOT FOUND') as numfails, count(*) \
    as trequests from log group by logdate order by logdate asc")

# Query to find day(s) in which failed requests are > 1% of total requests
c.execute("select logdate, 100.0*numfails/trequests as percentage \
    from datelogs where 100.0*numfails/trequests > 1")

failed_req = c.fetchall()
print
print "3. On which days did more than 1% of requests lead to errors?"
print
for row in failed_req:
    fail_per = str("%.2f" % row[1])
    print row[0].strftime("On %b %d, %Y,"), 'the percentage of requests that'\
        ' led to errors was', fail_per, '%.'
print

db.close()
