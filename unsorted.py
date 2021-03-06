import xml.etree.cElementTree as ET
import re 
import datetime
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

tmp = ''
tags = ''
cCount = 0 #number of posts tagged combinatotics 
noFibCount = 0 # same as above, no fibonacci-numbers tag
#noFibPattern = re.compile('^(?=.*combinatorics)(?!.*fibonacci-numbers).*') #used in regex to filter fib
gCount = 0 #numbe of graph-theory tagged posts
mostCommonMonth = "" #the month with most graph-theory tags
junePosts = 0 
quarterlyData = [] #results per quarter for graph theory
baseDate = datetime.datetime(1800, 1, 1) #hack to check if we are in the first line of xml
dateStart = baseDate
dateEnd = baseDate
maxGtDate = 0 #the most common date for graph theory posts
monthlyData = {}

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
                    if tmp not in monthlyData:
                        monthlyData[tmp] = 1
                    if monthlyData[tmp] >= 1:
                        monthlyData[tmp] += 1
                    
                    #if first result
                    if dateStart == baseDate:
                        dateStart = datetime.datetime.strptime(tmp, "%Y-%m")
                    else: 
                        dateEnd = datetime.datetime.strptime(tmp, "%Y-%m")
                   
                    #this code was to count months, which was misinterpreted
                    #since all dates have the same format YYYY-MM... I can simply slice the 6th and 7th digits to get the month.
                    #cast ro int, remove the leading 0... 07 = 7.
                    #tmp = int(elem.attrib["CreationDate"][5:7].strip("0"))
                    #tmp -= 1 #convert month to index.. ie.) maarch 03 = index 2
                    #monthList[tmp] += 1; #counting months. 
                    #print(tmp)
        root.clear() #delete as we go... save pc from blowing up via memory overutilization

#done with data now, just need most common month with graph-theory tags
v = list(monthlyData.values())
k = list(monthlyData.keys())
mostCommonMonth = k[v.index(max(v))]

#calculate the starting quarter (1-4)
q = (dateStart.month-1)//3+1
tot = 0

#Monthlydata has the key, val pairs.. i start with first date, get the quarter, 
#then every time the qtr changes, i add to the total for that quarter.
for key, value in monthlyData.items():
    date = datetime.datetime.strptime(key, "%Y-%m")
    #count qwuarterly totals until new quarter 
    if((date.month-1)//3+1 == q):
        tot += value
    elif tot > 0:
        q = ((date.month-1)//3)+1
        quarterlyData.append(tot)
        tot = value
dateRange = pd.date_range(dateStart, dateEnd, freq = 'Q')
plt.plot(dateRange, quarterlyData, lw = 2, color = 'green', alpha = 1)
plt.gcf().autofmt_xdate()
plt.title('Quarterly Posts tagged \'graph-theory\'')
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.savefig("quarterly_data.png")
plt.show()

print("Posts in June 2016: " , junePosts)
print("Posts tagged with combinatorics: " , cCount)
print("Posts tagged with combinatorics but not fibonacci-numbers: " , noFibCount)
print("Posts tagged wih graph-theory: " , gCount)
print("the month with most graph-theory tags:", mostCommonMonth)
