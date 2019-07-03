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
import argparse
import urllib2
import re
from datetime import datetime

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
	urls = []
	for each in res:
		if each in urls:
			continue
		urls.append(each)
	for each in urls:
		tmp = each[1].decode("latin-1")
		datedata = re.match(r'.+meeting-schedule-(([a-z]+)([0-9]+-[0-9]+))/', each)
		if datedata is not None:
			datestr = '{} {}'.format(datedata.group(2).capitalize()[:3], datedata.group(3))
		else:
			datedata = re.match(r'.+meeting-schedule-(([a-z]+)([0-9]+)-([a-z]+)([0-9]+))/', each)
			datestr = '{} {}-{} {}'.format(
				datedata.group(2).capitalize()[:3], datedata.group(3),
				datedata.group(4).capitalize()[:3], datedata.group(5))
		studies = grabweekstudies(URL_HEADER + each)
		print("- {}: {!r}".format(datestr, studies))


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
		studies.append(int(res.group(1)))
	return studies


if __name__ == "__main__":
	today = datetime.now()
	month = today.month + 1
	year = today.year
	if month == 13:
		month = 1
		year += 1
	parser = argparse.ArgumentParser('CLM Study Number')
	parser.add_argument('-m', '--month', choices=[
		'{}'.format(each) for each in range(1, 13)], default=month)
	parser.add_argument('-y', '--year', choices=[
		'{}'.format(each) for each in [year, year + 1]], default=year)
	args = parser.parse_args()
	month = int(args.month)
	year = int(args.year)
	print('{} {}'.format(months[month - 1].capitalize(), year))
	main(month, year)
