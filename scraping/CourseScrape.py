import re

from bs4 import BeautifulSoup
import urllib
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import config

# Disable js
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})

# Links
link_offerings = 'https://cse.ucsd.edu/undergraduate/2018-2019-tentative-undergraduate-course-offerings'
html_offerings = urllib.request.urlopen(link_offerings).read()
soup_offerings = BeautifulSoup(html_offerings, 'html.parser')

link_capes = 'http://www.cape.ucsd.edu'

link_courses = 'https://ucsd.edu/catalog/courses/CSE.html'
html_courses = urllib.request.urlopen(link_courses).read()
soup_courses = BeautifulSoup(html_courses, 'html.parser')

link_rmp = 'http://www.ratemyprofessors.com/search.jsp?query='

link_hours = "http://courses.ucsd.edu/courseList.aspx?name=CSE"
html_hours = urllib.request.urlopen(link_hours).read()
soup_hours = BeautifulSoup(html_hours, 'html.parser')

API = 'http://localhost:3000/api/'

requests.delete(API + 'offerings')
requests.delete(API + 'courses')

# Course description offering parsing

courses = []
names = soup_courses.find_all('p', 'course-name')
descs = [d for d in soup_courses.find_all('p', 'course-descriptions') if d.get_text().strip() is not '']

for n, d in zip(names, descs):
    n = n.get_text().replace('\n', ' ').replace('\r', '').replace('\t', '')
    d = d.get_text().replace('\n', ' ').replace('\r', '').replace('\t', '')

    number = n.split('. ')[0]
    name = n.split('. ')[1]
    name = name[:name.find(' (')].strip()
    prereqs = d.split(' Prerequisites: ')[1] if 'Prerequisites:' in d else None
    description = d.split(' Prerequisites: ')[0] if 'Prerequisites:' in d else d
    units = n[n.find('(') + 1:n.find(')')]
    course = {
        'number': number,
        'name': name,
        'prereqs': prereqs,
        'description': description,
        'units': units
    }

    courses.append(course)

requests.post(API + 'courses', json=courses)

# Construct a names dictionary
names_to_full_names = dict()
# Array of {prof_name, podcast_url, lecture_days, lecture_start, lecture_end, lecture_room, final_day, final_start, final_end},
course_number_to_info_arr = dict()

# Log on SSO
driver = webdriver.Chrome()
driver.get('https://act.ucsd.edu/webreg2/start')
driver.find_element_by_id('ssousername').send_keys(config.user)
driver.find_element_by_id('ssopassword').send_keys(config.pw)
driver.find_element_by_name('_eventId_proceed').click()

for offering_tr in soup_hours.find('table', id='courses_DataList').find_all('tr'):
    offering_li = offering_tr.td.li.find_all('a')
    course_number = ' '.join(re.sub('\s+', ' ', offering_li[0].get_text()).split(' ')[:2])
    print(course_number)
    url = 'https://courses.ucsd.edu/' + offering_li[0]['href']
    short_name = offering_li[1].get_text()
    full_name = offering_li[1]['href']
    full_name = ' '.join(full_name[full_name.index('=') + 1:].split(' ')[:2])
    names_to_full_names[short_name] = full_name

    soup_info = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

    podcast_elem = [x for x in soup_info.find('ul', class_='single-resources').find_all('li') if x.a.span.get_text() == 'Podcast']
    if len(podcast_elem) is not 0:
        podcast_intermediate_url = podcast_elem[0].a['href']
        # Get podcast info
        driver.get(podcast_intermediate_url)
        try:
            podcast_video = driver.find_element_by_tag_name('video')
            podcast_url = podcast_video.get_property('src')
        except:
            podcast_url = None
    else:
        podcast_url = None
    print(podcast_url)

    try:
        print(soup_info.find_all('tr', class_='lecture')[0].find_all('td'))

        lecture_tds = soup_info.find_all('tr', class_='lecture')[0].find_all('td')
        lecture_days = re.sub('\s+', ' ', lecture_tds[2].span.get_text().strip())
        lecture_start = ' '.join(lecture_tds[3].get_text().replace('\n', '').split(' ')[:2])
        lecture_end = ' '.join(lecture_tds[3].get_text().replace('\n', '').split(' ')[3:5])
        lecture_room = re.sub('\s+', ' ', lecture_tds[4].span.get_text().strip())
    except:
        lecture_start = None
        lecture_days = None
        lecture_end = None
        lecture_room = None

    try:
        final_tds = soup_info.find_all('tr', class_='final')[0].find_all('td')
        final_day = final_tds[1].get_text().replace('\n', '')
        final_start = ' '.join(final_tds[3].get_text().replace('\n', '').split(' ')[:2])
        final_end = ' '.join(final_tds[3].span.get_text().replace('\n', '').split(' ')[3:5])
    except:
        final_day = None
        final_start = None
        final_end = None

    if course_number not in course_number_to_info_arr.keys():
        course_number_to_info_arr[course_number] = []
    course_number_to_info_arr[course_number].append({
        'prof_name': short_name,
        'podcast_url': podcast_url,
        'lecture_days': lecture_days,
        'lecture_start': lecture_start,
        'lecture_end': lecture_end,
        'lecture_room': lecture_room,
        'final_day': final_day,
        'final_start': final_start,
        'final_end': final_end
    })
    print({
        'prof_name': short_name,
        'podcast_url': podcast_url,
        'lecture_days': lecture_days,
        'lecture_start': lecture_start,
        'lecture_end': lecture_end,
        'lecture_room': lecture_room,
        'final_day': final_day,
        'final_start': final_start,
        'final_end': final_end
    })
