#!venv/bin/python
"""
Get list of Openproxy servers.
Author: Paulo Coimbra
Date: 2025-07-25
"""
import os
import re
import sys

import requests
from bs4 import BeautifulSoup


def usage():
	"""
	Prints help of this tool.

	Parameters:
		None

	Returns:
		None
	"""
	print('Usage:')
	print (f'{sys.argv[0]} <OUTPUT_PROXY_LIST>')



def get_free_proxy_list(output):
	"""
	Downloads and parses Free Proxy List to <output>

	Parameters:
		output (string): Name of output file

	Returns:
		None
	"""
	global total
	try:
		html = requests.get('https://free-proxy-list.net/en/').text
	except Exception as error:
		print ('An error occurred loading url')
		exit(1)

	soup = BeautifulSoup(html,'html.parser')
	table = soup.find('tbody')
	rows = table.find_all('tr')
	with open(output,'a+') as file:
		for row in rows:
			cell = row.find_all('td')
			ip = cell[0].string
			port = cell[1].string
			file.write(f'{ip}:{port}\n')
		file.close()
	print(f'Free Proxy List: {len(rows)}')
	total+=len(rows)


def get_roosterkid(output):
	"""
	Download and parses RoosterKid list to file <output>

	Parameters:
		output (string): Name of output file

	Returns:
		None
	"""
	global total
	try:
		rows = requests.get('https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS.txt').text.split('\n')
		#🇨🇦 72.10.160.172:10919 323ms CA [GloboTech Communications]
		with open(output,'a+') as file:
			for row in rows[12:]:
				row = re.sub(r'\s+', ' ',row).split(' ')
				file.write(f'{row[1]}\n')
		file.close()
		print(f'RoosterKid List: {len(rows[12:])}')
		total = total + len(rows[12:])
	except Exception as error:
		print ('An error occurred loading url (roosterkid)')
		print(error)
		exit(1)


def get_thespeedx(output):
	"""
	Download and parses TheSpeedX list to file <output>

	Parameters:
		output (string): Name of output file

	Returns:
		None
	"""
	global total
	try:
		rows = requests.get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/refs/heads/master/http.txt').text.split('\n')
		# 10.0.0.1:80
		with open(output,'a+') as file:
			for row in rows:
				file.write(f'{row}\n')
		file.close()
		print(f'TheSpeedX List: {len(rows)}')
		total = total + len(rows)
	except Exception as error:
		print ('An error occurred loading url (TheSpeedX)')
		print(error)
		exit(1)



if __name__ == '__main__':
	if len(sys.argv) != 2:
		usage()
		exit(1)
	output=sys.argv[1]
	if os.path.exists(output):
		if input(f"The file '{output}' exists. Replace (y/n)? ") != 'y':
			exit(1)
		else:
			os.remove(output)
	total=0
	get_free_proxy_list(output)
	get_roosterkid(output)
	#get_thespeedx(output)
	print(f'Total of Proxies obtained: {total}')
