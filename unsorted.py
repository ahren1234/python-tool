import xml.etree.cElementTree as ET
import re 
import datetime
from collections import Counter

tmp = ''
junePosts = 0 
tags = ''
cCount = 0 #number of posts tagged combinatotics 
noFibCount = 0 # same as above, no fibonacci-numbers tag
#noFibPattern = re.compile('^(?=.*combinatorics)(?!.*fibonacci-numbers).*') #used in regex to filter fib
gCount = 0 #numbe of graph-theory tagged posts
mostCommonMonth = "" #the month with most graph-theory tags
monthList = []

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
                #to the reader: 
                #I had a few options here. I could try to sort the graph theory rows and then get 
                #the most common month, but that would probably have been O(nlogn), so i eliminated that.
                #that leaves me 2 options: try to count as i go, or just use most_common at the end. 
                #I figure that just doing O(n) at the end will be faster than trying to compare as I go. 
                #if I had more time, perhaps this perf could be improved!
                if "CreationDate" in elem.attrib:
                    tmp = elem.attrib["CreationDate"][0:7]
                    monthList.append(tmp) #counting months.                    
                    #this code was to count months, which was misinterpreted
                    #since all dates have the same format YYYY-MM... I can simply slice the 6th and 7th digits to get the month.
                    #cast ro int, remove the leading 0... 07 = 7.
                    #tmp = int(elem.attrib["CreationDate"][5:7].strip("0"))
                    #tmp -= 1 #convert month to index.. ie.) maarch 03 = index 2
                    #monthList[tmp] += 1; #counting months. 

        root.clear() #delete as we go... save pc from blowing up via memory overutilization
#done with data now, just need most common month with graph-theory tags
#
#I can't really find how this lib handles ties with a quick search, but it seems to be lowest index. 
#for the purposes of a test, i think it is highly unlikely for there to be a tie in 2.5GB
#in real life, I'd handle this accordingly. 
mostCommonMonth = Counter(monthList).most_common(1)[0]
print("Posts in June 2016: " , junePosts)
print("Posts tagged with combinatorics: " , cCount)
print("Posts tagged with combinatorics but not fibonacci-numbers: " , noFibCount)
print("Posts tagged wih graph-theory: " , gCount)
print("the month with most graph-theory tags:", mostCommonMonth[0])