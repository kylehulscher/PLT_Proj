from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import csv

# Requires python packages selenium, bs4, lxml, requests, csv
# I installed using pip

def loadDBCSV():
	siteList = []
	with open('data-broker.csv', newline='') as csvfile:
		csvReader = csv.reader(csvfile, delimiter=',')
		for row in csvReader:
			siteList.append(row[2])
	return siteList

def findDNSMPI(s):
	if "do not sell" in s.lower():
		 return s

def pageSearchBS(urls):
	headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
	#urls = ["http://www.oracle.com"]
	trueURL = []
	falseURL = []
	errorURL = []
	for dbURL in urls:
		try:
			page = requests.get(dbURL, headers=headers, timeout=15)
			#print(page.content)
			soup = BeautifulSoup(page.content, 'lxml')
			result = soup.find_all(string=findDNSMPI)
			if len(result) > 0:
				#print("Result: " + str(result))
				trueURL.append(dbURL)
			else:
				falseURL.append(dbURL)
			print(str(len(trueURL) + len(falseURL) + len(errorURL)) + "/" + str(len(urls)) + " Processed")
			print(str(len(trueURL)) + " Found")
			print(str(len(errorURL)) + " Error")
		except Exception as e:
			errorURL.append(dbURL)
			print(str(len(trueURL) + len(falseURL) + len(errorURL)) + "/" + str(len(urls)) + " Processed")
			print(str(len(trueURL)) + " Found")
			print(str(len(errorURL)) + " Error")
			print("Error: " + str(type(e).__name__) +  str(e))
		print()
	print("True: " + str(trueURL), end='\n\n\n')
	print("False: " + str(falseURL), end='\n\n\n')
	print("Error: " + str(errorURL), end='\n\n\n')
	with open('bsOut.txt', 'w') as f:
		f.write("True: " + str(trueURL) + "\n\n\n" +
	  			"False: " + str(falseURL) + "\n\n\n" +
				"Error: " + str(errorURL))
	return falseURL + errorURL

def pageSearchSel(urls):
	driver = webdriver.Chrome()
	trueURL = []
	falseURL = []
	errorURL = []
	for dbURL in urls:
		#print("dbURL #" + str(i) + ": " + dbURL)
		try:
			driver.set_page_load_timeout(15)
			driver.get(dbURL)
			get_source = driver.page_source
			soup = BeautifulSoup(get_source, 'lxml')
			result = soup.find_all(string=findDNSMPI)
			if len(result) > 0:
				#print("Result: " + str(result))
				trueURL.append(dbURL)
			else:
				falseURL.append(dbURL)
			print(str(len(trueURL) + len(falseURL) + len(errorURL)) + "/" + str(len(urls)) + " Processed")
			print(str(len(trueURL)) + " Found")
			print(str(len(errorURL)) + " Error")
		except Exception as e:
			errorURL.append(dbURL)
			print(str(len(trueURL) + len(falseURL) + len(errorURL)) + "/" + str(len(urls)) + " Processed")
			print(str(len(trueURL)) + " Found")
			print(str(len(errorURL)) + " Error")
			print("Error: " + str(type(e).__name__) +  str(e))
		print()
	print("True: " + str(trueURL), end='\n\n\n')
	print("False: " + str(falseURL), end='\n\n\n')
	print("Error: " + str(errorURL), end='\n\n\n')
	with open('selOut.txt', 'w') as f:
		f.write("True: " + str(trueURL) + "\n\n\n" +
	  			"False: " + str(falseURL) + "\n\n\n" +
				"Error: " + str(errorURL))
	driver.quit()

if __name__ == "__main__":
	sl = loadDBCSV()
	rejects = pageSearchBS(sl)
	pageSearchSel(rejects)