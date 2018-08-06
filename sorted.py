import xml.etree.cElementTree as ET
import re 
import datetime
from collections import Counter

tmp = ''
prev = '' #if xml ordered by date, we can get the next result and keep track of max

total = 0 #most common date so far for grsphing thory
prevTotal = 0 #the previous dates maximum, for graph theory matches
maxGtDate = 0 #the most common date for graph theory posts

junePosts = 0 
tags = ''
cCount = 0 #number of posts tagged combinatotics 
noFibCount = 0 # same as above, no fibonacci-numbers tag
#noFibPattern = re.compile('^(?=.*combinatorics)(?!.*fibonacci-numbers).*') #used in regex to filter fib
gCount = 0 #numbe of graph-theory tagged posts

# get an iterable
context = ET.iterparse('../Posts.xml', events=("start", "end"))

# turn it into an iterator
context = iter(context)
# get the root element, so we can iterate and delete from root as wee go
event, root = next(context)

for event, elem in context:
    if event == "end" and elem.tag == "row":
        if "CreationDate" in elem.attrib:
            #get the date of the post and tally if june 2016.
            if "2016-06" in elem.attrib["CreationDate"]:
                junePosts += 1
        if "Tags" in elem.attrib:
            if "combinatorics" in elem.attrib["Tags"]:
                cCount += 1
                if "fibonacci-numbers" not in elem.attrib["Tags"]:
                    noFibCount += 1
            if "graph-theory" in elem.attrib["Tags"]:
                gCount += 1 
                #I search for the creation date 
                if "CreationDate" in elem.attrib:
                    tmp = elem.attrib["CreationDate"][0:7]
                    #if this date is the same as last, increment total. If not,
                    #the total is 1. Once we find new max, set it to prev, and 
                    #record the current max date.
                    if prev == tmp:
                        total += 1
                    elif prev != tmp: 
                        total = 1
                        prev = tmp #need to set prev again to catch the multiples
                    if total > prevTotal or prevTotal == 0:
                        prevTotal = total
                        prev = maxGtDate = tmp
                   
                    #this code was to count months, which was misinterpreted
                    #since all dates have the same format YYYY-MM... I can simply slice the 6th and 7th digits to get the month.
                    #cast ro int, remove the leading 0... 07 = 7.
                    #tmp = int(elem.attrib["CreationDate"][5:7].strip("0"))
                    #tmp -= 1 #convert month to index.. ie.) maarch 03 = index 2
                    #monthList[tmp] += 1; #counting months. 
                    #print(tmp)

        root.clear() #delete as we go... save pc from blowing up via memory overutilization
date = datetime.datetime.strptime(maxGtDate, "%Y-%m")
formatted_date = datetime.datetime.strftime(date, "%B %Y")

print("Posts in June 2016: " , junePosts)
print("Posts tagged with combinatorics: " , cCount)
print("Posts tagged with combinatorics but not fibonacci-numbers: " , noFibCount)
print("Posts tagged wih graph-theory: " , gCount)
print("the month with most graph-theory tags ", formatted_date)
#print("the month with most graph-theory tags:", maxTotal)