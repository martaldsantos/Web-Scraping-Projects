import requests
import json
import pandas as pd
import time

def get_data():

    #url to be scraped
    url = "https://www.base.gov.pt/Base4/pt/resultados/" 

    #headers to be sent with the request
    headers = { 
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '147',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=KOOIJPGPHMMGFDAFDMIPIAOJMBHKOEDNAFAKJDMLLIAOIBLIBPMFDKKEBOABIMNLGNIDEABLPDBFGFHEJHJAHGJDFJNAIIAAGHLPKHLGALEIMPAJAPLDJGILFINNEKCO; f5avraaaaaaaaaaaaaaaa_session_=KCPMODJGNINMIDHJCOAMOEOHNDFPCEANOFMMEIHJJAAGGMJCOMACCIBLGACDNPFPBAGDLPEILDEEGPJHGFGAAMPOFJNFEHDOAFPFNHOGHOMNKGMILBKNJMIAMKDJKJHN',
        'Host': 'www.base.gov.pt',
        'Origin': 'https://www.base.gov.pt',
        'Referer': 'https://www.base.gov.pt/Base4/pt/pesquisa/?type=contratos&texto=&tipo=0&tipocontrato=0&cpv=&aqinfo=&adjudicante=&adjudicataria=&sel_price=price_c1&desdeprecocontrato=&ateprecocontrato=&desdeprecoefectivo=&ateprecoefectivo=&sel_date=date_c1&desdedatacontrato=&atedatacontrato=&desdedatapublicacao=&atedatapublicacao=&desdeprazoexecucao=&ateprazoexecucao=&desdedatafecho=&atedatafecho=&pais=0&distrito=0&concelho=0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }


    payload = { 
        'type': 'search_contratos',
        'version': '111.0', #version of the search API being used
        'query': 'tipo=0&tipocontrato=0&pais=0&distrito=0&concelho=0', #search query
        'sort': '-publicationDate', #sorting order of the search results
        'size': '25' #maximum number of search results to return. It will return (up) to 25 results because our webpage has 25 rows
    }

    i=0
    while True:
        payload['page'] = i #set the page number to be scraped
        response = requests.post(url, headers=headers, data=payload) #send the request
        data = json.loads(response.content) #get the response
        # print(data)
        data = data['items'] #get the items from the response in json format
        
        if i==0:
            df = pd.DataFrame.from_dict(data) #first dataframe creation
        else:
            df2 = pd.DataFrame.from_dict(data) #set data in dataframe format (helps with cleaning the utf-8 characters)
            df = pd.concat([df, df2], ignore_index=True) #add data to the originally created dataframe
        
        if i==1: #Number of pages to be scraped
            break
        
        i+=1

        time.sleep(2) #to avoid detection by the website

        #code to see the number of the page that is being scraped
        #print(i) 

    #take a look at the data you're scraping
    df['id'] = df['id'].astype(object).replace(',','')
    df.to_excel('contratos_request.xlsx', index=False,header=True )

if __name__ == "__main__":
    get_data()