from selectorlib import Extractor
import requests 
from time import sleep
import csv
import os
from datetime import datetime
from datetime import date

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
e = Extractor.from_yaml_file(__location__+'/keys.yml')

def inputDate(inDate):
    '''Input the date for search'''
    format='%d-%m-%Y'
    startDate=inDate
    try:
        startDate=datetime.strptime(startDate,format)
    except:
        print("Date is not in desired format [DD-MM-YYYY]")
    day=startDate.day
    month=str(startDate.month)
    datetime_object = datetime.strptime(month, "%m")
    month_name = datetime_object.strftime("%b")
    year=startDate.year
    today=datetime.today()
    if startDate < today:
        print("Selected a future date for booking.")
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
    #day=f"{day:02d}"
    #monthNum=f"{int(monthNum):02d}"
    return str(day), str(month), str(year)

def contInput():
    '''Check to Continue'''
    contInput=input("\nPress [C] to continue or [Q] to exit or [R] to reneter the date: ")
    contIn=str(contInput)
    if ( contIn=='Q'):
        exit()
    else:
        if ( contIn=='R'):
            inputDate()
        else:
            if (contIn=='C'):
                return
            else:
                try:
                   contInput()
                except:
                    contInput()

def paerseURL():
    checkInDate=input("Enter the Checkin Date [DD-MM-YYYY]: ")
    checkInDay,cInMonth,cInYear=inputDate(cInDate)
    checkOutDate=input("Enter the Checkout Date [DD-MM-YYYY]: ")
    checkOutDay,cOutMonth,cOutYear=inputDate(cOutDate)
    location=input("Enter the location: ")
    adults=input("Enter the number of Adults: ")
    child=input("Enter the number of Children: ")
    rooms=input("Enter the number of rooms required: ")
    return location,checkInYear,checkInMonth,checkInDay,checkOutYear,checkOutMonth,checkOutDay,adults,child,rooms

def scrape(url):    
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://www.booking.com/index.en-gb.html',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }


    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
  
    return e.extract(r.text,base_url=url)


def main():
    data=paerseURL()
    url='https://www.booking.com/searchresults.en-gb.html?&ss='+data[0]+'&is_ski_area=&checkin_year='+data[1]+'&checkin_month='+data[2]+'&checkin_monthday='+data[3]+'&checkout_year='+data[4]+'&checkout_month='+data[5]+'&checkout_monthday='+data[6]+'&group_adults='+data[7]+'&group_children='+data[8]+'&no_rooms='+data[9]+'&b_h4u_keep_filters=&from_sf=1&search_pageview_id=34a1631d5bd40123&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0&ac_position=0&ac_langcode=en&order=price'
    
    with open(__location__+'/data.csv','w') as outfile:
        fieldnames = [
            "name",
            "location",
            "price",
            "price_for",
            "room_type",
            "beds",
            "rating",
            "rating_title",
            "number_of_ratings",
            "url"
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
        writer.writeheader()
        data = scrape(url) 
        
        if data:
            for h in data['hotels']:
                writer.writerow(h)

if __name__ == "__main__":
    main()
