from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

def loadURL(checkExisting):
    urls = []
    fnf = False
    if checkExisting:
        # Read URLs from output_gpt.csv if it exists
        try:
            with open('output_gpt.csv', 'r', encoding = "utf8") as file:
                reader = csv.reader(file)
                for row in reader:
                    # Skip headers row
                    if row[0] != 'url':
                        # Add URLs with 'empty' or 'error' values to list
                        if 'empty' in row[1:] or 'error' in row[1:]:
                            urls.append(row[0])
        except FileNotFoundError:
            fnf = True
            pass
    if not checkExisting or fnf:
        # Read URLs from data-broker.csv
        with open('data-broker.csv', 'r', encoding = "utf8") as file:
            reader = csv.reader(file)
            for row in reader:
                urls.append(row[2])

    return urls

def checkDNSMPI(urls):
    # Initialize WebDriver
    # Options allows us to suppress USB log messages
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(10)
    

    # Create CSV file and write headers
    with open('output_gpt2.csv', 'w', newline='', encoding = "utf8") as file:
        writer = csv.writer(file)
        writer.writerow(['url', 'font_size', 'bg_color', 'fg_color', 'element_text', 'html_tag_type', 'link_url'])
        numTrue = 0
        numFalse = 0
        numError = 0

        # Find DNSMPI links and gather information for each URL
        for url in urls:
            print("Processing " + url)
            try:
                driver.get(url)
                elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'do not sell') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'do not sell my personal information') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'dnsmpi')]")
                
                found_dnsmpi = False
                
                for element in elements:
                    # Check if element contains DNSMPI-related text
                    if 'do not sell' in element.text.lower() or 'do not sell my personal information' in element.text.lower() or 'dnsmpi' in element.text.lower():
                        found_dnsmpi = True

                    # Gather font size, background color, foreground color, element text, tag type, and link url
                    font_size = element.value_of_css_property('font-size')
                    bg_color = element.value_of_css_property('background-color')
                    fg_color = element.value_of_css_property('color')
                    element_text = element.text
                    html_tag_type = element.tag_name
                    link_url = element.get_attribute('href')

                    # Write information to CSV file
                    writer.writerow([url, font_size, bg_color, fg_color, element_text, html_tag_type, link_url])

                # Write empty row to CSV file if no DNSMPI links found
                if not found_dnsmpi:
                    writer.writerow([url, 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'])
                    numFalse += 1
                elif found_dnsmpi:
                    numTrue += 1

            except Exception as e:
                # Write error message to console and CSV file
                #print(f"Error processing URL {url}: {e}")
                writer.writerow([url, 'error', 'error', 'error', 'error', 'error', 'error'])
                numError += 1
            currNum = numFalse + numTrue + numError
            totNum = len(urls)
            print("Progress: " + str(currNum) + "/" + str(totNum))
            print("True: " + str(numTrue))
            print("False: " + str(numFalse))
            print("Error: " + str(numError))
            print()
        # Quit WebDriver
        driver.quit()

def main():
    # Load URLs from CSV files
    urls = loadURL(True)

    # Check for DNSMPI links and gather information for each URL
    checkDNSMPI(urls)

if __name__ == '__main__':
    main()
