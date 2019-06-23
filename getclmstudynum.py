#!/bin/env python
# ---------------------------------------------------------------------
# getclmsched.py
# by John Cruz 2017-06-12
#
# Retrieves the Tagalog CLM schedule for a particular month and print
# it out in the screen.
#
# ---------------------------------------------------------------------
from __future__ import unicode_literals, print_function
import urllib2
import re

# +++ constants
URL_HEADER = "https://www.jw.org"
# months = ["enero", "pebrero", "marso", "abril", "mayo", "hunyo", "hulyo", "agosto", "setyembre",
# 	"oktubre", "nobyembre", "disyembre"]
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
	"octuber", "november", "descember"]


def main(month, year):
	"""This is the main function

	Args:
	- `month` (`int`): self-explained
	- `year` (`int`): self-explained

	Returns:
	- `None`
	"""
	try:
		pageurl = 'https://www.jw.org/en/publications/jw-meeting-workbook/{}-{}-mwb/'.format(
			months[month - 1], year)
		site = urllib2.urlopen(pageurl)
		data = site.read()
	except urllib2.URLError as err:
		print("Failed to retrieve page: {}".format(pageurl))
		print("{}: {}".format(err.__class__.__name__, err))
		exit(0)

	# NOTE: Look for the following pattern
	# https://www.jw.org/en/publications/jw-meeting-workbook/june-2019-mwb/meeting-schedule-june3-9/
	res = re.findall(r'/en/publications/jw-meeting-workbook/.+?/meeting-schedule-.+?/',
		data.decode('utf-8'))
	for each in set(res):
		tmp = each[1].decode("latin-1")
		datedata = re.match(r'.+meeting-schedule-(.+?)/', each)
		studies = grabweekstudies(URL_HEADER + each)
		print("Studies for {}: {!r}".format(datedata.group(1), studies))


def grabweekstudies(url):
	"""Grab the per-week program data.

	Args:
	- `url` (`str`): URL of the per week's page

	Returns:
	- `list`: all the program's data including the header of each
	program's section
	"""
	# print('URL = {!r}'.format(url))
	site = urllib2.urlopen(url)

	# get the HTML-stripped data
	tmp = site.read().decode('utf-8')
	study = re.findall(r"<em>th.*?</em>study.*?\d+</a>", tmp)

	# get the data enclosed in the first and last song
	studies = []
	for each in study:
		res = re.match('.+study.+?(\d+)</a>', each)
		studies.append('{}'.format(res.group(1)))
	return studies


if __name__ == "__main__":
	month = int(raw_input("Month (1-12 where 1=Jan & 12=Dec): "))
	year = int(raw_input("Year (ex: 2017): "))
	main(month, year)
