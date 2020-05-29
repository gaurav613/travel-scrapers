# Required module imports
import sys
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# User defined variables for data retreival
origin = sys.argv[1]				# Origin airport code
destin = sys.argv[2]				# Destination airport code
trDate = sys.argv[3]		# Date as 1st command line argument.
adults = sys.argv[4]
children = sys.argv[5]
premium = sys.argv[6]	# E,PE,B,F


# url to display data
baseDataUrl = "https://www.makemytrip.com/flight/search?itinerary="+ origin +"-"+ destin +"-"+ trDate +"&tripType=O&paxType=A-"+adults+"_C-"+children+"_I-0&intl=true&cabinClass="+premium

try:
	# webdriver.Chrome(ChromeDriverManager().install())
	driver = webdriver.Chrome(executable_path="C:\\Users\\Gaurav\\Downloads\\chromedriver_win32\\chromedriver.exe") # Chrome driver is being used.
	 
	print ("Requesting URL: " + baseDataUrl)

	driver.get(baseDataUrl)  			 # URL requested in browser.
	print ("Webpage found ...")

	element_xpath = '//*[@id="left-side--wrapper"]/div[2]' # First box with relevant flight data.

	# Wait until the first box with relevant flight data appears on Screen
	element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))

	# Scroll the page till bottom to get full data available in the DOM.
	print ("Scrolling document upto bottom ...")
	for j in range(1, 100):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	# Find the document body and get its inner HTML for processing in BeautifulSoup parser.
	body = driver.find_element_by_tag_name("body").get_attribute("innerHTML")

	print("Closing Chrome ...") # No more usage needed.
	driver.quit() 				# Browser Closed.

	print("Getting data from DOM ...")
	soupBody = BeautifulSoup(body,'html') # Parse the inner HTML using BeautifulSoup

	# Extract the required tags 
	spanFlightName = soupBody.find_all("span", "airways-name") 			# Tags with Flight Name
	pFlightCode = soupBody.find_all("span",  "pull-left flight-name")				# Tags with Flight Code
	divDeptTime = soupBody.find_all("div","dept-time")				# Tags with Departure Time
	pDeptCity = soupBody.find_all("p","dept-city")				# Tags with Departure City
	pFlightDuration = soupBody.find_all("p", "fli-duration")			# Tags with Flight Duration
	pArrivalTime = soupBody.find_all("p", "reaching-time append_bottom3") 	# Tags with Arrival Time
	pArrivalCity = soupBody.find_all("p",  "arrival-city")				# Tags with Arrival City
	spanFlightCost = soupBody.find_all("span", "actual-price")			# Tags with Flight Cost
	pLayovers = soupBody.find_all("p","fli-stops-desc")                 # Tags with flight Layovers
	pDeptDate = soupBody.find_all("span","pull-left flight_details__flinam") #Departure Date
	
	# Data Headers
	flightsData = []
	flight_details = ["airlines" , "flight_details", "departure_time", "departure_city", "departure_date","flight_duration", "arrival_time", "arrival_city", "flight_cost", "layovers"]

	# Extracting data from tags and appending to main database flightsData
	for j in range(0, len(spanFlightName)):
		flightsData.append([spanFlightName[j].text, pFlightCode[j].text, divDeptTime[j].text, pDeptCity[j].text, pDeptDate[j].text, pFlightDuration[j].text, pArrivalTime[j].text, pArrivalCity[j].text, spanFlightCost[j].text, pLayovers[j].text])

	# # Output File for FlightsData. This file will have the data in comma separated form.
	outputFile = "FlightsData_" + origin +"-"+ destin +"-"+ trDate.split("/")[0] + "-" + trDate.split("/")[1] + "-" + trDate.split("/")[2] + ".csv"
	
	# Publishing Data to File
	print("Writing flight data to file: "+ outputFile + " ...")
    # Convert to pandas dataframe
	flight_Df = pd.DataFrame(flightsData,columns=flight_details)
	flight_Df['flight_cost'] = flight_Df['flight_cost'].map(lambda x: ''.join([i for i in x if i.isdigit()])).astype(int)*0.013
	no_of_days = []
	for i in range(0, len(spanFlightName)):
		flight_Df['departure_date'][i] = flight_Df['departure_date'][i].split(',')[1]
		time_string = flight_Df['arrival_time'][i].split(' ')[0]
		if '+' in time_string:
			no_of_days.append(time_string.split('+')[1])
			flight_Df['arrival_time'][i] = time_string.split('+')[0]
		else:
			flight_Df['arrival_time'][i] = time_string
			no_of_days.append('Same day')
	
	flight_Df.insert(3,"no_of_days",no_of_days)
	
	flight_Df.to_csv("flight_data\\"+outputFile,index=False)

except Exception as e:
	print (str(e))
