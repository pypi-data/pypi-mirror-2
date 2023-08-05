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
This module define HtmlListBreak which make sure every HTML section has some
text in it. It is also calculate the average number of words that in the HTML
list. The counting is done BEFORE rendering the list text.
"""

from htmllist_base import HtmlList, InvalidListException, validate_list
from htmllist_base import traverse_list, words_after_element

class HtmlListBreak(HtmlList):
	""" """
	def handle_sub_html(self, lst, next):
		""" Add validation that a sub HTML section has some text in it. """
		# If I will throw InvalidListException from this method, the list will
		# bee discarded
		if not validate_list(lst, next):
			raise InvalidListException()
		return HtmlList.handle_sub_html(self, lst, next)

	def _count_words_after(self, elm):
		""" Add the number of words after an element (tag) to a class member
		counter.
		"""
		self.num_words += words_after_element(elm)


	def avrg_words_in_section(self):
		""" Return the approximate average number of words in a sub HTML section.
		I use a method that return None as argument to the traverse_list
		function, this method updates a class member counter as side effect.
		"""
		html_lst = self._bhp.get_text_list(self._rp.indices_lst)
		total = count = 0
		for lst, next in html_lst:
			count += 1
			self.num_words = 0
			if len(lst) > 1 or lst[0].end < lst[0].close_tag.end:
				traverse_list(lst, self._count_words_after,
					self._count_words_after, next)
			total += self.num_words
		if count == 0: return 0
		return float(total) / count

if __name__ == '__main__':
	pass
	# TODO: Add unit test
