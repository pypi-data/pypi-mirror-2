#! python
# -*- encoding: iso8859-1 -*-

"""
test: fetch data and export it as XML, parse it to verify it's valid (just valid xml, no schema check
"""

import os, sys, logging, urllib
from xml.etree import ElementTree as etree

from valtioneuvosto_scraper import parse_governments, parse_cabinet, output_xml

logging.basicConfig()

logger = logging.getLogger("scraper")
logger.setLevel(logging.DEBUG)

govts_url = "http://www.valtioneuvosto.fi/tietoa-valtioneuvostosta/hallitukset/vuodesta-1917/tulokset/fi.jsp?report_id=V2"
data_dir = "data"

govts_fname = "hallitukset.html"
cab_fname = "%i.html"

xmlout_fname = "hallitukset.xml"


def write_xml(governments, cabinets):
   logger.info("generating xml")
   xml = output_governments(govts, msters)
   logger.info("writing to %s" % xml_output_file)
   out = open(xml_output_file, "w")                                             
   out.write(xml.encode("UTF-8"))
   out.close()


def cache_files(govts_url, data_dir, govts_fname):
   html = urllib.urlopen(govts_url).read()
   datapth = os.getcwd() + os.sep + data_dir
   logger.debug("luodaan hakemisto %s" % datapth)
   os.mkdir(datapth)
   with open(datapth + os.sep + govts_fname, "w") as gfile:
      gfile.write(html)
   logger.debug("tallennettiin hallitusluettelo tiedostoon")

   govts = parse_governments(html)
   for g in govts:
      with open(datapth + os.sep + cab_fname % g[0], "w") as cab_file:
         html = urllib.urlopen(g[-1]).read()
         logger.info(u"haettiin hallituksen %i kokoonpanon sisältävä www-sivu" % g[0])
         cab_file.write(html)
         logger.info("tallennettiin sivu tiedostoon '%s'" % (cab_fname % g[0],))


if __name__=="__main__":

   cache_files(govts_url, data_dir, govts_fname)
   logger.info("kaikkien tietojen haku onnistui!")

   try:
      with open(data_dir + os.sep + govts_fname) as gfile:
         govts_html = gfile.read()
   except IOError, e:
      logger.error(u"datahakemisto ei sisällä hallituksia luetteloivaa html-sivua")
      sys.exit("ohjelman suoritus keskeytetään.")  

   govts = parse_governments(govts_html)
   logger.info("hallitusluettelon luku onnistui")

   logger.info("luetaan hallitusten kokoonpanot ... (hetkinen)")  
   cabs = {}
   for g in govts:
      try:
         with open(data_dir + os.sep + cab_fname % g[0]) as cab_file:
            cab_html = cab_file.read()
            cabs[g[0]] = parse_cabinet(cab_html)
      except IOError, e:
         logger.error(u"datahakemisto ei sisällä hallituksen %i kokoonpanoa sisältävää html-sivua" % g[0])
         sys.exit("ohjelman suoritus keskeytetään.")
      
   logger.info("hallitusten kokoonpanojen luku onnistui")

   xml = output_xml(govts, cabs)
   with open(data_dir + os.sep + xmlout_fname, "w") as xml_file:
      xml_file.write(xml.encode("UTF-8"))

   logger.info("kirjoitettiin xml-tiedosto '%s' datahakemistoon." % xmlout_fname)

   try:
      xml = etree.parse(data_dir + os.sep + xmlout_fname)
      logger.info("output is valid xml. tests ok.")
   except:
      logger.error("output is NOT valid xml or does not exist. need to debug.")
