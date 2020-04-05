## From the json output of sample_scraper.py, gets the url for each member and gets Date of Birth in addition to the already existing information.
## For each MP, fetch some attribute, say data of birth, from Member page.
## Creates a csv file with each entry of candidate info like slno, MP name, Constituency, DOB
## CSV can later be imported to sheets

import requests
from bs4 import BeautifulSoup
import json
import csv


#------------------------------------python functions start------------------------------------
## All functions needed for the program go in this block.


## For a hyperlink element in html, returns the link value.
## If link_element is none, returns empty string.
## Eg: link_element = <a href="abc.com">, returns "abc.com" string
def get_link(link_element):
	print link_element
	if link_element is not None:
		return link_element.get('href')
	return ''

#------------------------------------python functions end------------------------------------


with open('mps_direct_table_info.json') as file:
  member_data_arr = json.load(file)

## Dictionary elements will be of the following format as we inserted them in sample_scraper.py
# 'slno' : sl_no_cell_text,
# 'constituency' : constituency_cell_text,
# 'candidate' : candidate_cell_text,
# 'pagelink' : fully_qualified_url,
# 'party' : party_cell_text

## In addition to the already existing 5 columns, we will be adding more columns like facebook link, twitter link.


moidified_member_data_arr = []

## We need to find DOB from the url link present in the member_data object by parsing the page.
for member_data in member_data_arr:

	member_page = requests.get(member_data['pagelink'])
	parsed_member_page = BeautifulSoup(member_page.text, 'lxml')

	fb_link_element = parsed_member_page.find('a', attrs={'id':'ContentPlaceHolder1_fblnk'})
	twitter_link_element = parsed_member_page.find('a', attrs={'id':'ContentPlaceHolder1_twtrlnk'})

	## Add fb link and twitter account links in the dictionary.
	member_data['facebook'] = get_link(fb_link_element)
	member_data['twitter'] = get_link(twitter_link_element)

	moidified_member_data_arr.append(member_data)


## Modified member object has 2 extra fields, fb_link and twitter_link
## Write modifed members data into a csv file.
with open('member_nested_data.csv', mode='w') as csv_file:
    fieldnames = ['slno', 'constituency', 'candidate', 'party', 'pagelink', 'facebook', 'twitter']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for modified_member_data in moidified_member_data_arr:
    	writer.writerow(modified_member_data)







