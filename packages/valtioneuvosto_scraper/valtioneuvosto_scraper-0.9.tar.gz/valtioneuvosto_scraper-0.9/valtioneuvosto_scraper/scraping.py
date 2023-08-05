# -*- encoding: iso8859-1 -*-

import logging
from BeautifulSoup import BeautifulStoneSoup, SoupStrainer

from util import parse_date

logging.basicConfig()
logging.root.setLevel(logging.INFO)

baseurl = "http://www.valtioneuvosto.fi/tietoa-valtioneuvostosta/hallitukset/vuodesta-1917/tulokset/fi.jsp"

def parse_cabinet(html):
   "parse single government details"
   restrict = SoupStrainer("table", {"class":"header-table report-table"})
   soup = BeautifulStoneSoup(html, parseOnlyThese=restrict, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
   rows = soup.findAll("tr")[1:]
   cabinet = {}

   for row in rows:
      try:
         if row["class"] == "table-row-header":
            minister = row.td.text
            cabinet[minister] = []
      except:
         data = row.findAll("td")
         
         # party, person, from, until
         season = (data[3].text, data[0].text, data[1].span.text, data[2].span.text)
         cabinet[minister].append(season)

   return cabinet


def parse_governments(html):
   "parse a list of governments"

   govts = []   
   restrict = SoupStrainer("table", {"class":"header-table report-table"})
   soup = BeautifulStoneSoup(html, parseOnlyThese=restrict, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
   data = soup.findAll("tr")[1:]
   for row in data:
      r_label, r_dates, r_duration, r_party, r_type, r_ignore = row.findAll("td")
   
      label = r_label.a.text
      infourl = baseurl + r_label.a["href"]
      id, name = label.split(".", 1)
      id = int(id)

      name = name.strip()
      pmname = name.rstrip("V").rstrip("I").rstrip()

   
      if name.endswith("II"):
         order = 2
      elif name.endswith("III"):
         order = 3
      elif name.endswith("IV"):
         order = 4
      elif name.endswith("V"):
         order = 5
      else:
         order = 1
   
      begun, ended = r_dates.span.text.split("-")
      begun = parse_date(begun)
      if ended:
         ended = parse_date(ended)
      duration = int(r_duration.span.text)
      party = r_party.text
      govt_type = r_type.text
   
      govt = (id, name, pmname, party, order, begun, ended, duration, govt_type, infourl)
      
      govts.append(govt)

   return govts
   

