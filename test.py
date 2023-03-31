from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

def loadDBCSV():
	siteList = []
	with open('data-broker.csv', newline='') as csvfile:
		csvReader = csv.reader(csvfile, delimiter=',')
		for row in csvReader:
			siteList.append(row[2])
	return siteList



#################################
# Terms used for opt out buttons
# - "Do Not Sell My Personal Information" in Element Text
# - Do not sell my personal information as text but requires clicking privacy policy link
#########
def checkForDNSMPI():
	driver = webdriver.Chrome()
	sl = loadDBCSV()
	i = 0
	for dbURL in sl:
		print("dbURL #" + str(i) + ": " + dbURL)
		try:
			driver.get(dbURL)
			get_source = driver.page_source
			search_text = "Do Not Sell My Personal Information"
			print(search_text in get_source)
		except:
			print("An exception occured when loading: " + dbURL)
		print()
		i += 1
	driver.quit()

if __name__ == "__main__":
	checkForDNSMPI()