from selectorlib import Extractor
import requests 
from time import sleep
import csv
import os
from datetime import datetime
from datetime import date

# Create an Extractor by reading from the YAML file
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
    chkDay=day%10
    if chkDay==1:
        print("The date entered is {}st day of {} in {}. \n".format(day,month_name,year))
        contInput()
    else:
        if chkDay==2:
            print("The date entered is {}nd day of {} in {}. \n".format(day,month_name,year))
            contInput()
        else:
            if chkDay==3:
                print("The date entered is {}rd day of {} in {}. \n".format(day,month_name,year))
                contInput()
            else:
                print("The date entered is {}th day of {} in {}. \n".format(day,month_name,year))
                contInput()
    #day=f"{day:02d}"
    #monthNum=f"{int(monthNum):02d}"
    return str(day), str(monthNum), str(year)

def contInput():
    '''Check to Continue'''
    contInput=input("\nPress [c/C] to continue or [q/Q] to exit or [r/R] to reneter the date: ")
    contIn=str(contInput)
    if (contIn=='q' or contIn=='Q'):
        exit()
    else:
        if (contIn=='r' or contIn=='R'):
            inputDate()
        else:
            if (contIn=='c' or contIn=='C'):
                return
            else:
                try:
                   contInput()
                except:
                    contInput()

def parseURL():
    tInDate=input("Enter the Traveling Date [DD/MM/YYYY]: ")
    tInDay,tInMonth,tInYear=inputDate(tInDate)
    origin=input("Enter the Orgin Airport Code: ")
    destination=input("Enter the Destination Airport Code: ")
    adults=input("Enter the number of Adults: ")
    child=input("Enter the number of Children (age betweem 5 and 18): ")
    infant=input("Enter the number of Infants: ")
    return origin,destination,tInDate,adults,child,infant

def scrape(url):    
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache, , max-age=0, must-revalidate, no-store',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        # You may want to change the user agent if you get blocked
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-encoding': 'gzip, deflate, br',
        'Accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,',
        'Referer': 'https://www.makemytrip.com/'
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    print (r)
    #r = requests.get(url)
    # Pass the HTML of the page and create 
    return e.extract(r.text,base_url=url)


def main():
    data=parseURL()
    url='https://www.makemytrip.com/flight/search?tripType=1&itinerary='+data[0]+'-'+data[1]+'-'+data[2]+'&paxType=A-'+data[3]+'_C-'+data[4]+'_I-'+data[5]+'&cabinClass=E'
    #print(urlTemplate.format(paerseURL()))
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