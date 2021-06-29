import urllib.request
import urllib.parse
import json
import pprint
import time
import pandas as pd
from pandas import json_normalize

class CoreApiRequestor:

    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key
        #defaults
        self.pagesize = 100
        self.page = 1

    def parse_response(self, decoded):
        res = []
        for item in decoded['data']:
            doi = None
            if 'identifiers' in item:
                for identifier in item['identifiers']:
                    if identifier and identifier.startswith('doi:'):
                        doi = identifier
                        break
            res.append([item['title'], doi])
        return res

    def request_url(self, url):
        with urllib.request.urlopen(url) as response:
            html = response.read()
        return html

    def get_method_query_request_url(self,method,query,fullText,page,from_year=2001):
        if (fullText):
            fullText = 'true'
        else:
            fullText = 'false'
        params = {
            'apiKey':self.api_key,
            'page':page,
            'pageSize':self.pagesize,
            'fulltext':fullText,
            'language.name':'en',
            'from_Year':from_year
        }
        return self.endpoint + method + '/' + urllib.parse.quote(query) + '?' + urllib.parse.urlencode(params)

    def get_up_to_20_pages_of_query(self,method,query,fulltext):
        url = self.get_method_query_request_url(method,query,fulltext,1)
        all_articles=[]
        resp = self.request_url(url)
        result = json.loads(resp.decode('utf-8'))
        all_articles.append(result)
        if (result['totalHits']>100):
            numOfPages = int(result['totalHits']/self.pagesize)  #rounds down
            
            if (numOfPages>20):
                numOfPages=20
                
            for i in range(2,numOfPages):
                url = self.get_method_query_request_url(method,query,False,i)
                #print(url)
                resp =self.request_url(url)
                all_articles.append(json.loads(resp.decode('utf-8')))
                if i%10==0:
                    time.sleep(5)
        return all_articles
    
    def get_all_pages_of_query(self,method,query,fulltext):
        url = self.get_method_query_request_url(method,query,fulltext,1)
        all_articles=[]
        resp = self.request_url(url)
        result = json.loads(resp.decode('utf-8'))
        all_articles.append(result)
        
        
        if (result['totalHits']>100):
            numOfPages = int(result['totalHits']/self.pagesize)  #rounds down
            
            for i in range(2,numOfPages):
                url = self.get_method_query_request_url(method,query,False,i)
                #print(url)
                resp =self.request_url(url)
                all_articles.append(json.loads(resp.decode('utf-8')))
                if i%10==0:
                    time.sleep(5)
        return all_articles


from collections import Counter

def year_profile(data):
    years_list = []
    for hits in data:
        for hit in hits['data']:
            if 'year' in hit['_source']:
                years_list.append(hit['_source']['year'])
    
    
    cnts = Counter(years_list)
    del(cnts[None])
    
    return cnts

def year_profile_fromdf(df):
    cnts = Counter(list(df['year']))
    del(cnts[None])
    
    return cnts

def To_pd_DF(orginal):
        
    pages = len(orginal)
    df = json_normalize(orginal[0]['data'][0]['_source'])

    for i in range(pages):
        articles=len(orginal[i]['data']) # articles per page
        for j in range(articles):
            df_temp = json_normalize(orginal[i]['data'][j]['_source'])
            df = pd.concat([df,df_temp], ignore_index=True)
    
    df = df.drop(0).reset_index(drop=False, inplace = False)
    
    df['fullText'] = [k.replace('-\n', '').replace(' \n',' ').replace('\n',' ').replace('\t',' ') for k in df['fullText']]
    
    return df

def string_preprocessing(list_text):
    processed = [k.replace('-\n', '').replace(' \n',' ').replace('\n',' ').replace('\t',' ') for k in list_text]
    return processed