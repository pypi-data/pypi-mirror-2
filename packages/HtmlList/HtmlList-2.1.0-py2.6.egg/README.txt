HtmlList
========

#This package finds repetitive format patterns in an HTML page that contains one or more lists and extracts the sub-html text that creates the patterns.#
The idea is that in a typical HTML data page containing a list of items, there will be a repetitive pattern for the human eye (the page format). This pattern can be recognized automatically, and the data in the list can be extracted.

The user should inherit from *HtmlList* and overwrite the *handle_sub_html* method in order to extract the relevant data. I built one *HtmlList* class - *HtmlListBreak* that verifies there is some text in the sub HTML sections, and counts the total number of words in the HTML list. This class is in the *htmllist_break* module.

The *htmllist_demo* module can be used as a simple stand-alone demon to process HTML pages from a web browser (see Testing below). This module runs all (enabled) algorithms on the HTML text, and displays a list of HTML-lists ordered by some relevance factor.

#A note about the version numbers:# The current version is 2.1.x. When the very first version of this package want to production in my old working place, I set the major to one. When I redesigned the entire package and implemented the "new" algorithm, I set the major to two. For practical reasons you can consider it as version 0.1.x.

 - This package is still in development, there is a stable version on PyPi. Download it from http://pypi.python.org/pypi/HtmlList/ or by running #easy_install HtmlList#

 - Up to date subversion archive of the project is in https://pyhtmllist.svn.sourceforge.net/svnroot/pyhtmllist/ or for browsing  http://pyhtmllist.svn.sourceforge.net/viewvc/pyhtmllist/

 - This package needs python 2.6 (but it will be easy to get it to work with 2.5).

--------------------------------------------------------------------------------

Basic Usage Example
===================

	>>> from htmllist.htmllist_base import HtmlList
	>>> hl = HtmlList()
	>>> hl.set_text(some_html_page_taxt)
	>>> hl.process()
	>>> lst = hl.get_html_list()
	>>> if lst:
	...    for itm in lst:
	...        print itm
	... else:
	...    print "Cannot parse the page"

for a more detailed example look at *htmllist.htmllist_demo.py*

--------------------------------------------------------------------------------

Testing
=======

There is a regression test module for this package in the test directory. It tests the best result list on several HTML pages from different types of pages (news, shopping, search results, etc.). It still does not test the other, less relevant, results.

There is a way for a user to see how the system works by running *htmllist_demo.py*. The *setup.py* installer sets an *htmllist_demo* script that runs this module.
This script will run in the background. The user then should "Save As" the HTML pages from a web browser (as "HTML only") to the folder this script monitors ("./temp" by default). The script will try to process any HTML file in this folder, and will then open the resulting HTML file in the web browser. However when running from an egg file you probably must give a --monitor argument with the directory you want to monitor.
This script uses all (enabled) algorithms on the page, and from each one takes the best three lists.

try: *htmllist_demo --help*

--------------------------------------------------------------------------------

Optional Configuration
======================

If the system doesn't work well on pages from some websites, you should try to change some parameters of *HtmlListXXX* (also arguments of *htmllist_demo*):

	#min_len# - Optional minimum length of the output pattern (sub-list),
	default = 2
	#max_len# - Optional maximum length of the output pattern (sub-list),
	default = 0 which is no limit.
	#min_repeat# - Optional minimum time the pattern should repeat in the list,
	default = 2. Note: min_repeat must be more then one!
	#max_repeat# - Optional maximum time the pattern should repeat in the list,
	a value of zero cancels this limit, default = 0.
	#max_stdv# - Optional maximum normalized standard deviation of the distances
	between occurrences. This is a number between 0 and 1. 0 means that the
	occurrences are in sequence (no other item in between). 1 means that there
	is no importance to the position of the occurrences in the list. The default
	is one.
	#min_weight# - Optional minimum weight of the occurrences list (see the
	weight method), a value of zero cancels this limit, default = 0.
	#min_coverage# - Optional minimum coverage of the occurrences list (see the
	coverage method), a value of zero cancels this limit, default = 0.
	#min_comp# - Optional minimum compactness of the occurrences list (see the
	compactness method), a value of zero cancels this limit, default = 0.

See the documentation for more (up to date) details.

--------------------------------------------------------------------------------

