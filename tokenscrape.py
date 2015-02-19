#!/usr/bin/python

import praw
import time, datetime
import sys
from pandas import DataFrame 
from nltk import word_tokenize

sys.settrace

subreddit_name = "Homebrewing"

r = praw.Reddit("User-agent: analysis of /r/Homebrewing by /u/ajfranke v1.0")
sub = r.get_subreddit( subreddit_name )

start = sub.created_utc
# start = time.mktime(datetime.datetime.utcnow().timetuple())-15*86400
finish = time.mktime(datetime.datetime.utcnow().timetuple())

interval = 10*86400 # seconds

front = start
back = front+interval

allresults = []
wordlist = []
timelist = []
postlist = []
scorelist = []

count = 0

while back <= finish:  

    results = []
    
    print "querying time %s to %s" % (datetime.datetime.fromtimestamp(front).strftime("%Y-%m-%d"), 
                                      datetime.datetime.fromtimestamp(back).strftime("%Y-%m-%d"))
    while True:
        results = []
        query = "timestamp:%d..%d" % (front, back)

        # limited to 1000 submissions
        try:
            results = list(sub.search(query, sort='new', 
                                      syntax='cloudsearch', 
                                      limit=None))
        except:
            results = []
        
        if len(results) == 0:  # this is an awful failure condition...  
            print "No results... retrying"
            front = back
            back = front + interval
            time.sleep(1)
        elif len(results) < 999:
            time.sleep(1)
            # print [str(x) for x in results]
            break
        else:
            print "%d results... retrying" % len(results)
            interval = int(interval*0.9)
            back = front + interval
            time.sleep(1)
    
    print "adding %d results" % len(results)

    for result in results:
        count += 1
        tokens = word_tokenize( result.title )
        wordlist.extend( tokens )
        postlist.extend( [result.id for x in range(len(tokens))] )
        timelist.extend( [result.created_utc for x in range(len(tokens))] )
        scorelist.extend( [result.score for x in range(len(tokens))] )

    if back == finish:
        break

    front = back
    back = min( front + interval, finish )


print '%d posts catalogued' % count


# analyze

bigframe = DataFrame({ 'word': wordlist,
                       'post_id': postlist,
                       'time': timelist,
                       'score': scorelist
                      })

bigframe.to_csv("Homebrewing_data_%d_%d.csv"%(start,finish),
               sep='\t',
               encoding='utf-8')

print "Done!"
