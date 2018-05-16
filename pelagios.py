from bs4 import BeautifulSoup
import re

# This code aims at creating the rdf file used by Pelagios

rdf = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xml:base="http://isawnyu.github.com/isaw-papers-awdl/pelagios/isaw-papers-pelagios.rdf">
'''

creator = '<dcterms:creator rdf:resource="http://isaw.nyu.edu/"/>'
annotation = '<rdf:type rdf:resource="http://www.openannotation.org/ns/Annotation"/>'

for i in range(1, 14):
	with open ("isaw-papers-awdl/"+str(i)+"/index.xhtml") as index :
		j=0
		soup = BeautifulSoup(index, "lxml")
		locations = soup.find_all("a", {"href" : re.compile("://pleiades.stoa.org/*")})

		for location in locations :
			j+=1
			rdf += '\n<rdf:Description xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:h="http://www.w3.org/1999/xhtml" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:oac="http://www.openannotation.org/ns/" xmlns:dcterms="http://purl.org/dc/terms/" rdf:ID="isaw-papers-'+str(i)+'-reference-'+str(j)+'">'
			rdf+= '\n' +annotation

			rdf+= ' \n<oac:hasBody rdf:resource="' + location["href"] + '"/>'
			try :
				target = location.find_parent("p")["id"]
			# article 9 has locations in figure elements and is raising this exception 
			except(TypeError) :
				try :
					target = location.find_parent("figure")["id"]
				except(KeyError):
					print("No id")
			rdf += '\n' + creator
			rdf += '\n<oac:hasTarget rdf:resource="http://dlib.nyu.edu/awdl/isaw/isaw-papers/'+str(i)+'/#'+target+'"/>'
			rdf += '\n<dcterms:title>Reference in ISAW Papers '+str(i)+' to "'+location.get_text()+'".</dcterms:title>'
			rdf += '\n</rdf:Description>'

rdf += '\n</rdf:RDF>'

with open ("pelagios.rdf", "w") as pelagios_rdf :
	pelagios_rdf.write(rdf)
