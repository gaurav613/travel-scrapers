# travel-scrapers
Scraping flight and hotel data from MakeMyTrip and TripAdvisor in Python

**Running Scrapers**
* Flight Scraper: done using Selenium & BeautifulSoup4
  * `python flightscraper.py  <Date> <From> <To> <No. of adults> <No.of Children> <Flight Class(B/E)>`  
  * Date format: DD/MM/YYY
  * From and To values must be airport codes for the cities(e.g., Toronto would be YYZ, New York would be JFK).

* Hotel Scraper: done using Requests 
  * `python hotelscraper.py "checkInDate" "checkOutDate" "sortby" "city"`
  * Date format: YYYY/MM/DD
  * Data can be sorted by `popularity` or `price`.

Data stored in .csv format  
