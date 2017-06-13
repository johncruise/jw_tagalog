from __future__ import unicode_literals, print_function
import urllib2
import re

# +++ constants
URL_HEADER = "https://www.jw.org"


def main():
	"""TODO: put documenation here"""
	site = urllib2.urlopen("https://www.jw.org/tl/publikasyon/jw-workbook-para-sa-pulong/"
		"agosto-2017-mwb/")
	data = site.read()
	res = re.findall(r"(?P<url>/.+?iskedyul-ng-pulong.+\d+/?)\">(?P<daterange>.+?)</a>", data)
	for each in res:
		tmp = each[1].decode("latin-1")
		print("-" * 80)
		print("{}".format(tmp.replace(u"\xe2\x80\x93", u"-")))
		for program in grabweekdata(URL_HEADER + each[0]):
			if program.isupper() or program.startswith("Pambungad") or program.startswith("Repaso"):
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
	programs = []
	for each in res:
		tmp = each.replace(u"\xe2\x80\x94", "-").replace(u"\xc2\xb6", "par.") \
			.replace(u"\xe2\x80\x9c", "\"").replace(u"\xe2\x80\x9d", "\"") \
			.replace(u"\xc2\xa0", " ").replace(u"\xe2\x80\x8b", "-")
		if each.isupper():
			programs.append(tmp)
			continue
		if " min." not in tmp:
			continue
		start = tmp.index(" min.")
		pos = tmp.index(")", start) + 1
		programs.append(tmp[:pos])
	return programs


if __name__ == "__main__":
	main()
