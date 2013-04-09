#import feedparser
import urllib2
import chardet
from lxml import html

from lxml.html import parse
import lxml
import json

index_url="http://data.mcc.gov/raw/index.json"

index=urllib2.urlopen(index_url).read()

#index=json.dumps(json.loads(index), indent=4)

index=json.loads(index)

#print index

errs_url="http://www.mcc.gov/pages/activities/activity/economic-rates-of-return"

doc=parse(errs_url).getroot()
compacts=doc.cssselect('div#activity-content-04 li a')

#print compacts[0].text_content()

links=[]

for c in compacts:	
	link=c.text_content().strip()
	#print c.text_content()
	#print c.attrib['href']
	links.append(c.attrib['href'])
	
#print "Links #1"
print links


err_links=[]
for link in links:
	print "-----------"
	print link


	content = urllib2.urlopen(link).read()
	encoding = chardet.detect(content)['encoding']
	if encoding != 'utf-8':
		content = content.decode(encoding, 'replace').encode('utf-8')
	doc = html.fromstring(content, base_url=link)
	
	#doc=parse(link).getroot()
	errs=doc.cssselect('ul.unstyled li.span4 a')
	
	for err in errs:
	
		href= err.attrib["href"]
		name=err.cssselect("span")[0].text_content()
		#name=name.replace(u'\u2019',"'")
		
		err_links.append({"href":href, "name":name})

# index.json {"datasets":d;"categories":c}

datasets=[]

for dataset in index["datasets"]:
	if dataset["group_id"]!=4:
		dataset["metadatalocation"]=dataset["metadatalocation"].strip()
		datasets.append(dataset)

index["datasets"]=datasets

print "Errs"
offs=0
for link in err_links:
	print link["href"].encode('utf-8')
	print link["name"].encode('utf-8')
	print "---"
	
	index["datasets"].append({
            "description": link["name"].encode('utf-8'), 
            "name": link["name"].encode('utf-8'), 
            "location": link["href"].encode('utf-8'), 
            "formats": ".xls", 
            "group_id": 4, 
            "type": "documents", 
            "id": 9999+offs, 
        }) 

	offs=offs+1
	


"""
        {
            "description": "Senegal's Irrigation and Water Resources Management Project Delta Irrigation Activit", 
            "name": "Senegal's Irrigation and Water Resources Management Project Delta Irrigation Activit", 
            "location": "http://www.mcc.gov/documents/err/mcc-err-senegal-delta-irrigation.xls", 
            "formats": ".xls", 
            "group_id": 4, 
            "type": "documents", 
            "id": 1221, 
        }, 

        {
            "metadatalocation": "http://www.mcc.gov/documents/err/mcc-err-senegal-delta-irrigation.html                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          ", 
            "description": "Senegal's Irrigation and Water Resources Management Project Delta Irrigation Activit", 
            "name": "Senegal's Irrigation and Water Resources Management Project Delta Irrigation Activit", 
            "location": "http://www.mcc.gov/documents/err/mcc-err-senegal-delta-irrigation.xls", 
            "formats": ".xls", 
            "group_id": 4, 
            "type": "documents", 
            "id": 1221, 
            "group_location": "/null"
        }, 

"""

f=open("index.json","w")
f.write(json.dumps(index,indent=4))
f.close()
	