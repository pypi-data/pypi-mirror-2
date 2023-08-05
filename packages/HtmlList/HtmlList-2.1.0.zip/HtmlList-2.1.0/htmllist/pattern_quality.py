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
This module tries to assess the quality of a pattern on an HTML page. It has
more information than the RepeatPattern classes because it sees the HTML page
itself (through the BreakHtmlPage class).

The only "public" function is "pattern_quality" that take RepeatPattern object
and BreakHtmlPage object and return a number between 0 and 1. The higher the
number the better the quality.

The current implementation checks the deviation of the number of words in each
section of a pattern in each occurrences. But in the future I may change this
assessment without having to change the usage of this module.
"""

from break_html_page2 import words_between_elements

def _print_matrix(matrix):
	""" Debugging function """
	for i in range(len(matrix)):
		print '\t'.join(str(elm) for elm in matrix[i])

def _derivative(lst):
		""" Return a list of numbers of the absolute distances between numbers
		in the input list.
		lst - A list of numbers.
		"""
		if len(lst) < 2: return []
		return [abs(lst[i+1] - lst[i]) for i in range(len(lst) - 1)]

def _deviation(lst):
		""" Return an inverse normalized deviation in a list of numbers.
		lst - A list of numbers
		Returns a number between 0 and 1 (1 = no deviation)
		"""
		if not lst: return 0
		length = len(lst)
		avg = float(sum(lst)) / length
		max_dev = max(lst) - min(lst)
		if max_dev == 0: return 1
		sum_dev = sum(map(lambda x: abs(x-avg), lst))
		return 1 - ((sum_dev / length) / max_dev)

def _avrg_deviation(matrix):
	""" Calculates the average normalized deviation on the derivatives of a
	matrix columns.
	"""
	devs = [_deviation(_derivative(row)) for row in matrix]
	return sum(devs) / len(devs)


def pattern_quality(rp, bhp):
	""" Access a pattern quality on an HTML page.
	rp - RepeatPattern object.
	bhp - BreakHtmlPage object
	Return a number between 0 to 1, the higher the number the better the quality.
	"""
	# Every column in the matrix is the number of "words" after each tag from
	# the pattern. Every row is a specific occurrence of the pattern (index).
	matrix = [[] for _ in range(len(rp.pattern))]
	for i, index in enumerate(rp.indices_lst):
		start, end = index
		last_index = start
		max_section = bhp.element_by_tag_index(start).close_tag
		for j, itm in enumerate(rp.pattern[1:]):
			index = rp._input_lst.index(itm, last_index, end+1)
			close_tag = bhp.element_by_tag_index(index).close_tag
			if close_tag.end > max_section.end:
				max_section = close_tag
			matrix[j].append(words_between_elements(
				bhp.element_by_tag_index(last_index),
				bhp.element_by_tag_index(index)))
			last_index = index
		matrix[len(rp.pattern)-1].append(words_between_elements(
			bhp.element_by_tag_index(last_index), max_section))
	#_print_matrix(matrix)
	#print ">>>", _avrg_deviation(matrix)
	return _avrg_deviation(matrix)




