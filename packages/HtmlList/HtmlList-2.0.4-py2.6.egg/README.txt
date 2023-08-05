HtmlList
========

This package finds repetitive format patterns in an HTML page that contains one or more lists and extracts the sub-html text that creates the patterns.
The idea is that in a typical HTML data page containing a list of items, there will be a repetitive pattern for the human eye (the page format). This pattern can be recognized automatically, and the data in the list can be "scraped".

The user should inherit from *HtmlList* and overwrite the *handle_sub_html* method in order to extract the relevant data.

I built one *HtmlList* class - *HtmlListBreak* that verifies there is some text in the sub HTML sections, and counts the total number of words in the HTML list. This class is in the *htmllist_break* module.

The *htmllist_demo* module can be used as a simple stand-alone demon to process HTML pages from a web browser (see Testing below). This module runs all (for now two) algorithms on the HTML text, and displays a list of HTML-lists ordered by some relevance factor.

 - This package is still in development, there is an old version on PyPi. Download it from http://pypi.python.org/pypi/HtmlList/ or by running *easy_install HtmlList*

 - Up to date subversion archive of the project is in https://pyhtmllist.svn.sourceforge.net/svnroot/pyhtmllist/ or for browsing  http://pyhtmllist.svn.sourceforge.net/viewvc/pyhtmllist/

 - This package needs python 2.6 (but it will be easy to get it to work with 2.5).

--------------------------------------------------------------------------------

Basic Usage Example
===================

	>>> from htmllist.htmllist_base import HtmlList
	>>> hl = HtmlList()
	>>> hl.set_text(some_html_page_taxt)
	>>> hl.process()
	>>> itr = hl.get_html_list()
	>>> if itr:   # must make this test
	...    for itm in itr:
	...        print itm
	... else:
	...    print "Cannot parse the page"

for a more detailed example look at *htmllist.htmllist_demo.py*

--------------------------------------------------------------------------------

About the algorithms
====================

I am trying to detect the most prevalent patterns on the page, assuming that these sections of the page will hold the main content. A "pattern" is a repetitive sequence of HTML tags (but other tags can still be in between the sequence items). An "occurrence" is every place in the page this pattern exists. I'm taking the pattern where it's length multiplied by the number of occurrences multiplied by some kind of standard deviation on the occurrences indices, is the greatest. The pattern must occur more than once.

"Count Tags" in the *repeat_pattern* module
-------------------------------------------
The new Count Tags algorithm is based upon the heuristic assumption that in most pages the prevalent pattern will have two or more unique tags in it. The package will only recognize patterns that have these unique tags in them.

The idea is to count tags and put them in "buckets" according to the number of occurrences of each tag. The second level of distribution to buckets is tags that appear in a sequence. Each index of a new item in a bucket should be greater than the last item index but less than than the next index of the first item...
After I have the buckets, I simply find the one with the highest factor and try to expand it as much as I can. For more details see the *repeat_pattern* documentation.

"Tags Pattern" in the *repeat_pattern2* module
----------------------------------------------
The old Tags Pattern algorithm is working with an improved Suffix Tree data structure. By building a tree from the input list, I can find repetitive patterns relatively fast. In every node of the tree I also keep an indices list of the occurrence of this sequence on the input list. This allows me to check for overlapping, calculate derivative value, and find all the occurrences of the chosen pattern efficiently.

Breaking HTML pages
-------------------
The *break_html_page* module takes an HTML text and builds a list of tags (with optional attributes). So the *repeat_pattern* module works on a list of arbitrary items, it does not know what an HTML tag is. I now use *break_html_page2* that does not really parse the page, instead extracts the tags from it using regular expressions. It is much faster.

The sub-classes of *HtmlList* use the two previous types of modules to extract the information needed from an HTML page.

More about calculating a derivative on a list
---------------------------------------------
I use the term derivative as the distances between numbers in a list. This is a list by itself, with one less item than the original list. I'm calculating the normalized standard deviation on the first derivative of the occurrences list. This gives some idea of how randomly the occurrences are distributed on the page. This value is normalized to be between 0 and 1, lower being better. A lower value should indicate a good pattern on a typical HTML page.

The "weight" of a list
----------------------
The weight of a list is a number between zero and one that indicates how close this list is to the center of the page (the center of the input tag list). The weight is also factored in when calculating the list relevance factor.

--------------------------------------------------------------------------------

If the system doesn't work well on pages from some websites, you should try to change some parameters of *HtmlListXXX*:

	*min_len* - Minimum number of tags in the pattern.

	*min_repeat* - Minimum number of times the pattern should repeat in the page. Note: min_repeat must be more then one!

	*max_repeat* - Maximum number of times the pattern should repeat in the page.

	*max_stdv* - Maximum normalized standard deviation of the distances between occurrences. This is a number between 0 and 1. 0 means that the occurrences are in sequence (no other tags in between). 1 means that there is no importance to the position of the occurrences in the page. In a normal HTML page you should keep this number low, but maybe larger than zero.

See the documentation for more details.

--------------------------------------------------------------------------------

Testing
=======

There is a regression tests for this package in the test directory. It tests the best result list on several HTML pages from different types of pages (news, shopping, search results, etc.). It still does not test the other, less relevant, results.

There is a way for a user to see how the system works by running *htmllist_demo.py*. The *setup.py* installer sets an *htmllist_demo* script that runs this module.
This script will run in the background. The user then should "Save As" the HTML pages from a web browser (as "HTML only") to the sub-folder "temp" of this package. The script will monitor this folder and try to process any file in it. It will then open the resulting HTML file in the web browser.
This script uses both algorithms on the page, and from each one takes the best three lists. It then adds the total number of words in each list to the relevance factor of the list, and resorts the results in the descending order of this factor.

try: *htmllist_demo --help*

--------------------------------------------------------------------------------

ToDo
====
 - Implement the "Tags Pattern" algorithm using a suffix array instead of the suffix tree.
 - Find a way to recognize irrelevant lists, and remove them from the results.
 - Take the HTML data from a browser DOM module and not from the HTML in the page. As a result I will also get dynamic HTML.
 - Use this package to highlight important sections of HTML pages in a web browser (Firefox).

--------------------------------------------------------------------------------

This package uses *html5lib* in *break_html_page* to parse the HTML, you can download *html5lib* from http://code.google.com/p/html5lib/ (I don't use this module anymore. I now use *break_html_page2*).

HtmlList was originally developed at Blackwood Productions - http://blackwoodproductions.com - for gathering search engines results. I now direct it more for highlighting HTML pages (mainly on limited screens - smart phones), but it still works on search engines pages.

HtmlList is licensed under the GNU General Public License, but more liberal license can be arranged.

Erez Bibi
erezbibi@users.sourceforge.net

