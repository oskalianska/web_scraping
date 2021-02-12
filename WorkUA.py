# Analytics based on Skills - Work.UA

# Install and import libraries

!pip install bs4

import matplotlib as plt
import pandas as pd
import numpy as np
import bs4
import re
from urllib.request import urlopen as uReq
#from bs4 import BeautifulSoup as soup
from bs4 import BeautifulSoup
#import urllib

# Define job title and geographic location

#Search Work.ua web-site for "Data Scientist" job vacancies.

#jobtitle = str(input("Please enter the job title: "))
jobtitle = 'data scientist'
#location = str(input("Please enter the job location:"))
#location = 'Toronto'
query1=jobtitle.replace(' ','+')
#query2=location.replace(' ','+')
url_base = 'https://www.work.ua'
urlorig = url_base + '/jobs-'+query1+'/'
urlorig

url = uReq(urlorig)
page_html = url.read()
url.close()

page_soup = BeautifulSoup(page_html,'html.parser')
#print(page_soup)

links = []

for link in page_soup.find_all('a'):
    if link.get('title'):
        if link.get('title').startswith("Сторінка"):
            links.append(link.get('href'))
            print(link.get('href'),link.get('title'))

links[-1]

try:
    num_pages = re.search('page=(.*)', links[-1])
    N_pages = int(num_pages.group(1))
except:
    N_pages = 1
url_pages = links[-1][:-len(str(N_pages))]
url_pages

# Create list of job vacancies

#Extract knowledge of technologies (Python, Excel, R, Matlab, Hadoop, Spark, etc.)

# Empty list for job_title, company_name, location, job_description, job skills
titles = []
company_names = []
location_names = []
job_descriptions = []
job_descriptHTML = []
job_ids = []
skills = {}
skills['Python'] = []
skills['R '] = []
skills['Matlab'] = []
skills['Excel'] = []
skills['SAS'] = []
skills['SQL'] = []
skills['SPSS'] = []
skills['Hadoop'] = []
skills['Spark'] = []

#for i in range(1,3):
for i in range(1,N_pages+1):
    
    # html parsing Work.ua job portal page 
    my_url = url_base + url_pages + str(i)
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = BeautifulSoup(page_html,'html.parser')
    
    # extract job_title
    jobs = page_soup.findAll('div',{'class': 'job-link'})
    print(my_url,' ',len(jobs), 'jobs')
    for job in jobs:
        try:
            title = job.find(class_='add-bottom-sm').get_text()
            title = title.strip(' \t\n\r')
            titles.append(title)
        except:
            title = "N/A"
            titles.append(title)

    links = page_soup.findAll("h2", class_ = "add-bottom-sm")   

    for link in links:

        #print(url_base + link.a["href"])
        Jb = uReq(url_base + link.a["href"])
        try:
            res_id = re.search('\/jobs\/(.*)\/', link.a["href"])
            job_ids.append(res_id.group(1))
        except:
            job_ids.append("")

        Jb_html = Jb.read()
        Jb.close()
        Jb_soup = BeautifulSoup(Jb_html, "html.parser")
        
        html = u""
        for tag in Jb_soup.find("h1").next_siblings:
            if tag.name == "div":
                break
            else:
                html += str(tag)
                #html += unicode(tag)

        cleantext = BeautifulSoup(str(html), 'lxml').text
        
        job_descriptHTML.append(html)

        try:
            job_descriptions.append(cleantext)  
        except:
            job_descriptions.append("NA")  
            
        if("excel" in cleantext.lower()):
            skills['Excel'].append('1')
        else:
            skills['Excel'].append('0')
            
        if("python" in cleantext.lower()):
            skills['Python'].append('1')
        else:
            skills['Python'].append('0')
            
        if("R " in cleantext):
            skills['R '].append('1')
        else:
            skills['R '].append('0')
        
        if("matlab" in cleantext.lower()):
            skills['Matlab'].append('1')
        else:
            skills['Matlab'].append('0')
        
        if("sas" in cleantext.lower()):
            skills['SAS'].append('1')
        else:
            skills['SAS'].append('0')
            
        if("sql" in cleantext.lower()):
            skills['SQL'].append('1')
        else:
            skills['SQL'].append('0')
            
        if("spss" in cleantext.lower()):
            skills['SPSS'].append('1')
        else:
            skills['SPSS'].append('0')
            
        if("hadoop" in cleantext.lower()):
            skills['Hadoop'].append('1')
        else:
            skills['Hadoop'].append('0')
        
        if("spark" in cleantext.lower()):
            skills['Spark'].append('1')
        else:
            skills['Spark'].append('0')

# Create dataframe with job vacancies and save it to csv file

d = {'Job_ID':job_ids,'Job_Title':titles,'Job_Description':job_descriptions,'Job_DescripHTML':job_descriptHTML}
df1 = pd.DataFrame(d)
df2 = pd.DataFrame(skills)
frames = [df1, df2]
results = pd.concat(frames, axis = 1)
results.head()

results.tail()

results.to_csv('WorkUA_job_vacancies.csv')
