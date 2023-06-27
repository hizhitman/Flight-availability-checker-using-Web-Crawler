# Required module imports
import csv #to export data
import sys
import selenium.webdriver 
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# User defined variables for data retreival
origin = "BOM" 		#Find three letter abbrevs for all cities		#For departure city u need to find the three letter code	
destin = "DEL" 			 #For arrival city u find the three letter code	
trDate = "28/06/2023"			#You can enter any date in this format

baseDataUrl = "https://www.makemytrip.com/flight/search?itinerary="+ origin +"-"+ destin +"-"+ trDate +"&tripType=O&paxType=A-1_C-0_I-0&intl=false&=&cabinClass=E"

try:
    driver = selenium.webdriver.Chrome() # Chrome driver is being used.
    print ("Opening URL: " + baseDataUrl)

    driver.get(baseDataUrl)  			 # URL requested in browser.


    element_xpath = '//*[@id="left-side--wrapper"]/div[2]' # First box with relevant flight data.

        # Wait until the first box with relevant flight data appears on Screen
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, element_xpath))) #This solves the nosuchelement found error


    for j in range(1, 1000): #Scrolling through the whole webpage
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    body = driver.find_element(By.TAG_NAME,"body").get_attribute("innerHTML") 

   # element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "body")))


    driver.quit() 			

    soupBody = BeautifulSoup(body, features="html.parser")

    #spanFlightName = soupBody.find_all(lambda tag: tag.name == 'p' and tag.get('class') == ['boldFont blackText airlineName']) #alternate syntax


    spanFlightName=soupBody.findAll("p", class_="boldFont blackText airlineName")
    spanFlightCost = soupBody.findAll("div", class_= "blackText fontSize18 blackFont white-space-no-wrap")
    layover = soupBody.findAll("p", class_= "flightsLayoverInfo")
    time = soupBody.findAll("p", class_= "appendBottom2 flightTimeInfo")
    '''print([div.text for div in spanFlightName])	
    print([div.text for div in spanFlightCost])# Tags with Flight Name
    print([div.text for div in layover])
    print([div.text for div in time])	'''
    
        
        # Data Headers
    flightsData=[["DEPARTURE: "+origin+" ARRIVAL: "+destin+" DATE OF DEPARTURE: "+trDate]]
    flightsData.append(["flight_name", "flight_cost", "layover","departure_time" ])
    

        # Extracting data from tags and appending to main database flightsData
    for j in range(0, len(spanFlightName)):
        flightsData.append([spanFlightName[j].text,spanFlightCost[j].text,layover [j].text,time[j].text])
        # Output File for FlightsData. This file will have the data in comma separated form.
    outputFile = "FlightsData_" + origin +"-"+ destin +"-"+ trDate.split("/")[0] + "-" + trDate.split("/")[1] + "-" + trDate.split("/")[2] + ".csv"
        
        # Publishing Data to File
    print("Writing all available data to file: "+ outputFile)
    with open(outputFile, 'w', newline='') as spfile:
        csv_writer = csv.writer(spfile)
        csv_writer.writerows(flightsData)

        print ("Data Extracted and Saved to File. ")

except IndexError and Exception as e:
	print(str(e))