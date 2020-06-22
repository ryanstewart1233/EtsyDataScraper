import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


#returns a spreadsheet with item name, price, and status(e.g. if in someones basket)
def etsy_data(shop_name):


        shop_name=shop_name

        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        URL = "https://www.etsy.com/uk/shop/"+shop_name

        r=requests.get("https://www.etsy.com/uk/shop/"+shop_name, headers=headers)
        c=r.content
        soup = BeautifulSoup(c, 'html.parser')
        base_url = "https://www.etsy.com/uk/shop/"+shop_name+"?page="

        l=[]
        pg_nr=soup.find_all("p", {"class": "wt-action-group__item"})[0].text
        page_nr=str(pg_nr)[-2:]
        for page in range(1,(int(page_nr)+1)):
            #print(base_url+str(page)+"#items")
            r = requests.get(base_url+str(page)+"#items", headers=headers)
            c = r.content
            soup = BeautifulSoup(c, 'html.parser')
            all = soup.find_all("a", {"class":"display-inline-block listing-link"})
            for item in all:
                d={}
                try:
                    d["Product_Name"]=item.find_all("h3")[0].text.replace("\n", "").replace(" ", "")
                except:
                    d["Product_Name"]=None
                try:
                    d["Product_Price"]=item.find_all("span", {"class": "currency-value"})[0].text
                except:
                    d["Product_Price"]=None
                try:
                    d["Item_Status"]=item.find_all("div", {"class": "text-danger text-body-smaller"})[0].text.replace("\n", "")
                except:
                    d["Item_Status"]=None
                l.append(d)
        df=pd.DataFrame(l)
        df
        date=((str(datetime.now())[:10]) + " " + (str(datetime.now())[11:13]) + "-" + (str(datetime.now())[14:16]))
        global filename
        filename=(shop_name + date +".csv")
        df.to_csv(filename, index=False)
        

shop_name="NatureByHolly" #can change the shop name to whatever shop on etsy you want
etsy_data(shop_name)
