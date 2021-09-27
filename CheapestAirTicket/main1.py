from selectorlib import Extractor
import requests 
from time import sleep
from datetime import datetime
from datetime import date
import os
import csv


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

e = Extractor.from_yaml_file(__location__+'/keys.yml')
print (e)

def inputDate(inDate):
    '''Input the date for search'''
    format='%d/%m/%Y'
    sDate=inDate
    
    try:
        sDate=datetime.strptime(sDate,format)
    except:
        print("Date is not in desired format [DD-MM-YYYY]")
    
    day=sDate.day
    
    monthNum=str(sDate.month)
    
    datetime_object = datetime.strptime(monthNum, "%m")
    
    month_name = datetime_object.strftime("%b")
    
    year=sDate.year
    
    today=datetime.today()
    
    if sDate < today:
        print("Selected a future date.")
        contInput()
    
    checkDay=day%10
    
    if checkDay==1:
        print("The date entered is {}st day of {} in {}. \n".format(day,month_name,year))
        contInput()
    
    else:
        if checkDay==2:
            print("The date entered is {}nd day of {} in {}. \n".format(day,month_name,year))
            contInput()
        
        else:
            if checkDay==3:
                print("The date entered is {}rd day of {} in {}. \n".format(day,month_name,year))
                contInput()
        
        else:
                print("The date entered is {}th day of {} in {}. \n".format(day,month_name,year))
                contInput()
    
    return str(day), str(monthNum), str(year)

def contInput():
    '''Check to Continue'''
    contInput=input("\nPress [C] to continue or [Q] to exit or [R] to reneter the date: ")
    contIn=str(contInput)
    
    if ( contIn=='Q'):
        exit()
    
    else:
        if (  contIn=='R'):
            inputDate()
        
        else:
            if ( contIn=='C'):
                return
            
            else:
                try:
                   contInput()
                except:
                    contInput()

def parseURL():
    tInDate=input("Enter the date on which you have to travel [DD/MM/YYYY]: ")
    tInDay,tInMonth,tInYear=inputDate(tInDate)
    airport=input("Enter the code for airport from where you are gonna start the journey: ")
    destination=input("Enter the code for Destination Airport : ")
    adult=input("Enter the number of Adults who are going to travel: ")
    child=input("Enter the number of Children going to travel: ")
    infant=input("number of Infants: ")
    return origin,destination,tInDate,adults,child,infant

def scrape(url):    
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache, , max-age=0, must-revalidate, no-store',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-encoding': 'gzip, deflate, br',
        'Accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,',
        'Referer': 'https://www.makemytrip.com/'
    }

    
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    print (r)
    
    return e.extract(r.text,base_url=url)


def main():
    data=parseURL()
    url='https://www.makemytrip.com/flight/search?tripType=1&itinerary='+data[0]+'-'+data[1]+'-'+data[2]+'&paxType=A-'+data[3]+'_C-'+data[4]+'_I-'+data[5]+'&cabinClass=E'
    
    with open(__location__+'/data.csv','w') as outfile:
        fieldnames = [
            "name",
            "depart",
            "arrive",
            "price",
            "travel",
            "stops"
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
        writer.writeheader()
        data = scrape(url)
        print (data)
        if data:
            for h in data['Listing']:
                writer.writerow(h)

if __name__ == "__main__":
    main()
