from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import pdb
import re
from datetime import datetime
from itertools import zip_longest
import csv


# Create webdriver object 
driver = webdriver.Chrome() 

url = 'https://packaging.python.org/en/latest/guides/section-install/'
# wait = WebDriverWait(driver, 10)
##Hit main url
driver.get(url)
sleep(2)


install_div = driver.find_element(By.CSS_SELECTOR, "#installation > div")
install_div_list = install_div.find_elements(By.TAG_NAME, "li")

##Get List of installation urls
##https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
install_div_urls_raw = [each.find_element(By.TAG_NAME, "a").get_attribute('href') for each in install_div_list]

print('scrape')
for each_url in install_div_urls_raw:
    ##Hit each installation url
    driver.get(each_url)
    sleep(2)
   
    url_name = each_url.split('/')[-2].strip()
    headings = driver.find_elements(By.TAG_NAME, "h2")
    headings_texts = [heading.text.strip() for heading in headings]

    sub_headings = driver.find_elements(By.TAG_NAME, "h3")
    sub_headings_texts = [sub_heading.text.strip() for sub_heading in sub_headings]

    codes = codes = driver.find_elements(By.TAG_NAME, "pre")
    codes_texts = [code.text.strip() for code in codes if code.text.strip()]    
    
    ##Zip lists based on longest list
    result = list(zip_longest(headings_texts, sub_headings_texts, codes_texts, fillvalue=' '))    
   
    ###Writing the extracted Data to Excel file
    if result:    
        with open(f'{url_name}.csv','w',encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['Header', 'Sub_Header', 'Code'])
            writer.writerows(result)


driver.quit()
print('-----------process_completed------------------')
