#!python

# HtmlList - Finds repetitive format patterns in an HTML page.
# Copyright (C) 2010  Erez Bibi (erezbibi@users.sourceforge.net)
#
# This file is part of HtmlList.
#
# HtmlList is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HtmlList is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HtmlList.  If not, see <http://www.gnu.org/licenses/>.

"""
When run as a stand-alone this module creates a quick and dirty way to break
pages from a web browser in order to test this package.
The user should save web browser pages to a folder. The script runs in the
background, monitors this folder and will process files in it. Then it tries to
open the result as an HTML page again using a web browser.

If the option "--std" is given on the command line, it will process an HTML text
from the standard input and print an XML output to the standard output.

It process the page using all algorithms and print the best X results from each
one. The results will be sorted by a relevance factor (which hopefully work well)

try: htmllist_demo.py --help
"""
from __future__ import with_statement
from glob import iglob
from webbrowser import open as web_open
from sys import argv
from optparse import OptionParser, OptionGroup
import os, time, re, sys, cPickle

from htmllist_break import HtmlListBreak
from repeat_pattern import RepeatPattern
from repeat_pattern2 import RepeatPattern as RepeatPatternOld
from repeat_title import RepeatPattern as RepeatTitle
from utills import strip_tags, strip_scripts

ALGO_DICT = {
	"Count Tags": RepeatPattern,
	"Tags Pattern": RepeatPatternOld,
	"Titles": RepeatTitle,
}

EXCLUDE_TAGS = None # Comma separated tags names: "b,u,i,em"
INCLUDE_TAGS = None
MIN_LEN = 1
MAX_LEN = 20
MIN_REPEAT = 5
MAX_REPEAT = 60
MAX_STDV = 0.1
MAX_PATTERNS = 3

WORDS_IN_TITLE = 5	# This is for the output XML titles of the HTML sections

def get_options_parser():
	""" Return the command line arguments parser. """
	parser = OptionParser(description=main.__doc__)
	parser.add_option("-m", "--monitor", action="store", type="string",
		default="./temp", dest="monitor",
		help="""Directory to monitor [default: %default]""")
	parser.add_option("-o", "--outfile", action="store", type="string",
		default="./temp.html", dest="outfile", help="""Output file [default: %default]""")
	parser.add_option("-s", "--std", action="store_true", dest="std", default=False,
		help="""Get the input HTML from the standard input and write the output
to the standard output, mutual exclusive to --monitor, --output and --test
[default: %default]""")
	parser.add_option("-v", "--verbose", action="store", type="int", default="0",
		dest="verbose",  help="""Verbose mode (level 0-5) [default: %default]""")

	group = OptionGroup(parser, "HTML List Configuration",
		"""Pass custom configuration to the htmllist package (See documentation
for help)""")
	group.add_option("--include_tags", action="store", type="string",
		default=EXCLUDE_TAGS, dest="include_tags", help="[default:%default]")
	group.add_option("--exclude_tags", action="store", type="string",
		default=EXCLUDE_TAGS, dest="exclude_tags", help="[default:%default]")
	group.add_option("--min_len", action="store", type="int",
		dest="min_len", help="[default:%s]" % MIN_LEN)
	group.add_option("--max_len", action="store", type="int",
		dest="max_len", help="[default:%s]" % MAX_LEN)
	group.add_option("--min_repeat", action="store", type="int",
		dest="min_repeat", help="[default:%s]" % MIN_REPEAT)
	group.add_option("--max_repeat", action="store", type="int",
		dest="max_repeat", help="[default:%s]" % MAX_REPEAT)
	group.add_option("--max_stdv", action="store", type="float",
		dest="max_stdv", help="[default:%s]" % MAX_STDV)
	group.add_option("--max_pttrn", action="store", type="int",
		dest="max_pttrn", help="[default:%s]" % MAX_PATTERNS)
	parser.add_option_group(group)

	group = OptionGroup(parser, "For Regression Tests",
		"""Normal user should not use these options (See documentation for help)""")
	group.add_option("--test", action="store_true", dest="test",
		default=False, help="""Create a regression test [default:%default]""")
	parser.add_option_group(group)

	return parser

def prepare(options, algo_name, break_cls=None):
	""" Create an HtmlList object  by the algorithm name """
	if not options.std: print "\nusing the %s algorithm" % algo_name
	hl = HtmlListBreak(pattern_cls=ALGO_DICT[algo_name], break_cls=break_cls)
	hl.algo_name = algo_name

	if options.exclude_tags:
		hl.exclude_tags += options.exclude_tags.split(',')
	if options.include_tags:
		hl.include_tags += options.include_tags.split(',')
	if options.min_len:
		hl.min_len = options.min_len
	else:
		hl.min_len = MIN_LEN
	if options.max_len:
		hl.max_len = options.max_len
	else:
		hl.max_len = MAX_LEN
	if options.min_repeat:
		hl.min_repeat = options.min_repeat
	else:
		hl.min_repeat = MIN_REPEAT
	if options.max_repeat:
		hl.max_repeat = options.max_repeat
	else:
		hl.max_repeat = MAX_REPEAT
	if options.max_stdv:
		hl.max_stdv = options.max_stdv
	else:
		hl.max_stdv = MAX_STDV
	if options.max_pttrn:
		hl.max_patterns = options.max_pttrn
	else:
		hl.max_patterns = MAX_PATTERNS
	hl.debug_level = options.verbose
	return hl

