##    shitjs - a shit javascript interpreter
##    Copyright (C) 2009, 2010, 2011 Rene Dudfield
##
##    This library is free software; you can redistribute it and/or
##    modify it under the terms of the GNU Library General Public
##    License as published by the Free Software Foundation; either
##    version 2 of the License, or (at your option) any later version.
##
##    This library is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##    Library General Public License for more details.
##
##    You should have received a copy of the GNU Library General Public
##    License along with this library; if not, write to the Free
##    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##
##    Rene Dudfield
##    renesd@gmail.com


import unittest

try:
    import part1
except:
    from shitjs import part1

class TestPart2(unittest.TestCase):
    def test_evaluate(self):

        c = JsContext()
        self.assertEqual(c.evaluate("1 + 2"), 3.0)
        self.assertEqual(c.evaluate("1 * 2"), 2.0)
        self.assertEqual(c.evaluate("1 + 2 * 4"), 9.0)

        

if __name__ == '__main__':
    unittest.main()

