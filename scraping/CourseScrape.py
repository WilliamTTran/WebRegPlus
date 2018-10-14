#!/usr/bin/env python
# coding: utf-8

# In[37]:


from bs4 import BeautifulSoup
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# In[48]:


link_offerings = "https://cse.ucsd.edu/undergraduate/2018-2019-tentative-undergraduate-course-offerings"
html_offerings = urllib.request.urlopen(link_offerings).read()
soup_offerings = BeautifulSoup(html_offerings, 'html.parser')

link_capes = 'http://www.cape.ucsd.edu'

link_courses = "https://ucsd.edu/catalog/courses/CSE.html"
html_courses = urllib.request.urlopen(link_courses).read()
soup_courses = BeautifulSoup(html_courses, 'html.parser')


# In[39]:


# Tentative course offering parsing

seasons = ['fall', 'winter', 'spring']
offerings = []
for entry in soup_offerings.table.find_all('tr')[1:]:
    offering = {'number': None, 'professor': None, 'season': None}
    for index, element in enumerate(entry.find_all('td')):
        offering_text = element.get_text().replace('\xa0', '').replace('\t', '').strip()
        if index is 0:
            offering['number'] = offering_text
        elif index is not 1:
            offering['season'] = seasons[index - 2]
            for prof in offering_text.split('\n'):
                if prof is not '':
                    offering['professor'] = prof
                    offerings.append(offering.copy())


# In[31]:


# CAPEs

driver = webdriver.Chrome()
for offering in offerings:
    driver.get(link_capes)
    driver.find_element_by_id('Name').send_keys(offering['professor'])
    driver.find_element_by_id('courseNumber').send_keys(offering['number'])
    driver.find_element_by_id('courseNumber').send_keys(Keys.RETURN)
    soup_capes = BeautifulSoup(driver.page_source, 'html.parser')
    
    if 'No CAPEs have been submitted that match your search criteria' in soup_capes.tbody.get_text():
        continue
    
    class_rec_percent = 0 # i5
    prof_rec_percent = 0 # i6
    study_hrs = 0# i7
    avg_gpa = 0 # i9
    cape_count = len(soup_capes.tbody.find_all('tr'))
    for entry in soup_capes.tbody.find_all('tr'):
        for index, element in enumerate(entry.find_all('td')):
            cape_text = element.get_text().replace('\xa0', '').replace('\t', '').strip()
            if index is 5:
                class_rec_percent += float(cape_text.replace(' %', ''))
            elif index is 6:
                prof_rec_percent += float(cape_text.replace(' %', ''))
            elif index is 7:
                study_hrs += float(cape_text)
            elif index is 9 and 'N/A' not in cape_text:
                avg_gpa += float(cape_text.split('(')[1][:-1])
    
    offering['class_rec_percent'] = round(class_rec_percent / cape_count, 1)
    offering['prof_rec_percent'] = round(prof_rec_percent / cape_count, 1)
    offering['study_hrs'] = round(study_hrs / cape_count, 2)
    offering['avg_gpa'] = round(avg_gpa / cape_count, 2)

driver.close()


# In[69]:


# Course description offering parsing

courses = []
names = soup_courses.find_all('p', 'course-name')
descs = [d for d in soup_courses.find_all('p', 'course-descriptions') if d.get_text().strip() is not '']

for n, d in zip(names, descs):
    n = n.get_text().strip().replace('\n', ' ').replace('\t', ' ')
    d = d.get_text().strip().replace('\n', '').replace('\t', '')
    
    number = n.split('. ')[0]
    name = n.split('. ')[1]
    name = name[:name.find(' (')].strip()
    prereqs = d.split(' Prerequisites: ')[0] if 'Prerequisites:' in d else None
    description = d.split(' Prerequisites: ')[1] if 'Prerequisites:' in d else d
    units = n[n.find('(')+1:n.find(')')]
    course = {
        'number': number, 
        'name': name,
        'prereqs': prereqs, 
        'description': description,
        'units': units
    }

    courses.append(course)

