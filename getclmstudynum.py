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
	"october", "november", "december"]


def main(month, year):
	"""This is the main function

	Args:
	- `month` (`int`): self-explained
	- `year` (`int`): self-explained

	Returns:
	- `None`
	"""
	try:
		if year < 2021:
			pageurl = 'https://www.jw.org/en/library/jw-meeting-workbook/{}-{}-mwb/'.format(
				months[month - 1], year)
		else:
			pageurl = 'https://www.jw.org/en/library/jw-meeting-workbook/{}-{}-{}-mwb/'.format(
				months[month -1], months[month], year)
		# print('Opening workbook for {}/{}...'.format(month, year))
		site = urllib2.urlopen(pageurl)
		data = site.read()
	except urllib2.URLError as err:
		print("Failed to retrieve page: {}".format(pageurl))
		print("{}: {}".format(err.__class__.__name__, err))
		exit(0)

	# NOTE: Look for the following pattern
	# https://www.jw.org/en/publications/jw-meeting-workbook/june-2019-mwb/meeting-schedule-june3-9/
	# https://www.jw.org/en/library/jw-meeting-workbook/december-2019-mwb/meeting-schedule-december2-8/
	# https://www.jw.org/en/library/jw-meeting-workbook/january-2020-mwb/Our-Christian-Life-and-Ministry-Schedule-for-January-6-12-2020/
	# https://www.jw.org/en/library/jw-meeting-workbook/april-2020-mwb/Life-and-Ministry-Meeting-Schedule-for-April-20-26-2020/
	# https://www.jw.org/en/library/jw-meeting-workbook/january-february-2021-mwb/Life-and-Ministry-Meeting-Schedule-for-January-4-10-2021/
	res = None
	res = re.findall(
		r'/en/library/jw-meeting-workbook/.+?/(meeting-schedule|[^/]*Life-and-Ministry[^/]*-Schedule-for)-(.+?)/',
		data.decode('utf-8'))
	urls = []
	for each in res:
		if each in urls:
			continue
		urls.append(each)
	# print('urls = {!r}'.format(urls))
	for prefix, each in urls:
		# tmp = each[1].decode()
		datedata = re.match(r'([A-Za-z]+)-?([0-9]+-[0-9]+)(-[0-9]{4})?', each)
		if datedata is not None:
			datestr = '{} {}'.format(datedata.group(1).capitalize()[:3], datedata.group(2))
		else:
			datedata = re.match(r'([A-Za-z]+)-?([0-9]+)-([A-Za-z]+)-?([0-9]+)(-[0-9]{4})?', each)
			datestr = '{} {}-{} {}'.format(
				datedata.group(1).capitalize()[:3], datedata.group(2),
				datedata.group(3).capitalize()[:3], datedata.group(4))
		# print('Grabbing week studies...')
		studies, parts = grabweekstudies('{}{}-{}'.format(pageurl, prefix, each))
		print("- {}: {}".format(
			datestr,
			', '.join(['{} #{}'.format(part, study) for study, part in  zip(studies, parts)])))


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
	haspart = True
	study = re.findall(r"<strong>.+</strong>.+<em>th.*?</em>study.*?\d+</a>", tmp)
	if study is None:
		haspart = False
		study = re.findall(r"<em>th.*?</em>study.*?\d+</a>", tmp)

	# get the data enclosed in the first and last song
	studies = []
	parts = []
	for each in study:
		res = re.match(r'.+study.+?(\d+)</a>', each)
		studies.append(int(res.group(1)))
		if haspart:
			res = re.match(r'<strong>(.+?):?\s*</strong>', each)
			parts.append(res.group(1))
	return studies, parts


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
