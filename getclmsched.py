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
months = ["enero", "pebrero", "marso", "abril", "mayo", "hunyo", "hulyo", "agosto", "setyembre",
	"oktobre", "nobyembre", "disyembre"]


def main(month, year):
	"""This is the main function

	Args:
	- `month` (`int`): self-explained
	- `year` (`int`): self-explained

	Returns:
	- `None`
	"""
	site = urllib2.urlopen("https://www.jw.org/tl/publikasyon/jw-workbook-para-sa-pulong/"
		"{}-{}-mwb/".format(months[month - 1], year))
	data = site.read()
	res = re.findall(r"(?P<url>/.+?iskedyul-ng-pulong.+\d+/?)\">(?P<daterange>.+?)</a>", data)
	for each in res:
		tmp = each[1].decode("latin-1")
		print("-" * 80)
		print("{}".format(tmp.replace(u"\xe2\x80\x93", u"-")))
		for program in grabweekdata(URL_HEADER + each[0]):
			if program.isupper() or program.startswith("Pambungad") \
					or program.startswith("Repaso") or program.startswith("Awit"):
				print(program)
			else:
				print("    " + program)


def grabweekdata(url):
	"""Grab the per-week program data.

	Args:
	- `url` (`str`): URL of the per week's page

	Returns:
	- `list`: all the program's data including the header of each
	program's section
	"""
	site = urllib2.urlopen(url)
	# get the HTML-stripped data
	tmp = site.read()
	data = re.sub(r"<[^<]+?>", "", tmp.decode("latin-1"))
	songs = re.findall(r"Awit \d+", data)
	# get the data enclosed in the first and last song
	start = data.index(songs[0])
	stop = data.index(songs[-1])
	res = [each.strip() for each in re.findall(r"\n.+?\r\n", data[start:stop]) if each.strip()]
	programs = [songs.pop(0)]
	for each in res:
		tmp = each.replace(u"\xe2\x80\x94", "-").replace(u"\xc2\xb6", "par.") \
			.replace(u"\xe2\x80\x9c", "\"").replace(u"\xe2\x80\x9d", "\"") \
			.replace(u"\xc2\xa0", " ").replace(u"\xe2\x80\x8b", "-")
		if each.isupper():
			programs.append(tmp)
			if tmp.startswith("PAMUMUHAY"):
				programs.append(songs.pop(0))
			continue
		if " min." not in tmp:
			continue
		start = tmp.index(" min.")
		pos = tmp.index(")", start) + 1
		programs.append(tmp[:pos])
	programs.append(songs.pop())
	return programs


if __name__ == "__main__":
	month = int(raw_input("Month (1-12 where 1=Jan & 12=Dec): "))
	year = int(raw_input("Year (ex: 2017): "))
	main(month, year)
