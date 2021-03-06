#Analytics based on Skills - PracujPL

# Installation of selenium API
#! pip install selenium

# importing packages from selenium
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from selenium.webdriver import ActionChains

#!pip install webdriver-manager

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())

#Opening a specific website on the browser
#browser.get("https://www.indeed.ca/")
#browser.get("http://diasporiana.org.ua/")
browser.get("https://www.pracuj.pl/praca/data%20scientist")
#browser.get("https://www.pracuj.pl/praca/big-data-analyst-gdynia,oferta,6833333")

browser.page_source

timeout=2
lisT = [] 
Npages = int(browser.find_elements_by_class_name('pagination_trigger')[-2].text)
print('Scrapping %d pages of jobs\n=========================\n' % Npages)
for x in range(1,Npages+1): # loop through pages to gather the required information
    Job_search = browser.find_elements_by_class_name('results__list-container-item')
    for y in range(0,len(Job_search)):
        title=''
        company=''
        descript=''
        job_description=''
        title2=''
        url=''
        location=''
        employmentType=''
        datePosted=''
        dateValid=''
        attribs=''
        idx=''
        id_str=''
        author=''
        added=''
        publisher=''
        Npages=''
        description=''
        book_page=''
        #url_pdf=''
        url_file=''        
        #url_djvu=''
        url_img=''
        source=''
        page=x
        item=y+1
        
        # Getting the link to details of each book posting
        time.sleep(1)
        abc = Job_search[y].find_element_by_tag_name("a").get_attribute("href")
        try:
            int(abc[-7:])
        except:
            abc = Job_search[y].find_elements_by_tag_name("a")[2].get_attribute("href")
        url = abc

        try: # getting title1
            title = Job_search[y].find_elements_by_class_name('offer-details__title-link')[0].text
        except:
            print("Title 1 not available on page"+str(x)+" position "+str(y+1))
            title = "Not Available"

        try: # getting title1
            company = Job_search[y].find_elements_by_class_name('offer-company__wrapper')[0].text
        except:
            company = "Not Available"           

        try: # getting description
            descript = Job_search[y].text
        except:
            descript = ""
            
        try: # getting attributes
            attribs = Job_search[y].get_attribute("class")
        except:
            print("Attributes not available on page"+str(x)+" position "+str(y+1))
            attribs = ""
            
        id_str = url[-7:]
        try:
            idx = int(url[-7:])
        except:
            idx = float('NaN')
        
        print('Page %d - processing item %d with id=%s' % (page,item,id_str))

        # opening the link in new page
        actions = ActionChains(browser)
        find = browser.find_element_by_link_text("data scientist")
        #find = browser.find_element_by_class_name("offer__click-area")
        actions.key_down(Keys.CONTROL).click(find).key_up(Keys.CONTROL).perform()
        time.sleep(2)
        browser.switch_to.window(browser.window_handles[-1])
        ##time.sleep(1)
        browser.get(abc)
        ##time.sleep(3)

        try:# getting tittle
            job_description = browser.find_elements_by_id("offer")[0].text
        except:
            job_description = ""       
        
        try:# getting tittle
            title2 = browser.find_element_by_class_name("main__right_offer_head_title-mobile").text
        except:
            print("Title 2 not available on page"+str(x)+" position "+str(y+1))
            title2 = "Not Available"
            
        print(title)
        print(url)        
            
        Section_search = browser.find_elements_by_class_name("o-main__right_offer_cnt_details_item_text")
        location=""
        employmentType=""
        datePosted=""
        dateValid=""
        for k in range(0,len(Section_search)):
            #print(Section_search[k].text)
            if k==0:
                location=Section_search[k].text
            if k==1:
                employmentType=Section_search[k].text
            if k==2:
                datePosted=Section_search[k].text
            if k==3:
                dateValid=Section_search[k].text
                
        # Creating a dictionary for all the values
        current_row={"ID":idx, "Job_Title":title, "Job_Title2":title2, "Company_Name":company, "Location":location,
                     "Job_Description":job_description, "URL":url, "IDStr":id_str,"Page":page,"Item":item,
                     "Description":descript, "Employment_Type":employmentType, "Date_Posted":datePosted, "Date_Valid":dateValid}

        #current_row={"ID":idx, "Job_Title":title, "Job_Title2":title2, "Attributes":attribs,
        #            "URL":url, "Job_Description":job_description, "IDStr":id_str,"Page":page,"Item":item,
        #             "Added":added, "Author":author, "Publisher":publisher, "Npages":Npages, "Description":description,
        #             "Source":source, "URLfile":url_file, "URLimg":url_img, "BookPage":book_page}
            
        # appending it to a List
        lisT.append(current_row)
                    
        # coming out to the main page
        browser.execute_script("window.history.go(-1)")
        browser.switch_to.window(browser.window_handles[-1])
        browser.close()
        browser.switch_to_window(browser.window_handles[0])
        
    #Next_button_series = browser.find_element_by_class_name('nextpostslink')
    #Next_button_series = browser.find_element_by_class_name('pagination_element pagination_element--next')
    #Next_button_series = browser.find_elements_by_class_name('pagination_trigger')[-1].get_attribute("href")
    Next_button_series = browser.find_elements_by_class_name('pagination_trigger')[-1]
    #Next_button_series[len(Next_button_series) -1].click()
    time.sleep(2)
    Next_button_series.click()
    time.sleep(3)

# Converting to a Dataframe and publishing the result
df= pd.DataFrame(lisT)
df = df[["ID", "Job_Title", "Job_Title2", "Company_Name","Location",
         "Job_Description", "URL", "IDStr","Page","Item",
         "Description", "Employment_Type", "Date_Posted", "Date_Valid"]]

df.head()

df.tail()

df.to_csv('Pracuj_pl_results_May11.csv')

