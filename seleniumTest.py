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
	with open('hasDNSMPI.csv', 'w', newline='') as writeFile:
		fieldnames = ['urlNum', 'urlStr', 'hasDNSMPI']
		writer = csv.DictWriter(writeFile, fieldnames=fieldnames)

		writer.writeheader()
		for dbURL in sl:
			print("dbURL #" + str(i) + ": " + dbURL)
			try:
				driver.get(dbURL)
				get_source = driver.page_source
				# TODO: Need to make page search more robust to catch various terms/cases etc
				search_text = "Do Not Sell My Personal Information"
				hDNSMPI = search_text in get_source
				print(hDNSMPI)
				writer.writerow({'urlNum': i, 'urlStr': dbURL, 'hasDNSMPI': hDNSMPI})
			except:
				print("An exception occured when loading: " + dbURL)
				writer.writerow({'urlNum': i, 'urlStr': dbURL, 'hasDNSMPI': 'Err'})
			print()
			i += 1
	driver.quit()

if __name__ == "__main__":
	checkForDNSMPI()