## Sample program to scrape a page in a given url
## The page has a table with list of MPs. 
## Program creates a representing data structure of the data in the table.
## Creates and prints lsit of dictionary objects. Each object has information of a candidate from the table.
## The output can be dumped into a file in json format directly

import requests
from bs4 import BeautifulSoup
from urlparse import urljoin  ## This is for python2. For python3 use 'from urllib.parse import urljoin'
import json

## Url of the page you want to scrape
base_url = 'http://164.100.47.194/Loksabha/Members/StateDetail.aspx?state_code=Andhra+Pradesh'

## Make a http request to the url and get the response.
## requests package helps make http get request here to the url.
page = requests.get(base_url)

## Parse the contents of the http response using a HTML parser. 
## We are using BeautifulSoup library to parse the web page text.
## This creates a HTML object representing the entire page.
parsed_page = BeautifulSoup(page.text, 'lxml')


## Find the table where members information is present. 
## The table has comes under the tag <table> and has class attribute with value member_list_table.
## This gives a HTML tag from which we need to extract rows to get table rows.
member_list_table = parsed_page.find('table', attrs = {'class' : 'member_list_table'})

## The table has children tags <tr> meaning tablerow.
## Get all the rows except 0th row.
## Python starts counting from 0. So we need 1-> end, which is represented as [1:].
## 0th row is eliminated because it is the header row which we are not interested in.
## The result is a ResultSet. Each element is a tag.
member_row_list = member_list_table.findAll('tr')[1 : ]

## Array to store list of row objects.
## Each row object will be a dictionary(python data structure) containing the below elements
##    - Sl No, Constituency name, MP Name, Link to individual details page, Party
candidate_row_arr = []


## For each row, prepare row object
for member_row_element in member_row_list:

    ## Get all cells in the row, i.e, column elements for the row
	cells = member_row_element.findAll('td')


	## First cell has Sl. No.
	sl_no_cell_text = cells[0].text.encode('utf-8')
	## The text is in a bad format. It has unnecessary leading and trailing spaces and \n\r which we will remove by calling strip() method
	## This will be done for all the cells.
	sl_no_cell_text = sl_no_cell_text.strip()


	## Second cell has Constituency name. Formatting same as sl_no_cell
	constituency_cell_text = cells[1].text.encode('utf-8')
	constituency_cell_text = constituency_cell_text.strip()


	## Third cell has Candidate name.
	candidate_cell_text = cells[2].text.encode('utf-8')
	candidate_cell_text = candidate_cell_text.strip()

	## We also need link to the page of the candidate details
	## Link comes as <a href="link url"> Somename </a>
	## Extract link url from the cell.
	## The value has partial url : ../Member/somepath. Convert it to fully qualified url(http://hostname/Member/somepath) using urljoin.
	candidate_page_link = cells[2].find('a')['href']
	fully_qualified_url = urljoin(base_url, candidate_page_link)


	## Fourth cell has Party.
	## Formatting same as sl_no_cell
	party_cell_text = cells[3].text.encode('utf-8')
	party_cell_text = party_cell_text.strip()

	candidate_row_object = {
		'slno' : sl_no_cell_text,
		'constituency' : constituency_cell_text,
		'candidate' : candidate_cell_text,
		'pagelink' : fully_qualified_url,
		'party' : party_cell_text
	}

	candidate_row_arr.append(candidate_row_object)

## Out of for loop

## Print objects from the array line by line.
print ("\r\n".join(str(element) for element in candidate_row_arr))

## Write the data into a file in json format, which is already the case.
## Uncomment the below 2 lines if you want output in a json file.

# with open('mps_direct_table_info.json', 'w') as outfile:
#     json.dump(candidate_row_arr, outfile)