driver.close()
print(course_number_to_info_arr)

# Tentative course offering parsing

seasons = ['fall', 'winter', 'spring']
offerings = []
for entry in soup_offerings.table.find_all('tr')[1:]:
    offering = {'course_number': None, 'prof_name': None, 'season': None}
    for index, element in enumerate(entry.find_all('td')):
        offering_text = element.get_text().replace('\xa0', '').replace('\t', '').strip()
        if index is 0:
            offering['course_number'] = offering_text
        elif index is not 1:
            offering['season'] = seasons[index - 2]
            for prof in offering_text.split('\n'):
                if prof is not '':
                    offering['prof_name'] = prof
                    offerings.append(offering.copy())

# CAPEs
prof_to_rmp = dict()

driver = webdriver.Chrome()
driver_rmp = webdriver.Chrome(chrome_options=chrome_options)
post_offerings = []
for offering in offerings:
    if 'STAFF' in offering['prof_name']:
        continue

    # RMP
    if offering['prof_name'] not in prof_to_rmp.keys():
        if offering['prof_name'] in names_to_full_names.keys():
            name = names_to_full_names[offering['prof_name']]
        else:
            name = offering['prof_name']
        driver_rmp.get(link_rmp + ('University of California San Diego ' + name).replace(' ', '+'))
        # Click on search result
        try:
            driver_rmp.find_element_by_class_name('PROFESSOR').find_element_by_tag_name('a').click()
            prof_to_rmp[offering['prof_name']] = driver_rmp.find_element_by_class_name('breakdown-container').find_element_by_class_name('grade').text
            print(prof_to_rmp)
            print(prof_to_rmp[offering['prof_name']])
        except Exception as e:
            print('failed to initially get rmp')
            driver_rmp.get(link_rmp + ('University of California San Diego ' + offering['prof_name']).replace(' ', '+'))
            # Click on search result
            try:
                driver_rmp.find_element_by_class_name('PROFESSOR').find_element_by_tag_name('a').click()
                prof_to_rmp[offering['prof_name']] = driver_rmp.find_element_by_class_name(
                    'breakdown-container').find_element_by_class_name('grade').text
                print(prof_to_rmp)
                print(prof_to_rmp[offering['prof_name']])
            except Exception as e:
                print('Failed a second time')
                prof_to_rmp[offering['prof_name']] = None

    offering['rmp_score'] = prof_to_rmp[offering['prof_name']]

    driver.get(link_capes)
    driver.find_element_by_id('Name').send_keys(offering['prof_name'])
    driver.find_element_by_id('courseNumber').send_keys(offering['course_number'])
    driver.find_element_by_id('courseNumber').send_keys(Keys.RETURN)
    soup_capes = BeautifulSoup(driver.page_source, 'html.parser')

    if 'No CAPEs have been submitted that match your search criteria' not in soup_capes.tbody.get_text():
        class_rec_percent = 0  # i5
        prof_rec_percent = 0  # i6
        study_hr = 0  # i7
        avg_gpa = 0  # i9
        cape_count = len(soup_capes.tbody.find_all('tr'))
        for entry in soup_capes.tbody.find_all('tr'):
            for index, element in enumerate(entry.find_all('td')):
                cape_text = element.get_text().replace('\xa0', '').replace('\t', '').strip()
                if index is 5:
                    class_rec_percent += float(cape_text.replace(' %', ''))
                elif index is 6:
                    prof_rec_percent += float(cape_text.replace(' %', ''))
                elif index is 7:
                    study_hr += float(cape_text)
                elif index is 9 and 'N/A' not in cape_text:
                    avg_gpa += float(cape_text.split('(')[1][:-1])

        # offering['prof_name'] = soup_capes.tbody.td.get_text().replace('\xa0', '').replace('\t', '').strip()
        offering['class_rec_percent'] = round(class_rec_percent / cape_count, 1)
        offering['prof_rec_percent'] = round(prof_rec_percent / cape_count, 1)
        offering['study_hr'] = round(study_hr / cape_count, 2)
        offering['avg_gpa'] = round(avg_gpa / cape_count, 2)

    try:
        info_arr = course_number_to_info_arr[offering['course_number']]
        for elem in [x for x in info_arr if x['prof_name'] == offering['prof_name']]:
            offering_new = offering.copy()
            offering_new['podcast_url'] = elem['podcast_url']
            offering_new['lecture_days'] = elem['lecture_days']
            offering_new['lecture_start'] = elem['lecture_start']
            offering_new['lecture_end'] = elem['lecture_end']
            offering_new['lecture_room'] = elem['lecture_room']
            offering_new['final_day'] = elem['final_day']
            offering_new['final_start'] = elem['final_start']
            offering_new['final_end'] = elem['final_end']
            print(offering_new)
            post_offerings.append(offering_new)
    except Exception as e:
        print(e)
        post_offerings.append(offering)

driver.close()
driver_rmp.close()
requests.post(API + 'offerings', json=post_offerings)
