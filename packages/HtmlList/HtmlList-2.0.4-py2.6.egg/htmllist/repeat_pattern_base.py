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
This is a base class for both algorithms for the repeat-pattern class.
It defines some common help methods and the classes interface.
If in the future there will be other algorithms, they will all extend this class.

26-03-2010 - This class is now finding and returning multiple patterns
	* I canceled the legacy "lazy" mode - it doesn't work with multiple patterns.
	* The user should call "process" before calling "get_html_list".
	* The property "output_lst" is now called "pattern"
	* The property "best_factor" is now called "factor"
	* Other then that the default behavior is to return only one pattern and
	there is no change to the interface.

	This class is an iterator over the patterns. When working with multiple
	patterns we need to set the configuration parameter to a number bigger then
	one. In order to get the patterns do something like:

	>>> if rp.process(lst):
	>>> 	for i in rp:
	>>>			print rp.pattern
	>>>			print rp.indices_lst

	* And there is also a sort method:

	>>> rp.sort(rp.INDICES)		# First pattern first
	>>> rp.sort(rp.PATTERN)		# Longest pattern first
	>>> rp.sort(rp.REPEATS)		# Prevalent pattern first
	>>> rp.sort(rp.FACTOR)		# best pattern first (the default)
"""

from collections import Iterable
import math


class RepeatPatternBase(Iterable):
	"""
	Base class for the RepeatPattern classes
	"""

	## Fields Constants ##
	PATTERN = 0
	INDICES = 1
	FACTOR = 2
	REPEATS = 3		# I need it for sorting but it is not a real matrix field

	NUM_FIELDS = 3

	# "length one magic" is a rule that say: If the number of items in the
	# pattern is one, the STDV must be below a special minimum (the value of
	# this flag). Set to None to disable this "magic".
	LEN_ONE_MAGIC = 0

	def __init__(self, min_len=2, max_len=0, min_repeat=2, max_repeat=0,
		max_stdv=1, max_patterns=1, debug_level=0):
		""" Parameters:
		min_len - Optional minimum length of the output pattern (sub-list),
			default = 2
		max_len - Optional maximum length of the output pattern (sub-list),
			default = 0 which is no limit.
		min_repeat - Optional minimum time the pattern should repeat in the list,
			default = 2.
			Note: min_repeat must be more then one!
		max_repeat - Optional maximum time the pattern should repeat in the list,
			a value of zero cancels this limit, default = 0.
		max_stdv - Optional maximum normalized standard deviation of the
			distances between occurrences. This is a number between 0 and 1.
			0 means that the occurrences are in sequence (no other item in
			between). 1 means that there is no importance to the position of the
			occurrences in the list. The default is one.
		max_patterns - Optional maximum number of possible patterns to find. The
			default is one.
		debug_level - Print debugging messages. A number between 0 (none)
			and 5 (all)
		All parameters can be also controlled by changing class members with the
		same names.
		"""
		## Configuration Parameters ##
		self.min_len = min_len
		self.max_len = max_len
		self.min_repeat = min_repeat
		self.max_repeat = max_repeat
		self.max_stdv = max_stdv
		self.max_patterns = max_patterns
		self.debug_level = debug_level
		self.init()

	def init(self, input_lst=None):
		""" Initialize this instance (may be called more then once) """
		## Input ##
		self._input_lst = input_lst

		## Output ##
		self._num_patterns = 0		# Number of possible patterns found.

		## Internal ##
		self._matrix = []
		self._pattern_num = 0		# The pattern that we are working with

	def __iter__(self):
		""" Iterate over patterns when working with multiple patterns.
		This iterator has side effects, so nesting iteration will not work.
		"""
		for i in range(self._num_patterns):
			self._pattern_num = i
			yield i

	############################################################################

	## Indices Statistics ##

	def _derivative(self, lst, order=1):
		""" This method preforms discrete derive on a list of numbers. This is
		the list of gaps between the numbers of the list.
		order - the derive order.
		Returns a list of numbers or an empty list
		"""
		while order:
			if len(lst) < 2: return []
			lst = [abs(lst[i+1] - lst[i]) for i in range(len(lst) - 1)]
			order -= 1
		return lst

	def _nstdv(self, lst):
		""" This method calculates some kind of normalized standard deviation on
		a list of numbers. It calculates a regular standard deviation and then
		divide it by the total length of the list of items we are working on
		(this is a class member), the result should be equal or bigger than zero
		but less than one.
		"""
		length = len(lst)
		if length == 0: return 0
		if len(self._input_lst) == 0: return 1
		avg = float(sum(lst)) / length
		sqr_sum = float(sum(map(lambda x: x*x, lst)))
		return (math.sqrt((sqr_sum / length) - (avg * avg))) / len(
			self._input_lst)

	def _weight(self, indices):
		""" The weight of a pattern is the distance between the middle index of
		the input-list and the middle of the bucket pattern's span (that is the
		middle between the first start index and the last end index).
		The weight is normalized to be between 0 and 1. The closer the distance
		the higher the weight.

		In an HTML page the most important list should be near the middle of the
		rendered page, and that imply in many cases the middle of the HTML tags
		list. It is a questionable assumption but it seems to prevent picking a
		menu list in the top or left of a page.
		"""
		half_len = len(self._input_lst) / 2.0
		mid_pattern = (indices[0][0] + indices[-1][1]) / 2.0
		weight = 1 - ((abs(half_len - mid_pattern) + 1) / half_len)
		return weight

	############################################################################

	## Properties ##

	@property
	def num_patterns(self):
		""" Number of patterns found """
		return self._num_patterns

	@num_patterns.setter
	def num_patterns(self, value):
		""" Prepare place to this number of patterns
		Always has to be set before working with the other properties
		"""
		if value > self._num_patterns:
			self._matrix.extend([[None] * self.NUM_FIELDS for \
				i in range(value - self._num_patterns)])
		self._num_patterns = value
		self._pattern_num = value - 1

	@property
	def pattern_num(self):
		""" The number (index) of the pattern we are dealing with
		Must be between 0 and patterns_num
		"""
		return self._pattern_num

	@pattern_num.setter
	def pattern_num(self,value):
		""" Setting this value has the same effect as iterating through this
		RepeatPattern object.
		"""
		if value < 0 or value >= self._num_patterns:
			raise IndexError("Pattern number out of range")
		self._pattern_num = value

	# These properties hide the fact we are working with multiple patterns
	# From the sub classes

	@property
	def pattern(self):
		""" The Pattern """
		if not self._matrix:
			return None
		return self._matrix[self._pattern_num][self.PATTERN]

	@pattern.setter
	def pattern(self, value):
		self._matrix[self._pattern_num][self.PATTERN] = value

	@property
	def indices_lst(self):
		""" The places the pattern occur in the input list """
		if not self._matrix:
			return None
		return self._matrix[self._pattern_num][self.INDICES]

	@indices_lst.setter
	def indices_lst(self, value):
		self._matrix[self._pattern_num][self.INDICES] = value

	@property
	def factor(self):
		""" The factor of this pattern """
		if not self._matrix:
			return None
		return self._matrix[self._pattern_num][self.FACTOR]

	@factor.setter
	def factor(self, value):
		self._matrix[self._pattern_num][self.FACTOR] = value

	@property
	def repeats(self):
		""" The number of occurrences of this pattern in the input list """
		if not self._matrix:
			return None
		return len(self._matrix[self._pattern_num][self.INDICES])

	@repeats.setter
	def repeats(self, value):
		""" Ignore it - we will take repeats from len(indices) """
		pass

	############################################################################

	## Public Methods ##

	def process(self, input_lst):
		""" Find the best patterns in a list of items.
		Returns the number of patterns found.

		A derived class MUST implement this method.
		"""
		raise NotImplementedError("You have to implement this method")

	def process_by_pattern(self, input_lst):
		""" Find the indices list in a "lazy" mode from a pattern we already
		found. This method will not be relevant in most cases. It can be used to
		process multiple pages from the same website, and will work also if the
		indices list is shorter than "min_repeat".

		The method do a brute-force search on the input-list. Remember that
		there might be gaps between the pattern items.
		Return the number of patterns found.
		"""
		n = len(input_lst)
		d = len(self.pattern)
		pattern_set = set(self.pattern)				# For quick search
		self.indices_lst = []
		self.repeats = 0
		i = j = 0		# i - input list index, j - pattern index
		while i < n:
			if input_lst[i] == self.pattern[j]:		# One item match
				if j == 0: 							# This is the first item
					start = i
				j += 1
			elif input_lst[i] in pattern_set:		# Need to start over
				if input_lst[i] == self.pattern[0]:
					start = i
					j = 1
				else:
					j = 0
			i += 1
			if j == d:		# Found one
				self.indices_lst.append((start, i-1))
				self.repeats += 1
				j = 0
		return self.repeats

	def get_factor(self, pattern, indices):
		""" Calculate a factor for a repetitive pattern.
		pattern - a list of items.
		indices - The occurences of this pattern, a list of (start, end) indices.

		"stdv" is a normalized standard deviation of the distances between the
		indices of the pattern.

		Return 0 if the pattern should not be considered
		"""
		repeats = len(indices)
		#print ">>>", pattern, repeats
		if repeats < self.min_repeat: return 0
		if self.max_repeat and repeats > self.max_repeat: return 0
		if len(pattern) < self.min_len: return 0
		if self.max_len and len(pattern) > self.max_len: return 0
		stdv = self._nstdv(self._derivative([index[0] for index in indices]))
		if stdv > self.max_stdv: return 0
		if not self.LEN_ONE_MAGIC is None and \
		 len(pattern) == 1 and stdv > self.LEN_ONE_MAGIC:
			return 0
		weight = self._weight(indices)
		#print ">>> >>>", stdv, weight
		return (1 - stdv) * weight * repeats * len(pattern)

	def sort(self, sort_by=FACTOR):
		""" Sort the result pattern by a specific field (and rule) """
		if sort_by == self.PATTERN:
			key = lambda x: len(x[sort_by])
			reverse = True
		elif sort_by == self.INDICES:
			key = lambda x: x[sort_by][0]
			reverse = False
		elif sort_by == self.FACTOR:
			key = lambda x: x[sort_by]
			reverse = True
		elif sort_by == self.REPEATS:
			key = lambda x: len(x[self.INDICES])
			reverse = True
		else:
			raise TypeError(
				"sort_by must be one of RepeatPatternBase fields constants")
		self._matrix.sort(key=key, reverse=reverse)

	def clean_indices(self, indices):
		""" Remove indices that are included in other indices in the matrix
		(from all patterns from all indices).
		Change the 'indices' list in place!
		Returns the length of the modified indices list.
		"""
		def _overlap(index1, index2):
			return index1[0] >= index2[0] and index1[0] <= index2[1] or \
				index1[1] >= index2[0] and index1[1] <= index2[1]
		removables = []
		for i, index in enumerate(indices):
			for x in self:
				if any((_overlap(index, ind) for ind in self.indices_lst)):
					removables.append(i)
					break
		for i in reversed(removables):
			del indices[i]
		return len(indices)

	def break_indices_lst(self, indices):
		"""
		Break a list of indices to a list of lists of indices, so all indices
		lists will be within the STDV limit. All the lists will also be within
		the length limit. It ignores the LEN_ONE_MAGIC rule.
		This is a recursive method.
		Returns a list of indices lists.
		"""
		if len(indices) < self.min_repeat: return []	# First base case
		der_lst = self._derivative([start for start, _ in indices])
		stdv = self._nstdv(der_lst)
		if stdv < self.max_stdv:	# I ignore LEN_ONE_MAGIC
			return [indices]		# Second base case
		max_gap = max(der_lst)
		for index, val in enumerate(der_lst):
			if max_gap == val:
				return self.break_indices_lst(indices[:index+1]) + \
					self.break_indices_lst(indices[index+1:])

	############################################################################

	## The two following methods initialize an object from another object ##

	def get_pattern(self):
		""" """
		return self.output_lst

	def set_pattern(self, lst):
		""" """
		self.output_lst = lst

