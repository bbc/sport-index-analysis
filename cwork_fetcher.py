# encoding=utf8
import os
import requests
import pandas as pd
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

ssl_crt = os.environ['BBC_CERT_CRT']
ssl_key = os.environ['BBC_CERT_KEY']
apigee_key = os.environ['APIGEE_KEY']


def creative_works(about, page=1, language='en-gb', headers={'accept': 'application/json-ld'}):
    params = {"about": about, "api_key": apigee_key, "page": page}
    endpoint = "https://ldp-core.api.bbci.co.uk/ldp-core/creative-works"
    r = requests.get(endpoint, params=params, cert=(
        ssl_crt, ssl_key), headers=headers, verify=False)
    if r.status_code != 200:
        print r.text
    return r.text


def download_cworks():
    df = pd.read_csv("results.csv", header=0)
    for index, thing in df['thing'].iteritems():
        response = creative_works(thing)
        file = open("cworks/{}.json".format(thing), 'w')
        file.write(response)
        file.close
        # response = creative_works(thing, page=2)
        # file = open("cworks/{}-p2.json".format(thing), 'w')
        # file.write(response)
        # file.close


# Add cwork columns in the spreadsheet 
def add_cwork_columns_in_csv():
    df = pd.read_csv("results.csv", header=0)
    df['cw_number'] = pd.Series()
    for index in range(1, 21):
        df['cw{}_dateModified'.format(index)] = pd.Series()
        df['cw{}_category'.format(index)] = pd.Series()


def populate_cwork_columns_in_csv():
    df = pd.read_csv("results.csv", header=0)
    for filename in os.listdir("cworks"):
        if filename.endswith(".json"):
            thing = filename.split('.')[0]
            print filename
            with open('cworks/{}'.format(filename)) as json_file:
                cworks_data = json.load(json_file)
                row_no = df.index[df['thing'] == thing]
                if cworks_data.get('results'):
                    print row_no
                    df.at[row_no, 'cw_number'] = len(cworks_data['results'])
                    print len(cworks_data['results'])
                    cwork_col_i = 1
                    for cwork in cworks_data['results']:
                        if cwork.get('dateModified'):
                            df.at[row_no, 'cw{}_dateModified'.format(cwork_col_i)] = cwork['dateModified'].split('T')[0]
                        if cwork.get('category'):
                            df.at[row_no, 'cw{}_category'.format(
                                cwork_col_i)] = cwork['category']
                        cwork_col_i += 1
                else:
                    df.at[row_no, 'cw_number'] = 0
    df.to_csv('results.csv')


# download_cworks()
populate_cwork_columns_in_csv()
