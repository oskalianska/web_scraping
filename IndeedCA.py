# Analytics based on Skills from Indeed.ca

# Install and import libraries

#!pip install bs4

import matplotlib as plt
import pandas as pd
import numpy as np
import bs4
import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Define job title and geographic location

#Search Indeed.ca web-site for "Data Scientist" job vacancies at the specified geographic location.

#jobtitle = str(input("Please enter the job title: "))
jobtitle = 'data scientist'
#location = str(input("Please enter the job location:"))
location = 'Toronto'
query1=jobtitle.replace(' ','+')
query2=location.replace(' ','+')
urlorig='https://www.indeed.ca/jobs?q='+query1+'&l='+query2+'&start='
urlorig

# Create list of job vacancies

#Extract knowledge of technologies (Python, Excel, R, Matlab, Hadoop, Spark, etc.)

# Empty list for job_title, company_name, location, job_description, job skills
titles = []
company_names = []
location_names = []
job_descriptions = []
job_ids = []

# Loop over 1000 vacancies (20 at each page)
for i in range(0,50,20):
    
    # html parsing Indeed job portal page 
    my_url = urlorig+str(i)
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html,'html.parser')
    
    # extract job_title
    jobs = page_soup.findAll("div", class_="row" )
    for job in jobs:
        try:
            titles.append(job.a["title"])
        except:
            titles.append("NA")
        
    # extract company_name
    companies = page_soup.findAll("span", class_="company" )
    for company in companies:
        try:
            company_names.append(company.text.strip())
        except:
            company_names.append("NA")
    
    # extract location       
    locations = page_soup.findAll( class_="location")
    for location in locations:
        try:
            location_names.append(location.text)
        except:
            location_names.append("NA")
    
    # extract job_description 
    links = page_soup.findAll("div", class_ = "row")   
    for link in links:
        
        Jb = uReq("https://www.indeed.ca" + link.a["href"])
        try:
            res_id = re.search('clk\?jk=(.*)&fccid', link.a["href"])
            job_ids.append(res_id.group(1))
        except:
            job_ids.append("")
        Jb_html = Jb.read()
        Jb.close()
        Jb_soup = soup(Jb_html, "html.parser")
        
        job_description = Jb_soup.findAll("div", class_= "jobsearch-JobComponent-description")
        cleantext = soup(str(job_description), 'lxml').text
        try:
            job_descriptions.append(cleantext)  
        except:
            job_descriptions.append("NA")

# Create dataframe with job vacancies and save it to csv file"""

d = {'Job_ID':job_ids,'Job_Title':titles,'Company_Name':company_names,'Location':location_names,'Job_Description':job_descriptions}
results = pd.DataFrame(d)
results.head()

results.tail()

results.to_csv('Indeed_job_vacancies.csv')
