#Project-Web scraper using Beautiful soup and requests
import requests   #getting webpage(here html) content
from bs4 import BeautifulSoup   #for parsing the html code
import pandas
import argparse
import connect

parser = argparse.ArgumentParser()
parser.add_argument("--page_num_max", help="Enter the number of pages to parse", type=int)
parser.add_argument("--dbname", help="Enter the number of pages to parse", type=char)
args = parser.parse_args()

page_num_max = 3
oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="
scraped_info_list=[]
connect.connect(args.dbname)


for page_num in range(1,page_num_max):
    req = requests.get(oyo_url+str(page_num))  #creates a request object 'req'
    content = req.content        # accessing the content using req object


    soup = BeautifulSoup(content,"html.parser") #parsing the content
    all_hotels = soup.find_all("div",{"class":"hotelCardListing"})


    for hotel in all_hotels:
        hotel_dict={}
        hotel_dict["name"] = hotel.find("h3",{"class":"listingHotelDescription__hotelName"}).text
        hotel_dict["adress"] = hotel.find("span",{"itemprop":"streetAddress"}).text
        hotel_dict["price"] = hotel.find("span",{"class":"listingPrice__finalPrice"}).text


    #try to neglect empty Attribute
        try:
            hotel_dict["rating"] = hotel.find("span",{"class":"hostelRating__ratingSummary"}).text
        except AttributeError:
            hotel_dict["rating"] = None


        amenities_list = []
        parent_amenities = hotel.find("div",{"class":"amenityWrapper"})
        for amenity in parent_amenities.find_all("div",{"class":"amenityWrapper__amenity"}):
            amenities_list.append(amenity.find("span",{"class":"d-body-sm"}).text)
        hotel_dict["amenities"] = ', '.join(amenities_list[:-1])

        scraped_info_list.append(hotel_dict)
        #print(hotel_name,hotel_address,hotel_price,hotel_rating,amenities_list)
        connect.insert_into_table(args.dbname,tuple(hotel_dict.values()))


dataFrame = pandas.DataFrame(scraped_info_list)
dataFrame.to_csv("Oyo.csv")
connect.get_hotel_info(dbname)
