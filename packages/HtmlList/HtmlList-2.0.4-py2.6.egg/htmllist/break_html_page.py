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
The module defines BreakHtmlPage class with some "private" and "public" help
functions.

DEF_EXCLUDE_TAGS is a list of tags names to always exclude (see BreakHtmlPage
documentation)

This module uses html5lib
http://code.google.com/p/html5lib/

If one wants to implement this module functionality using different HTML parsing
library, he/she needs to write a module with the exact same API (all public
functions/methods).
"""

from cStringIO import StringIO
from xml.sax.saxutils import escape

from html5lib import HTMLParser
from html5lib.treebuilders.simpletree import Element

from utills import iter2tuple
from tag_tools import Tag, TagSet

# This is the default excluding tags (as strings),
# I don't think we will ever need to change them.
DEF_EXCLUDE_TAGS = "html", "head", "title", "script", "style", "body"

ENCODING = "utf-8"	# TODO: Do I always need utf-8?

## Private functions that work with the traverse_element function ##

def _write_elm(buff):
	""" Return a function (closure) that render element into buff """
	def __write_elm(elm):
		""" Render an HTML element """
		if elm.type != 5:
			buff.write(elm.toxml().encode(ENCODING))
		else:
			buff.write('<' + elm.name)
			if elm.attributes:
				for name,value in elm.attributes.iteritems():
					value = escape(value,{'"':'&quot;'})
					buff.write(' %s="%s"' % (
						name.encode(ENCODING), value.encode(ENCODING)))
			if elm.childNodes:
				buff.write('>')
			else:
				buff.write(' />')
	return __write_elm

def _write_close_elm(buff):
	""" Same for close element (tag) """
	def __write_close_elm(elm):
		buff.write('</%s>' % elm.name)
	return __write_close_elm

def _is_text_elm(elm):
	""" Returns True if an element is not empty text element.
	Otherwise return None so we continue to scan the tree.
	"""
	if elm.type == 4 and elm.value.strip():
		return True
	return None

class STOP_TRAVERSING: pass

## Public functions ##

def traverse_element(elm, elm_func, elm_close_func, stop_tag, parents):
	""" Traverse the sub tree starting from 'elm', until the end, or until it
	gets to 'stop_tag'. It adds every tag it scans to the 'parents' set.
	On every element it applies 'elm_func' if the result is not None, the
	function returns it. On every (virtual) close element it applies
	'elm_close_func' if it is not None, if the result is not None, the function
	returns it.

	This is a recursive function.
	"""
	if elm is stop_tag: return STOP_TRAVERSING
	res = elm_func(elm)
	if not res is None:
		return res
	if elm.childNodes:
		parents.add(elm)
		for child in elm.childNodes:
			res = traverse_element(
				child, elm_func, elm_close_func, stop_tag, parents)
			if not res is None:
				return res
		if elm_close_func:
			res = elm_close_func(elm)
			if not res is None:
				return res
	return None

def list2text(lst, stop_tag=None):
	""" Render the HTML text a list of HTML elements represent.
	It takes a second argument, stop_tag, which it will stop the rendering of
	the HTML if it finds this tag in one of the child tags, so the returned HTML
	section will not overlap, even if one of the tags in the list spans over the
	next list (which will start with the stop_tag).
	"""
	if not lst: return None
	parents = set()
	buff = StringIO()
	for node in lst:
		if not node.parent in parents:
			if traverse_element(node, _write_elm(buff), _write_close_elm(buff),
			stop_tag, parents) is STOP_TRAVERSING:
				break
	return buff.getvalue()

def validate_list(elm_lst, stop_tag=None, good_elm_func=None):
	""" Scans the sub HTML Element list that in elm_lst, until it finds an
	element that good_elm_func returns True on it.

	elm_lst - A list of tags (html5lib.simpletree.Element).
	stop_tag An optional tag to stop the scan on (like in list2text).
	good_elm_func An optional function that take Element and return boolean.
	The default function checks if the element is none empty text.

	Returns True if found an element such as the above, or False.
	"""
	if not elm_lst: return False
	if not good_elm_func:
		good_elm_func = _is_text_elm
	parents = set()
	for elm in elm_lst:
		if not elm.parent in parents and traverse_element(
		elm, good_elm_func, None, stop_tag, parents):
			return True
	return False

## The main class ##

class BreakHtmlPage(object):
	""" Implements the BreakHtmlPage class using html5lib.
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
		self.include_tags = TagSet()
		self.exclude_tags = TagSet()
		self.exclude_tags += DEF_EXCLUDE_TAGS

	def feed(self, data):
		""" Add text to be parsed. """
		if not self._html:
			self._html = StringIO()
		self._html.write(data)

	def close(self):
		""" Should be called after all HTML text has been feed in. """
		doc = HTMLParser().parse(self._html)
		self._html.close()
		self._orig_lst = tuple(doc)

	def clear(self):
		""" Clear all old data """
		if self._html:
			self._html.close()
		self._html = StringIO()
		self._orig_lst = None
		self._index_lst = None

	@iter2tuple
	def get_tag_list(self):
		""" Return the list of tags in the HTML body. Each tag is a Tag instance
		It also builds a translation list between the indices in the tag-list it
		gives to RepeatPattern and the original HTML list.
		"""
		if not self._orig_lst: return
		self._index_lst = []
		for index, node in enumerate(self._orig_lst):
			if isinstance(node, Element):
				tag = Tag(node.name, node.attributes)
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
			assert html.startswith('<li class="g">')
			assert html.endswith('</li>')
			assert html[14:].find('<li class="g">') == -1


if __name__ == '__main__':
	BreakHtmlPage.test(verbose=True)
	print "Test Passed"

