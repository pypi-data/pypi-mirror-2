#!python
#
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
This is a data module that define a dictionary that carry the different
RepeatPattern algorithms meta data. The keys of this dictionary are the
implementation classes of the algorithms. The values are named tuple that is
defined below.

Run as a script to see the algorithms data.
"""

# NOTE: Python 2.6 Only
from collections import namedtuple

AlgoData = namedtuple("AlgoData", ["name", "desc", "order", "min_quality", "enabled"])

from repeat_pattern import RepeatPattern
from repeat_pattern2 import RepeatPattern as RepeatPatternTree
from repeat_pattern_suffix import RepeatPattern as RepeatPatternArray
from repeat_title import RepeatPattern as RepeatTitle

algo_dict = {
	RepeatPattern: AlgoData(
		name = "Count Tags",
		desc = "Counts the tags in (sub sections of) the HTML page and groups them to sequences. Than it tries to expand the best groups.",
		order = 1,
		min_quality = 0.7,
		enabled = True
	),
	RepeatTitle: AlgoData(
		name = "Titles",
		desc = "Not much of an algorithm, simply look for Hx tags",
		order = 4,
		min_quality = 0,
		enabled = True
	),
	RepeatPatternArray: AlgoData(
		name = "Tags Pattern",
		desc = "Finds repetitive patterns using suffix array",
		order = 3,
		min_quality = 0.8,
		enabled = True
	),
	RepeatPatternTree: AlgoData(
		name = "Tags Pattern",
		desc = "Finds repetitive patterns using suffix tree",
		order = 2,
		min_quality = 0.8,
		enabled = False
	),
}

if __name__ == '__main__':
	key_val = algo_dict.items()
	key_val.sort(key=lambda x: x[1].order)
	for cls, data in key_val:
		print "Name:", data.name
		print "Descriptiopn:", data.desc
		print "Enabled:", data.enabled
		print "Class:", cls
		print "----------------------------------"