def find_title(html):
	""" Find a possible title for this HTML section (XML version). """
	text = strip_scripts(html)
	text = strip_tags(text)
	lst = text.split(None, WORDS_IN_TITLE + 1)
	title = ' '.join(lst[:WORDS_IN_TITLE])
	title = title.replace('<', "&lt;").replace('>', "&gt;") + "..."
	return title

def orderd_htmllists(hls):
	""" A generator for html-lists ordered by the revised list factor.
	The new factor take into account the number of words in sub-html section.
	"""
	lst = [(hl, i, hl.factor * hl.words_in_section()) for hl in hls \
		for i in hl]
	lst = filter(lambda x: x[2] > 10, lst)
	lst.sort(key=lambda x: x[2], reverse=True)
	for hl, i ,factor in lst:
		# Setting pattern_num value has the same effect as iterating through
		# the HtmlList object
		hl.pattern_num = i
		hl.new_factor = factor
		yield hl


def print_html(hls, fl):
	""" Build an HTML version of the list and write it to the file object 'fl'. """
	fl.write(u'<HTML><HEAD><TITLE>Html-List Breakdown</TITLE></HEAD><BODY><DIV>\n\n')
	for hl in orderd_htmllists(hls):
		fl.write(
			u"\n</DIV><HR>=== Factor = %s Algorithm: %s ===<HR><DIV>\n" % \
				(round(hl.new_factor), hl.algo_name))
		itr = hl.get_html_list()
		if not itr or not hl.is_list_valid: continue
		for sub in itr:
			fl.write(sub)
			fl.write(u"\n</DIV><HR><DIV>\n")
	fl.write(u"\n</DIV></BODY></HTML>")

def print_xml(hls, fl):
	""" Build an XML version of the list and write it to the file object 'fl'. """
	fl.write('<?xml version="1.0"?>\n')
	fl.write('\n<LISTS>\n')
	for hl in orderd_htmllists(hls):
		itr = hl.get_html_list()
		if not itr or not hl.is_list_valid: continue
		fl.write('\n<SECTIONS factor="%s" algo="%s">' % \
			(hl.new_factor, hl.algo_name))
		for sub in itr:
			fl.write('\n\t<SECTION factor="%s">\n\t<TITLE>\n\t\t' \
				% round(hl.factor))
			fl.write(find_title(sub))
			fl.write('\n\t</TITLE> \n\t<HTML>\n\t\t<![CDATA[\n')
			fl.write(sub)
			fl.write('\n\t\t]]> \n\t</HTML>\n\t</SECTION>')
		fl.write('\n</SECTIONS>\n')
	fl.write('\n</LISTS>\n')

def process(fl, options):
	""" Process an HTML file, returns a list of iterators """
	results = []
	text = fl.read()
	for count, name in enumerate(ALGO_DICT.keys()):
		if count == 0:
			hl = prepare(options, name)
			hl.set_text(text)
		else:
			hl = prepare(options, name, break_cls=hl.break_cls)
		hl.process()
		results.append(hl)
	return results

def process_std(options):
	""" Run the script once on stdin, the output goes to sdtout. """
	hls = process(sys.stdin, options.old, options)
	print_xml(hls, sys.stdout)

def main(argv):
	""" A quick and dirty way to process HTML pages from a web browser. Save
	pages as "HTML only" to the MONITOR directory. The script runs in the
	background, will process these files, and reopen the result page.
	"""
	options, args = get_options_parser().parse_args(argv)

	if options.std:
		process_std(options)
		return

	SLEEP = 0.5
	if not os.path.exists(options.monitor):
		os.mkdir(options.monitor)
	print "Waiting..."

	while True:		#  Poll a folder indefinitely (need to work on Windows too:)
		time.sleep(SLEEP)
		for fl in iglob(options.monitor + "/*"):
			# If file exists - process, open in browser and delete them
			print "Handling:", fl
			with open(fl) as html_file:
				start = time.time()
				hls = process(html_file, options)
				duration = time.time() - start
				if hls:
					if options.test:
						hl = orderd_htmllists(hls).next()
						itr = tuple(hl.get_html_list())
					with open(options.outfile, "wb") as flo:
						print_html(hls, flo)
					web_open("file://%s" % os.path.abspath(options.outfile),
						new=2, autoraise=1)
				else:
					print "Cannot find a pattern"
			print "Processing took:", duration
			if options.test:
				with open("temp.rslt", "wb") as rslt:
					cPickle.dump(itr, rslt)
					cPickle.dump(hl.algo_name, rslt)
					cPickle.dump(options, rslt)
				return
			os.remove(fl)

			print "Waiting..."

if __name__ == '__main__':
	main(sys.argv)
