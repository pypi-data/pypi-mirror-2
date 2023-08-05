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
A trivial algorithem to find HTML titles. Some time that is what we need.
I inherit from the module repeat_pattern and not from the base, because there
are common methods here.
"""

from collections import defaultdict

from repeat_pattern import RepeatPattern as RepeatPatternBase

# Multiply the factor by this value, because titles factors are very low.
FACTOR_ADJUST = 5

TITLES = set(("h1", "h2", "h3", "h4", "h5", "h6"))

class RepeatPattern(RepeatPatternBase):
	"""
	See module documentation
	"""

	def _find_titles(self):
		""" Here I do most of the work.
		1. Find the titles
		2. Get the indices and factors
		3. Break the indices to groups
		4. Populate with the best X titles type
		- There is no need to use "clean_indices" here
		I have to "cheat" with the indices list and the pattern so the factor
		will not be zero. The factor will be low anyway, I adjust it in the
		get_factor method.
		"""
		lst = []
		# Find all titles
		for title, indices in self._items_dict.iteritems():
			if not title.tag_name() in TITLES: continue
			if self.debug_level > 3:
				print "Found", title
			# "Fix" indices list and pattern
			indices_lst = self.break_indices_lst(zip(indices, indices))
			pattern = [title]
			for indices in indices_lst:
				if self.debug_level > 4:
					print "Indices", indices
				factor = self.get_factor(pattern, indices)
				if factor > 0:
					lst.append((pattern, indices, factor))
		if not lst: return 0		# We didn't find a pattern
		if self.debug_level > 2:
			print "Titles", lst
		# Sort the titles by the factor
		lst.sort(key = lambda x: x[2], reverse = True)
		# Extract the best title types
		self.num_patterns = 0
		index = 0
		while self.num_patterns < self.max_patterns and index < len(lst):
			self.num_patterns += 1	# Also sets the new pattern as "active"
			self.pattern, self.indices_lst, self.factor = lst[index]
			if self.debug_level > 0:
				self._print_pattern("Best %s" % self.num_patterns)
			index += 1
		self.pattern_num = 0

	def get_factor(self, pattern, indices):
		""" Adjustment to the factor which will be low for this class. """
		return FACTOR_ADJUST * \
			RepeatPatternBase.get_factor(self, pattern, indices)

	def process(self, input_lst):
		""" Find the titles """
		self.init(input_lst)
		self.LEN_ONE_MAGIC = None	# Cannot use it here, all length=1
		self._items_dict = defaultdict(list)	# Dictionary of item: indices
		# Here I'm doing the work
		self._group_items()
		self._find_titles()
		return self.num_patterns

if __name__ == '__main__':
	# TODO: test this module
	pass
