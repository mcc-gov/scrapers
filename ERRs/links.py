#import feedparser
import urllib2
import chardet
from lxml import html

from lxml.html import parse
import lxml
import json

import requests
from datetime import datetime

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

		if name.find(u"\u2019")>0:
			country=name[0:name.find(u"\u2019")]
		else:
			country=""

		name=name.replace(u'\u2019',"'")


		r= requests.head(href)

		identifier=href[href.find("/err/")+5:-4]

		try:
			d = datetime.strptime(r.headers["last-modified"], "%a, %d %b %Y %H:%M:%S %Z") 
		except:
			d=datetime.now()

		updated=d.strftime('%Y-%m-%d')
		#print updated, r.headers["last-modified"]		
		err_links.append({"href":href, "name":name, "country":country, "identifier":identifier, "updated":updated})

# index.json {"datasets":d;"categories":c}


print err_links

print "Errs"

metadata=[]	

print "QSRs"
offs=0
for link in err_links:
	dataset={
		"title": link["name"],
		"description": link["name"],
		"theme":"Economic Rate of Returns",
		"keyword": "return rate, economy, err, analysis, compact, human-readable, "+link["country"].lower(),
		"modified": link["updated"],
		"publisher": "Millennium Challenge Corporation",
		"person": "Open Data Initiative",
		"mbox": "opendata@mcc.gov",
		"identifier": link["identifier"],
		"accessLevel": "Public",
		"distribution": [
			{
			"accessURL": link["href"],
			"format": "xls"
			}
		]
    }

	metadata.append(dataset)

	offs=offs+1
	
print metadata

f=open("errs.json","w")
f.write(json.dumps(metadata,indent=4))
f.close()
	