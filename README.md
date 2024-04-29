# AirBnB MongoDB Analysis

## Data Set Details
### Origin of the Data Set
The dataset used in this project comprises listing information from Airbnb for Munich, Bavaria, Germany. This data was obtained from [Inside Airbnb](http://insideairbnb.com/get-the-data.html), which provides publicly available information about listings for different cities around the world.

### Data Format
The original data file was in CSV format, compressed as a gzip file (`listings.csv.gz`). Upon download, the file was decompressed to a plain CSV format for further processing using Cyberduck.

### Raw Data Sample
Below is a display of the first 20 rows from the original data file.
| id        | listing_url                        | name                                      | host_name | neighbourhood_cleansed | room_type      | price   | minimum_nights | maximum_nights | number_of_reviews | review_scores_rating |
|-----------|------------------------------------|-------------------------------------------|-----------|------------------------|----------------|---------|----------------|----------------|-------------------|----------------------|
| 14726865  | https://www.airbnb.co...           | Rental unit in Munich · 1 bed...          | Ivana     | Neuhausen-Nymphenburg  | Shared room    | N/A     | 1              | 1125           | 0                 | N/A                  |
| 14976237  | https://www.airbnb.co...           | Rental unit in Munich · 3 bed...          | Sebas     | Laim                   | Entire home... | N/A     | 2              | 7              | 0                 | N/A                  |
| 15794305  | https://www.airbnb.co...           | Rental unit in Munich · 1 bed...          | Daniel    | Moosach                | Entire home... | N/A     | 7              | 1125           | 1                 | 5                    |
| 40839352  | https://www.airbnb.co...           | Rental unit in Munich · 1 bed...          | Stefan    | Altstadt-Lehel         | Entire home... | N/A     | 2              | 14             | 2                 | 5                    |
| 45776129  | https://www.airbnb.co...           | Rental unit in Munich · 2 bed...          | Alina     | Schwanthalerhöhe       | Entire home... | N/A     | 10             | 42             | 0                 | N/A                  |
| 42892910  | https://www.airbnb.co...           | Rental unit in Munich · 1 bed...          | Emre      | Milbertshofen-Am Hart  | Entire home... | $170.00 | 1              | 1125           | 1                 | 4                    |
| 43056523  | https://www.airbnb.co...           | Rental unit in Munich · 1 bed...          | Daniel    | Schwabing-West         | Entire home... | $250.00 | 8              | 29             | 2                 | 5                    |
| 50368493  | https://www.airbnb.co...           | Condo in Munich · ★4.54 · 1 b...          | Mashkur   | Ludwigsvorstadt-Isa... | Entire home... | N/A     | 3              | 365            | 13                | 4.54                 |
| 44336913  | https://www.airbnb.co...           | Rental unit in Munich · ★5.0 ...          | Torben    | Ludwigsvorstadt-Isa... | Entire home... | N/A     | 4              | 9              | 10                | 5                    |
| 38483614  | https://www.airbnb.co...           | Rental unit in Neubiberg · 2 ...          | Jäger     | Ramersdorf-Perlach     | Entire home... | $500.00 | 2              | 7              | 0                 | N/A                  |
| 44392308  | https://www.airbnb.co...           | Rental unit in Munich · ★4.80...          | Loris     | Schwabing-Freimann     | Entire home... | N/A     | 1              | 1125           | 5                 | 4.8                  |
| 31938634  | https://www.airbnb.co...           | Boutique hotel in Munich · 1 ...          | Bernd     | Schwanthalerhöhe       | Private room   | $999.00 | 5              | 30             | 0                 | N/A                  |
| 45020945  | https://www.airbnb.co...           | Rental unit in Munich · 3 bed...          | Sarah     | Schwabing-West         | Private room   | N/A     | 7              | 1125           | 1                 | 5                    |
| 883740269 | https://www.airbnb.co...           | Rental unit in Munich · 1 bed...          | Loic      | Au-Haidhausen          | Private room   | N/A     | 1              | 365            | 0                 | N/A                  |
| 32602783  | https://www.airbnb.co...           | Rental unit in Munich · ★5.0 ...          | Thomas    | Untergiesing-Harla...  | Private room   | $50.00  | 2              | 7              | 17                | 5                    |
| 28748441  | https://www.airbnb.co...           | Rental unit in Munich · ★4.90...          | Alex      | Aubing-Lochhausen...   | Private room   | N/A     | 1              | 1125           | 10                | 4.9                  |
| 970188922 | https://www.airbnb.co...           | Rental unit in Munich · ★3.0 ...          | Niklas    | Ludwigsvorstadt-Isa... | Entire home... | N/A     | 1              | 20             | 3                 | 3                    |
| 52137504  | https://www.airbnb.co...           | Rental unit in Munich · ★5.0 ...          | Jörg      | Au-Haidhausen          | Entire home... | N/A     | 5              | 180            | 3                 | 5                    |
| 703299636 | https://www.airbnb.co...           | Rental unit in Munich · 1 bed...          | Felix     | Neuhausen-Nymphenburg  | Entire home... | N/A     | 2              | 21             | 0                 | N/A                  |
| 104469860 | https://www.airbnb.co...           | Rental unit in Munich · ★New ...          | Alice     | Hadern                 | Entire home... | $97.00  | 3              | 365            | 0                 | N/A                  |

### Data Cleaning and Scrubbing
Empty Fields: Many fields contained empty strings or NaN values which were not suitable for analysis

Inconsistent Entries: Some text fields contained whitespace characters and non-standard symbols like '\u200b' and '\ufeff', which required normalization.

To prepare the data set for import into the MongoDB database, the following Python script was employed to clean and scrub the data:
'''
import csv

def clean_row(header, row, irrelevant_columns):
    cleaned = []
    for column, cell in zip(header, row):
        if column not in irrelevant_columns:
            # Normalize the cell string
            normalized_cell = cell.strip().replace('\u200b', '').replace('\ufeff', '')
            if normalized_cell.lower() in ['', 'n/a', 'nan', 'null', 'none', 'undefined',""]:
                cleaned.append(None)  # Use Python's None, which translates to null in MongoDB
            else:
                cleaned.append(normalized_cell)
    return cleaned

irrelevant_columns = [
    'scrape_id', 'last_scraped', 'source', 'neighborhood_overview',
    'picture_url', 'host_url', 'host_about', 'host_thumbnail_url',
    'host_picture_url', 'host_verifications', 'host_has_profile_pic',
    'neighbourhood_group_cleansed', 'bathrooms', 'bedrooms', 'amenities',
    'minimum_minimum_nights', 'maximum_minimum_nights', 'minimum_maximum_nights',
    'maximum_maximum_nights', 'minimum_nights_avg_ntm', 'maximum_nights_avg_ntm',
    'calendar_updated', 'has_availability', 'availability_30', 'availability_60',
    'availability_90', 'availability_365', 'calendar_last_scraped',
    'number_of_reviews_ltm', 'number_of_reviews_l30d', 'license'
]

try:
    with open('data/listings.csv', mode='r', encoding='utf-8') as f, \
         open('data/listings_clean.csv', mode='w', newline='', encoding='utf-8') as f_new:
        csv_reader = csv.reader(f)
        csv_writer = csv.writer(f_new)

        # Write the header without irrelevant columns
        header = next(csv_reader)
        cleaned_header = [column for column in header if column not in irrelevant_columns]
        csv_writer.writerow(cleaned_header)

        # Write the remaining rows without irrelevant columns
        for row in csv_reader:
            cleaned_row = clean_row(header, row, irrelevant_columns)
            csv_writer.writerow(cleaned_row)
except Exception as e:
    print(f"Error occurred: {e}")
'''

This script processes the original CSV file, removing unwanted columns and normalizing text entries, then saves the cleaned data to a new CSV file ready for database import. It was necessary to remove several columns that were either irrelevant to the analysis goals or contained mostly unusable data.

## Inital Terminal Code:
'''
mongoimport --headerline --type=csv --db=ss14744 --collection=listings --host=class-mongodb.cims.nyu.edu --file="/Users/sufiyahathena/Desktop/6-mongodb-analysis-sufiyahathena/data/listings_clean.csv" --username=ss14744 --password=TivqynMH
mongo --host class-mongodb.cims.nyu.edu --username ss14744 --password TivqynMH --authenticationDatabase ss14744
use ss14744
'''

## Data Analysis in MongoDB
### Query 1: Show exactly two documents from the listings collection in any order
MongoDB Command: db.listings.find().limit(2)
Description: The first query aims to provide a brief glimpse into the listings database by retrieving two documents.
Sample Results:
'''
{ "_id" : ObjectId("662fc40982d3bbe5a242e7f7"), "id" : 14726865, "listing_url" : "https://www.airbnb.com/rooms/14726865", "name" : "Rental unit in Munich · 1 bedroom · 1 bed · 1 shared bath", "description" : "", "host_id" : 91678611, "host_name" : "Ivana", "host_since" : "2016-08-24", "host_location" : "Munich, Germany", "host_response_time" : "", "host_response_rate" : "", "host_acceptance_rate" : "", "host_is_superhost" : "f", "host_neighbourhood" : "Neuhausen", "host_listings_count" : 1, "host_total_listings_count" : 1, "host_identity_verified" : "t", "neighbourhood" : "", "neighbourhood_cleansed" : "Neuhausen-Nymphenburg", "latitude" : 48.14569, "longitude" : 11.53166, "property_type" : "Shared room in rental unit", "room_type" : "Shared room", "accommodates" : 2, "bathrooms_text" : "1 shared bath", "beds" : 1, "price" : "", "minimum_nights" : 1, "maximum_nights" : 1125, "number_of_reviews" : 0, "first_review" : "", "last_review" : "", "review_scores_rating" : "", "review_scores_accuracy" : "", "review_scores_cleanliness" : "", "review_scores_checkin" : "", "review_scores_communication" : "", "review_scores_location" : "", "review_scores_value" : "", "instant_bookable" : "f", "calculated_host_listings_count" : 1, "calculated_host_listings_count_entire_homes" : 0, "calculated_host_listings_count_private_rooms" : 0, "calculated_host_listings_count_shared_rooms" : 1, "reviews_per_month" : "" }
{ "_id" : ObjectId("662fc40982d3bbe5a242e7f8"), "id" : 42892910, "listing_url" : "https://www.airbnb.com/rooms/42892910", "name" : "Rental unit in Munich · 1 bedroom · 1 bed · 1 bath", "description" : "", "host_id" : 318736185, "host_name" : "Emre", "host_since" : "2019-12-18", "host_location" : "İstanbul, Turkey", "host_response_time" : "", "host_response_rate" : "", "host_acceptance_rate" : "0%", "host_is_superhost" : "f", "host_neighbourhood" : "", "host_listings_count" : 1, "host_total_listings_count" : 1, "host_identity_verified" : "f", "neighbourhood" : "", "neighbourhood_cleansed" : "Milbertshofen-Am Hart", "latitude" : 48.20318, "longitude" : 11.56423, "property_type" : "Entire rental unit", "room_type" : "Entire home/apt", "accommodates" : 1, "bathrooms_text" : "1 bath", "beds" : 1, "price" : "$170.00", "minimum_nights" : 1, "maximum_nights" : 1125, "number_of_reviews" : 1, "first_review" : "2020-03-22", "last_review" : "2020-03-22", "review_scores_rating" : 4, "review_scores_accuracy" : 5, "review_scores_cleanliness" : 5, "review_scores_checkin" : 5, "review_scores_communication" : 5, "review_scores_location" : 5, "review_scores_value" : 4, "instant_bookable" : "f", "calculated_host_listings_count" : 1, "calculated_host_listings_count_entire_homes" : 1, "calculated_host_listings_count_private_rooms" : 0, "calculated_host_listings_count_shared_rooms" : 0, "reviews_per_month" : 0.02 }
'''
 The two listings shown highlight the diversity in the types of properties available. One is a fully private rental unit with three beds, while the other is a shared room, indicative of the variety in accommodation types in Munich. The listings are located in different neighborhoods ("Laim" and "Neuhausen-Nymphenburg"), suggesting geographic diversity. This could influence many factors such as price, demand, and host instructions. The presence of NaN or empty fields for price and review_scores_rating indicates missing information, which could be due to new listings or blanks in data collection. 

 ### Query 2: Viewing Ten Listings in a Readable Format
MongoDB Command: db.listings.find().limit(10).pretty()
Description: This query fetches ten documents from the listings collection, using the pretty() function to format the output.
Sample Results:
'''
{
        "_id" : ObjectId("662fc40982d3bbe5a242e7fd"),
        "id" : 50368493,
        "listing_url" : "https://www.airbnb.com/rooms/50368493",
        "name" : "Condo in Munich · ★4.54 · 1 bedroom · 1 bath",
        "description" : "",
        "host_id" : 311212245,
        "host_name" : "Mashkur",
        "host_since" : "2019-11-21",
        "host_location" : "Munich, Germany",
        "host_response_time" : "",
        "host_response_rate" : "",
        "host_acceptance_rate" : "",
        "host_is_superhost" : "f",
        "host_neighbourhood" : "",
        "host_listings_count" : 1,
        "host_total_listings_count" : 1,
        "host_identity_verified" : "t",
        "neighbourhood" : "",
        "neighbourhood_cleansed" : "Ludwigsvorstadt-Isarvorstadt",
        "latitude" : 48.13133,
        "longitude" : 11.56511,
        "property_type" : "Entire condo",
        "room_type" : "Entire home/apt",
        "accommodates" : 2,
        "bathrooms_text" : "1 bath",
        "beds" : "",
        "price" : "",
        "minimum_nights" : 3,
        "maximum_nights" : 365,
        "number_of_reviews" : 13,
        "first_review" : "2021-07-06",
        "last_review" : "2022-10-04",
        "review_scores_rating" : 4.54,
        "review_scores_accuracy" : 4.62,
        "review_scores_cleanliness" : 4,
        "review_scores_checkin" : 4.46,
        "review_scores_communication" : 4.77,
        "review_scores_location" : 4.92,
        "review_scores_value" : 4.38,
        "instant_bookable" : "f",
        "calculated_host_listings_count" : 1,
        "calculated_host_listings_count_entire_homes" : 1,
        "calculated_host_listings_count_private_rooms" : 0,
        "calculated_host_listings_count_shared_rooms" : 0,
        "reviews_per_month" : 0.43
}
{
        "_id" : ObjectId("662fc40982d3bbe5a242e7fe"),
        "id" : 38483614,
        "listing_url" : "https://www.airbnb.com/rooms/38483614",
        "name" : "Rental unit in Neubiberg · 1 bedroom · 2 beds · 1 bath",
        "description" : "",
        "host_id" : 89547245,
        "host_name" : "Jäger",
        "host_since" : "2016-08-12",
        "host_location" : "",
        "host_response_time" : "",
        "host_response_rate" : "",
        "host_acceptance_rate" : "",
        "host_is_superhost" : "f",
        "host_neighbourhood" : "",
        "host_listings_count" : 1,
        "host_total_listings_count" : 1,
        "host_identity_verified" : "f",
        "neighbourhood" : "",
        "neighbourhood_cleansed" : "Ramersdorf-Perlach",
        "latitude" : 48.07795,
        "longitude" : 11.68178,
        "property_type" : "Entire rental unit",
        "room_type" : "Entire home/apt",
        "accommodates" : 2,
        "bathrooms_text" : "1 bath",
        "beds" : 2,
        "price" : "$500.00",
        "minimum_nights" : 2,
        "maximum_nights" : 7,
        "number_of_reviews" : 0,
        "first_review" : "",
        "last_review" : "",
        "review_scores_rating" : "",
        "review_scores_accuracy" : "",
        "review_scores_cleanliness" : "",
        "review_scores_checkin" : "",
        "review_scores_communication" : "",
        "review_scores_location" : "",
        "review_scores_value" : "",
        "instant_bookable" : "f",
        "calculated_host_listings_count" : 1,
        "calculated_host_listings_count_entire_homes" : 1,
        "calculated_host_listings_count_private_rooms" : 0,
        "calculated_host_listings_count_shared_rooms" : 0,
        "reviews_per_month" : ""
}
{
        "_id" : ObjectId("662fc40982d3bbe5a242e7ff"),
        "id" : 44392308,
        "listing_url" : "https://www.airbnb.com/rooms/44392308",
        "name" : "Rental unit in Munich · ★4.80 · Studio · 1 bed · 1 bath",
        "description" : "",
        "host_id" : 58331101,
        "host_name" : "Loris",
        "host_since" : "2016-02-11",
        "host_location" : "Gauting, Germany",
        "host_response_time" : "",
        "host_response_rate" : "",
        "host_acceptance_rate" : "",
        "host_is_superhost" : "f",
        "host_neighbourhood" : "",
        "host_listings_count" : 1,
        "host_total_listings_count" : 1,
        "host_identity_verified" : "t",
        "neighbourhood" : "",
        "neighbourhood_cleansed" : "Schwabing-Freimann",
        "latitude" : 48.16268,
        "longitude" : 11.58832,
        "property_type" : "Entire rental unit",
        "room_type" : "Entire home/apt",
        "accommodates" : 2,
        "bathrooms_text" : "1 bath",
        "beds" : 1,
        "price" : "",
        "minimum_nights" : 1,
        "maximum_nights" : 1125,
        "number_of_reviews" : 5,
        "first_review" : "2020-09-02",
        "last_review" : "2020-11-08",
        "review_scores_rating" : 4.8,
        "review_scores_accuracy" : 5,
        "review_scores_cleanliness" : 4.4,
        "review_scores_checkin" : 5,
        "review_scores_communication" : 5,
        "review_scores_location" : 5,
        "review_scores_value" : 4.4,
        "instant_bookable" : "t",
        "calculated_host_listings_count" : 1,
        "calculated_host_listings_count_entire_homes" : 1,
        "calculated_host_listings_count_private_rooms" : 0,
        "calculated_host_listings_count_shared_rooms" : 0,
        "reviews_per_month" : 0.12
}
'''
Each listing varies significantly in terms of amenities, price, and the number of nights required for booking, indicating a broad range of options tailored to different traveler needs and preferences. some listings have very few or no reviews, which could suggest newer listings or less frequent usage. This could be an opportunity for new hosts to capture market share or an indication of less popular properties.

### Query 3: Retrieving listings from two specific superhosts
MongoDB Commands: db.listings.find({host_is_superhost: "t"}, {host_id: 1, host_name: 1, _id: 0}).limit(5)
db.listings.find(
    {
        $or: [
            {host_id: 22183201},
            {host_id: 57502061}
        ],
        host_is_superhost: "t"
    },
    {
        name: 1,
        price: 1,
        neighbourhood: 1,
        host_name: 1,
        host_is_superhost: 1,
        _id: 0
    }
)
Description: This query retrieves listings from two superhosts, Jordy and Thomas, by filtering based on their respective host_ids. The results include only the name, price, neighbourhood, host_name, and host_is_superhost fields to focus on the most relevant information.
Sample Results:
{ "name" : "Rental unit in Munich · ★5.0 · 1 bedroom · 1 bed · 1 private bath", "host_name" : "Jordy", "host_is_superhost" : "t", "neighbourhood" : "", "price" : "" }
{ "name" : "Condo in Munich · ★5.0 · 1 bedroom · 1 bed · 1 shared bath", "host_name" : "Thomas", "host_is_superhost" : "t", "neighbourhood" : "", "price" : "$120.00" }
{ "name" : "Rental unit in Munich · ★5.0 · 1 bedroom · 2 beds · 1 bath", "host_name" : "Jordy", "host_is_superhost" : "t", "neighbourhood" : "", "price" : "$100.00" }
{ "name" : "Condo in Munich · ★4.83 · 1 bedroom · 1 bed · 1 shared bath", "host_name" : "Thomas", "host_is_superhost" : "t", "neighbourhood" : "", "price" : "" }

The listings showcase a variety of options in terms of space and accommodation types for both Jordy and Thomas who have two listed Airbnb's each.  For each super host they have one listing with visible prices which could indicate new listings or  incomplete data entries.

### Query 4:  Find all the unique host_name values
MongoDB Commands: db.listings.distinct("host_name")
Description: This command retrieves a list of all unique host names from the listings collection.
Sample Results:
Random snippet of unique host names
 "Pepe",
 "Pepijn",
"Pere",
"Perrine",
"Peter",
"Petra",
"Petra Andrea",
"Phil",
"Philip",

This result helps in analyzing the distribution of listings among different hosts, identifying top hosts, or simply understanding the scale of individual operations within the dataset.

### Query 5: Listings with More Than 2 Beds in a Selected Neighborhood, Ordered by Review Scores
MongoDB Command: 
db.listings.find(
    {
        $and: [
            {beds: {$gt: 2}},
            {neighbourhood_cleansed: "Schwabing-West"}, 
            {review_scores_rating: {$ne: null}} 
        ]
    },
    {
        name: 1,
        beds: 1,
        review_scores_rating: 1,
        price: 1,
        _id: 0
    }
).sort({review_scores_rating: -1})
Description: This query searches for listings within the "Schwabing-West" neighborhood that have more than two beds. It also filters out any listings that do not have a review score rating to avoid null values in the output. The results are sorted by review_scores_rating in descending order, ensuring that the highest-rated listings appear first. The query specifically returns the listing's name, number of beds, review scores rating, and price.
Sample Results:
{ "name" : "Condo in Munich · ★5.0 · 3 bedrooms · 3 beds · 2 baths", "beds" : 3, "price" : "$485.00", "review_scores_rating" : 5 }
{ "name" : "Rental unit in Munich · 3 bedrooms · 6 beds · 1.5 baths", "beds" : 6, "price" : "$850.00", "review_scores_rating" : 5 }
{ "name" : "Rental unit in Munich · ★5.0 · 3 bedrooms · 3 beds · 1.5 baths", "beds" : 3, "price" : "$383.00", "review_scores_rating" : 5 }
{ "name" : "Condo in Munich · ★5.0 · 2 bedrooms · 3 beds · 1.5 baths", "beds" : 3, "price" : "$210.00", "review_scores_rating" : 5 }
{ "name" : "Condo in Munich · 3 bedrooms · 4 beds · 2 baths", "beds" : 4, "price" : "$198.00", "review_scores_rating" : 5 }
{ "name" : "Rental unit in Munich · ★5.0 · 1 bedroom · 3 beds · 1 bath", "beds" : 3, "price" : "$150.00", "review_scores_rating" : 5 }

The data retrieved from the query highlights the availability and characteristics of larger accommodation options in the Schwabing-West neighborhood of Munich, which are capable of hosting larger groups due to the number of beds available (more than two). The pricing for these listings varies significantly, ranging from as low as $42.00 to as high as $850.00 per night. The types of properties range from condos to rental units, offering various living experiences. There appears to be a correlation between the number of beds, review scores, and pricing. Listings with higher review scores and more beds tend to command higher prices, reflecting the premium that guests are willing to pay for quality assured by other travelers’ experiences.

### Query 6: Number of listings per host
MongoDB Command:
db.listings.aggregate([
    {
        $group: {
            _id: "$host_id",  // Group by host ID
            totalListings: { $sum: 1 }  
        }
    },
    {
        $project: {
            _id: 0,  // Do not show the _id field in the final output
            host_id: "$_id",  // Show the host_id as 'host_id'
            totalListings: 1  // Include the count of listings
        }
    },
    {
        $sort: { totalListings: -1 }  
    }
])
Description: This query aggregates the listings by the host_id, counting the number of listings each host has under their profile. The results are then projected to exclude MongoDB's default _id field and rename the group identifier _id to host_id. Then sorted the results to see the hosts with the most listings at the top.
Sample Results:
{ "totalListings" : 152, "host_id" : 376961462 }
{ "totalListings" : 66, "host_id" : 205832270 }
{ "totalListings" : 52, "host_id" : 395880389 }
{ "totalListings" : 46, "host_id" : 51557252 }
{ "totalListings" : 38, "host_id" : 164225004 }
{ "totalListings" : 36, "host_id" : 549372436 }
{ "totalListings" : 32, "host_id" : 2266917 }
{ "totalListings" : 30, "host_id" : 512924239 }
{ "totalListings" : 30, "host_id" : 373004900 }
{ "totalListings" : 28, "host_id" : 175608026 }
{ "totalListings" : 28, "host_id" : 308052561 }
{ "totalListings" : 26, "host_id" : 7901771 }

 A few hosts manage a large number of listings, which might indicate professional or semi-professional property management involvement. Hosts with high numbers of listings could potentially offer diverse types of accommodations, impacting their responsiveness and the quality of service due to the scale of operations.

 ### Query 7: Average Review Scores Rating Per Neighborhood
 MongoDB Command:
 db.listings.aggregate([
    {
        $match: {
            review_scores_rating: { $gte: 4 }
        }
    },
    {
        $group: {
            _id: "$neighbourhood_cleansed",
            averageRating: { $avg: "$review_scores_rating" }
        }
    },
    {
        $match: {
            averageRating: { $gte: 4 }
        }
    },
    {
        $sort: { averageRating: -1 }
    },
    {
        $project: {
            _id: 0,
            neighbourhood: "$_id",
            averageRating: 1
        }
    }
])
Description: This query calculates the average review scores rating for each neighborhood where the rating is 4 or above. It first filters listings with a review score of 4 or higher, groups them by neighborhood, calculates the average rating for each neighborhood, filters those with an average rating of 4 or higher, and finally sorts them in descending order of the average rating. The results show only the neighborhood and the computed average rating.
Sample Results:
{ "averageRating" : 4.92, "neighbourhood" : "Allach-Untermenzing" }
{ "averageRating" : 4.867088235294117, "neighbourhood" : "Au-Haidhausen" }
{ "averageRating" : 4.859213114754098, "neighbourhood" : "Neuhausen-Nymphenburg" }
{ "averageRating" : 4.8515999999999995, "neighbourhood" : "Schwanthalerhöhe" }
{ "averageRating" : 4.8466956521739135, "neighbourhood" : "Bogenhausen" }
{ "averageRating" : 4.832794117647059, "neighbourhood" : "Untergiesing-Harlaching" }
{ "averageRating" : 4.8320454545454545, "neighbourhood" : "Pasing-Obermenzing" }
{ "averageRating" : 4.829354838709677, "neighbourhood" : "Tudering-Riem" }
{ "averageRating" : 4.823296703296704, "neighbourhood" : "Altstadt-Lehel" }
{ "averageRating" : 4.823203883495145, "neighbourhood" : "Schwabing-West" }

The results from this query provide a comprehensive overview of customer satisfaction across different neighborhoods in Munich, specifically highlighting those with an average review score of 4 or above. This query is especially useful for identifying which neighborhoods host the most well-received listings, which can be indicative of both desirable living areas and effective hosting. Neighborhoods like Allach-Untermenzing and Neuhausen-Nymphenburg score particularly high, suggesting that these more residential areas might offer qualities that are highly valued by guests, such as quiet, space, and perhaps more personalized hospitality. Airbnb itself or local tourism boards might use this data to promote certain neighborhoods as ideal places to stay, based on guest satisfaction. 