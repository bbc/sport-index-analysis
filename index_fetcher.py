import os
from ldpapi import LDPWriter, LDPCore, Dataset
from termcolor import colored
from rdflib import RDF, Graph, URIRef
from guids import *

SPORTS_KB = os.environ['SPORTS_KB']

ldp_writer = LDPWriter(
        ssl_crt=os.environ['BBC_CERT_CRT'],
        ssl_key=os.environ['BBC_CERT_KEY'],
        apigee_key=os.environ['APIGEE_KEY'])

ldp_core = LDPCore(
        ssl_crt=os.environ['BBC_CERT_CRT'],
        ssl_key=os.environ['BBC_CERT_KEY'],
        apigee_key=os.environ['APIGEE_KEY'])

def pull_datasets(guids):
    '''
    Get Sports datasets from live and saves them into the datasets folder
    '''
    for guid in guids:
        print colored('=> Downloading %s' % guid, 'yellow'),
        try:
            ds = ldp_writer.get_datasets_data(guid=guid, env='live')
            destination="datasets/%s" % ds.filename
            print destination
            ds.graph.serialize(destination=destination, format='turtle')
            print colored('Ok \n', 'green')
        except Exception as e:
            print colored('Error during download \n', 'red')
            print colored(e, 'red')

def sport_index_data():
    ds = Dataset()
    ds.graph = Graph()
    for filename in os.listdir("datasets"):
        if filename.endswith(".ttl"):
            new_ds = Dataset()
            new_ds.load("datasets/%s" % filename)
            ds.graph += new_ds.graph
    sparql = '''
        PREFIX core: <http://www.bbc.co.uk/ontologies/coreconcepts/>
        PREFIX sport: <http://www.bbc.co.uk/ontologies/sport/>
        PREFIX sal: <http://www.bbc.co.uk/ontologies/applicationlogic-sport/>
        PREFIX cms: <http://www.bbc.co.uk/ontologies/cms/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

        SELECT DISTINCT ?thing ?preferredLabel ?index 
        WHERE {
            ?thing core:preferredLabel ?preferredLabel ;
                core:primaryTopicOf ?index .
                FILTER STRSTARTS(str(?index), "http://www.bbc.co.uk/sport")
                
        }ORDER BY ?type 
    '''

    print "thing, preferredLabel, index"
    for row in ds.graph.query(sparql):
        # print row.preferredLabel, URIRef(row.index), row.type
        print "%s, %s, %s" % (row['thing'].toPython().split('/')[-1].split('#')[0], row['preferredLabel'].toPython(), row['index'].toPython())


if __name__ == '__main__':
    sport_index_data()
