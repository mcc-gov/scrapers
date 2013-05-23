#import feedparser
import urllib2
import chardet
from lxml import html

from lxml.html import parse
import lxml
import json

import requests

from datetime import datetime

errs_url="http://www.mcc.gov/pages/results/qsrs"

doc=parse(errs_url).getroot()
reports=doc.cssselect('li.span6 a')

#print compacts[0].text_content()

links=[]

for report in reports:	
	name=report.text_content().strip()
	href=report.attrib['href']

	if name.find("Compact")>0:
		country=name[0:name.find("Compact")-1]
	else:
		country=""

	r= requests.head(href)

	identifier="qsr-compact-"+country.lower()
	if name.find("Compact II")>0:
		identifier="qsr-compact-2-"+country.lower()
	elif name.find("Compact I")>0:
		identifier="qsr-compact-1-"+country.lower()


	try:
		d = datetime.strptime(r.headers["last-modified"], "%a, %d %b %Y %H:%M:%S %Z") 
	except:
		d=datetime.now()

	updated=d.strftime('%Y-%m-%d')
	#print updated, r.headers["last-modified"]

	links.append({"name":name,"href":href, "country":country, "updated":updated, "identifier":identifier})
	
print links

#import sys
#sys.exit(0)

metadata=[]

print "QSRs"
offs=0
for link in links:
	dataset={
		"title": link["name"],
		"description": link["name"],
		"theme":"Quarterly Status Reports",
		"keyword": "quarterly, status, report, compact, human-readable, "+link["country"].lower(),
		"modified": link["updated"],
		"publisher": "Millennium Challenge Corporation",
		"person": "Open Data Initiative",
		"mbox": "opendata@mcc.gov",
		"identifier": link["identifier"],
		"accessLevel": "Public",
		"distribution": [
			{
			"accessURL": link["href"],
			"format": "pdf"
			}
		]
    }

	metadata.append(dataset)

	offs=offs+1
	


print metadata

f=open("qsrs.json","w")
f.write(json.dumps(metadata,indent=4))
f.close()
	