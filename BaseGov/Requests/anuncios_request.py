import requests
import json
import pandas as pd
import time

def get_data():
    url = "https://www.base.gov.pt/Base4/pt/resultados/"
    headers = {
        'Host': 'www.base.gov.pt',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
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
        'version': '111.0',
        'query': 'tipoacto=0&tipomodelo=0&tipocontrato=0',
        'sort': '-drPublicationDate',
        'size': '25'
    }

    i=0
    while True:
        payload['page'] = i
        response = requests.post(url, headers=headers, data=payload)
        data = json.loads(response.content)
        data = data['items']
        
        if i==0:
            df = pd.DataFrame.from_dict(data)
        else:
            df2 = pd.DataFrame.from_dict(data)
            df = pd.concat([df, df2], ignore_index=True)
        
        if i==9000: #Number of Pages to be Scraped
            break
        i+=1
        time.sleep(2)
        print(i)
    print(df)

if __name__ == "__main__":
    get_data()