ToDo
====
 - Find a way to recognize irrelevant lists, and remove them from the results.
 - Take the HTML data from a browser DOM module and not from the HTML in the page. As a result I will also get dynamic HTML.
 - Use this package to highlight important sections of HTML pages in a web browser (Firefox).

--------------------------------------------------------------------------------

About the algorithms
====================

I am trying to detect the most prevalent patterns on the page, assuming that these sections of the page will hold the main content. A "pattern" is a repetitive sequence of HTML tags (but other tags can still be in between the sequence items). An "occurrence" is every place in the page this pattern exists. The rules for choosing the pattern are almost identical to the rules in the IEPAD paper (http://portal.acm.org/citation.cfm?id=372182). These rules work much better than my old rules (and some of them are identical to some of my old rules). The pattern must occur more than once.

* For more detailed (and maybe more up to date) description of the algorithms see the modules documentation.

"Count Tags" in the *repeat_pattern* module
-------------------------------------------
The new Count Tags algorithm is based upon the heuristic assumption that in most pages the prevalent pattern will have two or more unique tags in it. The package will only recognize patterns that have these unique tags in them.

The idea is to count tags and put them in "buckets" according to the number of occurrences of each tag. The second level of distribution to buckets is tags that appear in a sequence. Each index of a new item in a bucket should be greater than the last item index but less than than the next index of the first item...
After I have the buckets, I simply find the one with the highest factor and try to expand it as much as I can. For more details see the *repeat_pattern* documentation.

"Tags Pattern" in the *repeat_pattern2* module
----------------------------------------------
The old Tags Pattern algorithm is working with an improved Suffix Tree data structure. By building a tree from the input list, I can find repetitive patterns relatively fast. In every node of the tree I also keep an indices list of the occurrence of this sequence on the input list. This allows me to check for overlapping, calculate derivative value, and find all the occurrences of the chosen pattern efficiently.

"Tags Pattern" using suffix array in the *repeat_pattern_suffix* module
-----------------------------------------------------------------------
I now working with a suffix array instead of suffix tree. The idea is similar but the algorithm is completely different. It is running faster and take about half the memory. I use a slightly modified version of the *tools* module of the #pysuffix# project, to build the suffix array. http://code.google.com/p/pysuffix/

Breaking HTML pages
-------------------
The *break_html_page* module takes an HTML text and builds a list of tags (with optional attributes). So the *repeat_pattern* module works on a list of arbitrary items, it does not know what an HTML tag is. I now use *break_html_page2* that does not really parse the page, instead extracts the tags from it using regular expressions. It is much faster.

The sub-classes of *HtmlList* use the two previous types of modules to extract the information needed from an HTML page.

Standard Deviation and calculating a derivative on a list
---------------------------------------------------------
I use the term derivative as the distances between numbers in a list. This is a list by itself, with one less item than the original list. I'm calculating the normalized standard deviation on the first derivative of the occurrences list. This gives some idea of how randomly the occurrences are distributed on the page. This value is normalized to be between 0 and 1, lower being better. A lower value should indicate a good pattern on a typical HTML page.

The "weight" of a list
----------------------
The weight of a list is a number between zero and one that indicates how close this list is to the center of the page (the center of the input tag list). The weight is also factored in when calculating the list relevance factor.

Coverage and Compactness
------------------------
Are measurements taken from the IEPAD paper, they are also factored into the final relevance factor.

--------------------------------------------------------------------------------

- This package uses *html5lib* in *break_html_page* to parse the HTML, you can download *html5lib* from http://code.google.com/p/html5lib/ (I don't use this module anymore. I now use *break_html_page2*).

- I took some ideas from the excellent IEPAD paper (http://portal.acm.org/citation.cfm?id=372182). Thank you.

- HtmlList was originally developed at #Blackwood Productions# - http://blackwoodproductions.com, and #Netz Internet Solutions# - http://netzbiz.com - for extracting search engines results. I now direct it more for highlighting HTML pages (mainly on limited screens - smart phones), but it can also be used for automatic content extraction from HTML pages.

- HtmlList is licensed under the GNU General Public License, more liberal license can be arranged.

28-05-2010
Erez Bibi
erezbibi@users.sourceforge.net

*txt2html --infile README.txt --outfile index.html --titlefirst*
