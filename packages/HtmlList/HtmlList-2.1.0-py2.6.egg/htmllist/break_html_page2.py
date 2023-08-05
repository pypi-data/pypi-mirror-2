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
A way to break HTML list without using external library.
I am using regular expressions, it is working significantly faster than with
html5lib.

I don't really need to "parse" the page, only to find all the tags.

The regular expression is based on
http://kevin.deldycke.com/2008/07/python-ultimate-regular-expression-to-catch-html-tags/

The API of the "break_html_page" unit of this package is:

	The BreakHtmlPage class of this module with all the public methods.

	These functions need to be implemented:
		is_text_elm(elm)
		traverse_list(elm_lst, elm_func, elm_close_func=None, stop_elm=None)
		validate_list(elm_lst, stop_elm=None, good_elm_func=None)
		list2text(elm_lst, stop_elm=None)
		words_after_element(elm)
		words_between_elements(start, end)
	See the documentation of these functions.

This API is NOT final
"""

import re
from StringIO import StringIO
from collections import deque

from utills import iter2tuple
from tag_tools import Tag, TagSet

## The Regular Expressions ##

TAGS_RE = """
<
(?P<closing>\/)?
(?P<name>\w+)
(?P<attrs>(?:\s+\w+(?:\s*=\s*(?:\".*?\"|'.*?'|[^'\">\s]+))?)+\s*|\s*)
(?P<self_closing>\/)?
>
"""

ATTRS_RE = """
\s+
(?P<name>\w+)
(?:\s*=\s*
(?:
\"(?P<val1>.*?)\"
|
'(?P<val2>.*?)'
|
(?P<val3>[^'\">\s]+
)))?
"""

# This is the default excluding tags (as strings),
# I don't think we will ever need to change them.
DEF_EXCLUDE_TAGS = "html", "head", "title", "script", "style", "body"

# I must store the HTML page in a global variable...
g_html = None

# A Tag "Struct"
class TagStruct (object): pass

def is_text_elm(elm):
	""" Returns True if an element has some content in it.
	If not it returns None!
	"""
	if not elm.closing and not elm.self_closing and elm.end < elm.close_tag.end:
		if g_html[elm.end:elm.next.start].strip():
				return True
	return None

def traverse_list(elm_lst, elm_func, elm_close_func=None, stop_elm=None):
	""" Traverse the elements list until the end or until it gets to 'stop_elm'.
	On every element it applies 'elm_func', if the result is not None the
	function returns it. On every close element it applies 'elm_close_func' if
	it is not None, if the result is not None the function returns it.
	"""
	if not elm_lst: return None
	end = max([itm.close_tag.end for itm in elm_lst]) # The last close_tag place
	elm = elm_lst[0]
	while elm and elm.start < end:
		if stop_elm and elm.end > stop_elm.start:
			break
		if not elm.closing:
			res = elm_func(elm)
			if not res is None:
				return res
		elif elm_close_func:
			res = elm_close_func(elm)
			if not res is None:
				return res
		elm = elm.next

def validate_list(elm_lst, stop_elm=None, good_elm_func=None):
	""" Scans the sub HTML Elements that in the elm_lst range, until it finds an
	element that good_elm_func returns True on it. This is basically only a
	wrapper of traverse_list.

	elm_lst - A list of TagStruct.
	stop_elm An optional tag to stop the scan on (like in list2text).
	good_elm_func An optional function that take Element and return boolean or
	None. The default function checks if the element contains some text.

	Returns True if found an element such as the above, or False.
	"""
	if not good_elm_func:
		good_elm_func = is_text_elm
	return traverse_list(elm_lst, good_elm_func, stop_elm=stop_elm)

def list2text(lst, stop_elm=None):
	""" Render the HTML text a list of HTML elements represent.
	It takes an optional second argument, stop_elm, which it will stop the
	rendering of the HTML if it finds this tag in one of the child tags, so the
	returned HTML sections will not overlap, even if one of the tags in the list
	spans over the next list (which will start with the stop_elm).
	"""
	if not lst: return None
	start = lst[0].start
	end = max([itm.close_tag.end for itm in lst]) # The last close_tag place
	if stop_elm:
		end = min(end, stop_elm.start)			# See if we are over "stop_elm"
	return g_html[start:end]

def words_after_element(elm):
	""" Return the number of words after an element (tag) until the next element
	"""
	# TODO: Use regex not split!
	if not elm.next:
		return 0
	return len(g_html[elm.end:elm.next.start].split())

def words_between_elements(start, end):
	""" Count the number of words in an HTML section """
	counter = 0
	elm = start
	while elm != end:
		counter += words_after_element(elm)
		elm = elm.next
	return counter

class BreakHtmlPage(object):
	""" Implements the BreakHtmlPage class using regular expressions.
	This class should be used with RepeatPattern in order to get a repetitive
	pattern in an HTML text.

	BreakHtmlPage has two "public" variables: include_tags and exclude_tags.
	These are TagSets, if they are not empty, the class will include-only/
	exclude the tags that in this sets.
	See TagSet documentation for more details.

	This class will not return an overlapping HTML sections.
	"""
	def __init__(self):
		self._html = None			# The HTML buffer
		self._orig_lst = None		# Original list of elements in the page
		self._index_lst = None		# List of indices in orig_lst of the tags we
									# 	work with
		# Regular expression to find the tags
		self._tags_re = re.compile(TAGS_RE, re.I | re.X)
		self._attrs_re = re.compile(ATTRS_RE, re.I | re.X)

		self.include_tags = TagSet()
		self.exclude_tags = TagSet()
		self.exclude_tags += DEF_EXCLUDE_TAGS

	def _parse(self, text):
		""" Create the list of tags from the text. """
		lst = []
		last_tag = None
		for tag in self._tags_re.finditer(text):
			tag_struct = TagStruct()
			tag_struct.name = tag.group("name")
			tag_struct.closing = bool(tag.group("closing"))
			tag_struct.self_closing = bool(tag.group("self_closing"))
			tag_struct.start = tag.start()
			tag_struct.end = tag.end()
			tag_struct.close_tag = tag_struct	# For now
			if last_tag:
				last_tag.next = tag_struct
			last_tag = tag_struct
			if tag.group("attrs"):
				tag_struct.attrs_dict = dict([(attr.group("name"),
					attr.group("val1") or attr.group("val2") or attr.group("val3"))\
					for attr in self._attrs_re.finditer(tag.group("attrs"))])
			else:
				tag_struct.attrs_dict = None
			lst.append(tag_struct)
		return lst

	def _insert_close_tags(self, lst):
		""" close_tag of a TagSturct will be the closing tag if any.
		"""
		balance = deque()
		for tag in lst:
			if not tag.closing and not tag.self_closing:
				balance.appendleft(tag)
			elif tag.closing:	# This is a closing tag - find it's opening pair
				index = 0
				while index < len(balance) and balance[index].name != tag.name:
					index += 1
				if index < len(balance):	# Found the opening tag
					balance[index].close_tag = tag	# Set close_tag
					for i in range(index+1):	# Delete from balance until here
						balance.popleft()

	def element_by_tag_index(self, index):
		""" Return an element from the orig_lst by a Tag index from the tag_lst.
		I need it for other modules (not for this class or RepeatPattern).
		"""
		return self._orig_lst[self._index_lst[index]]

	def feed(self, data):
		""" Add text to be parsed. """
		if not self._html:
			self._html = StringIO()
		self._html.write(data)

	def close(self):
		""" Should be called after all HTML text has been feed in. """
		global g_html
		g_html = self._html.getvalue()
		self._html.close()
		self._orig_lst = self._parse(g_html)
		self._insert_close_tags(self._orig_lst)

	def clear(self):
		""" Clear all old data """
		if self._html:
			self._html.close()
		self._html = None
		self._orig_lst = None
		self._index_lst = None

	@iter2tuple
	def get_tag_list(self):
		""" Return an iterator of tags in the HTML body. Each tag is a Tag
		instance. It also builds a translation list between the indices in the
		tag-list it gives to RepeatPattern and the original HTML list.
		"""
		if not self._orig_lst: return
		self._index_lst = []
		for index, node in enumerate(self._orig_lst):
			if not node.closing:
				tag = Tag(node.name, node.attrs_dict)
				if (not self.include_tags or tag in self.include_tags) and \
				(not self.exclude_tags or tag not in self.exclude_tags):
					self._index_lst.append(index)
					yield tag

	def get_text_list(self, lst):
		""" Return an iterator over lists of elements in an HTML page.
		These lists are the sections we may be interested in.
		The iterator item is two tuple (list, next). next is the first element
		in the next list (or None). It is used to stop the rendering of the HTML
		section (to avoid overlapping)
		"""
		if not self._orig_lst or not self._index_lst or not lst: return
		# Extract the HTML from the original tags list
		for index, entry in enumerate(lst):
			start = self._index_lst[entry[0]]
			end = self._index_lst[entry[1]] + 1	# "end" is the tag after the pattern
			if index < len(lst) - 1:	# The next start tag
				next = self._orig_lst[self._index_lst[lst[index+1][0]]]
			else:
				next = None
			yield (self._orig_lst[start:end], next)

	@classmethod
	def test(cls, verbose=False):
		""" Testing this class

		I'm not testing the HTML overlap prevention (yet).
		An example of it working is if processing the page:
		http://docs.python.org/dev/whatsnew/2.6.html
		"""
		bhp = cls()
		f = open("test_google.html")
		for line in f.readlines():
			bhp.feed(line)
		bhp.close()

		if verbose:
			print "Test the exclusion feature, the inclusion hopefully works the same"
		bhp.exclude_tags += Tag("em"), Tag("a", {"class": "gb2"})
		tag_lst = bhp.get_tag_list()

		assert Tag("html", {"class": "bar"}) not in tag_lst
		assert Tag("a", {"class": "gb2"}) not in tag_lst

		if verbose:
			print "Manually find the 'known pattern' indices"
		start_lst = []
		end_lst = []
		start_tag = Tag("li", {"class": "g"})
		end_tag = Tag("span", {"class": "gl"})

		start_lst = [index for index, tag in enumerate(tag_lst) if tag == start_tag]
		end_lst = [index for index, tag in enumerate(tag_lst) if tag == end_tag]

		assert len(start_lst) == len(end_lst)
		lst = zip(start_lst, end_lst)

		if verbose:
			print "Make sure we are getting the appropriate HTML sections"
		for sub_lst, next in bhp.get_text_list(lst):
			html = list2text(sub_lst, next)
			#print html
			assert html.startswith('<li class=g>')
			assert html.endswith('</div>')
			assert html[14:].find('<li class=g>') == -1


if __name__ == '__main__':
	BreakHtmlPage.test(verbose=True)
	print "Test Passed"

