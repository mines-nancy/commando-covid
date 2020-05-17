# -*- coding: utf-8 -*-
"""
    This file is part of MODSIR19.

    MODSIR19 is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MODSIR19 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with MODSIR19.  If not, see <https://www.gnu.org/licenses/>.

    Copyright (c) 2020 Pierre-Etienne Moreau
    e-mail: Pierre-Etienne.Moreau@loria.fr
"""

import unittest
from models.components.box import Box, BoxSource, BoxTarget


class TestBox(unittest.TestCase):

    def test_box1(self):
        box = Box('BOX')
        self.assertEqual(box.input(), 0)
        self.assertEqual(box.size(), 0)
        self.assertEqual(box.output(), 0)
        box.add(1)
        box.remove(2)
        self.assertEqual(box.input(), 1)
        self.assertEqual(box.size(), 0)
        self.assertEqual(box.output(), -2)

        box.step()
        self.assertEqual(box.input(), 0)
        self.assertEqual(box.size(), 0)
        self.assertEqual(box.output(), 0)

        self.assertEqual(box.input(0), 0)
        self.assertEqual(box.size(0), 0)
        self.assertEqual(box.output(0), 0)

        self.assertEqual(box.input(1), 1)
        self.assertEqual(box.size(1), 0)
        self.assertEqual(box.output(1), -2)

    def test_box2(self):
        box = Box('BOX')
        for i in range(10):
            box.add(i)
            box.remove(i)
            box.step()

        for i in range(10):
            n = (9-i)
            self.assertEqual(box.input(1+i), n)
            self.assertEqual(box.size(1+i), 0)
            self.assertEqual(box.output(1+i), -n)

    def test_box_source(self):
        box = BoxSource('SOURCE')
        self.assertEqual(box.input(), 0)
        self.assertEqual(box.size(), 0)
        self.assertEqual(box.output(), 0)

        box.add(100)
        self.assertEqual(box.input(), 100)
        self.assertEqual(box.size(), 0)
        self.assertEqual(box.output(), 0)

        box.step()
        self.assertEqual(box.input(), 0)
        self.assertEqual(box.size(), 100)
        self.assertEqual(box.output(), 100)

        box.step()
        self.assertEqual(box.input(), 0)
        self.assertEqual(box.size(), 100)
        self.assertEqual(box.output(), 100)

        box.add(10)
        box.step()
        self.assertEqual(box.input(), 0)
        self.assertEqual(box.size(), 110)
        self.assertEqual(box.output(), 110)

        box.remove(10)
        box.step()
        self.assertEqual(box.input(), 0)
        self.assertEqual(box.size(), 100)
        self.assertEqual(box.output(), 100)


if __name__ == '__main__':
    unittest.main()
