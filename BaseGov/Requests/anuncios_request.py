import requests
import json
import pandas as pd
import time

def get_details(df):
    #This function gets the details of each of the anuncios, based on the ID scraped on the main website
    lista_completa= []
    df2 = pd.DataFrame({'id': df['id'].astype(str)})
    df2["link_detalhe"] = "https://www.base.gov.pt/Base4/pt/detalhe/?type=anuncios&id=" + df2["id"]
    
    for index in df.index:
        url = "https://www.base.gov.pt/Base4/pt/resultados/" 
        
        #headers to be sent with the request
        headers = { 
            'Host': 'www.base.gov.pt',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '44',
            'Origin': 'https://www.base.gov.pt',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': df2.loc[index, 'link_detalhe'],
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows"
        }

        payload = { 
            'type': 'detail_anuncios',
            'version':'111.0', 
            'id': df2.loc[index, 'id']
        }

        response = requests.post(url, headers=headers, data=payload) #send the request
        data = json.loads(response.content) #get the response
        lista_completa.append(data)

    expanded_data = pd.DataFrame(lista_completa)
    return expanded_data

df = pd.read_excel("anuncios_request.xlsx")
expanded_data= get_details(df)
expanded_data[['nif', 'description', 'entidade_id']] = expanded_data['contractingEntities'].apply(lambda x: pd.Series([x[0]['nif'], x[0]['description'], x[0]['id']]))
expanded_data.drop('contractingEntities', axis=1, inplace=True)
expanded_data.to_excel('expanded_data.xlsx', index=False,header=True )


def main():

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
        'Content-Length': '147',
        'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=KOOIJPGPHMMGFDAFDMIPIAOJMBHKOEDNAFAKJDMLLIAOIBLIBPMFDKKEBOABIMNLGNIDEABLPDBFGFHEJHJAHGJDFJNAIIAAGHLPKHLGALEIMPAJAPLDJGILFINNEKCO; f5avraaaaaaaaaaaaaaaa_session_=KCPMODJGNINMIDHJCOAMOEOHNDFPCEANOFMMEIHJJAAGGMJCOMACCIBLGACDNPFPBAGDLPEILDEEGPJHGFGAAMPOFJNFEHDOAFPFNHOGHOMNKGMILBKNJMIAMKDJKJHN',
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
        
        if i==1: #Number of pages to be scraped
            break
        
        i+=1
        time.sleep(2) #to avoid detection by the website
        #code to see the number of the page that is being scraped
        print(df["id"]) 
        get_details(df)

    df.to_excel('anuncios_request.xlsx', index=False,header=True )

# if __name__ == "__main__":
#     main()
