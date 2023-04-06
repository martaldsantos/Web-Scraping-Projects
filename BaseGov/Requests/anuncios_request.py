import requests
import json
import pandas as pd
import time

def get_data():

    #url to be scraped
    url = "https://www.base.gov.pt/Base4/pt/resultados/" 
    
    #headers to be sent with the request
    headers = { 
        'Host': 'www.base.gov.pt',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'pt-PT,pt;q=0.8,en;q=0.5,en-US;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '128',
        'Origin': 'https://www.base.gov.pt',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.base.gov.pt/Base4/pt/pesquisa/?type=anuncios&texto=&numeroanuncio=&emissora=&desdedatapublicacao=&atedatapublicacao=&desdeprecobase=&ateprecobase=&tipoacto=0&tipomodelo=0&tipocontrato=0&cpv=',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }


    payload = { 
        'type': 'search_anuncios',
        'version': '111.0', #version of the search API being used
        'query': 'tipoacto=0&tipomodelo=0&tipocontrato=0', #search query
        'sort': '-drPublicationDate', #sorting order of the search results
        'size': '25' #maximum number of search results to return. It will return (up) to 25 results because our webpage has 25 rows
    }

    i=0
    while True:
        payload['page'] = i #set the page number to be scraped
        response = requests.post(url, headers=headers, data=payload) #send the request
        data = json.loads(response.content) #get the response
        data = data['items'] #get the items from the response in json format
        
        if i==0:
            df = pd.DataFrame.from_dict(data) #first dataframe creation
        else:
            df2 = pd.DataFrame.from_dict(data) #set data in dataframe format (helps with cleaning the utf-8 characters)
            df = pd.concat([df, df2], ignore_index=True) #add data to the originally created dataframe
        
        if i==10: #Number of pages to be scraped
            break
        
        i+=1

        time.sleep(2) #to avoid detection by the website

        #code to see the number of the page that is being scraped
        #print(i) 

    #take a look at the data you're scraping
    print(df)

if __name__ == "__main__":
    get_data()