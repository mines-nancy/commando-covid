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
    e-mail: Pierre-Etienne.Moreau@univ-lorraine.fr
"""

import unittest
from models.components.box_convolution import BoxConvolution


class TestBoxFixedDelay(unittest.TestCase):

    def test_box_convolution1(self):
        for box in [BoxConvolution('CONV-1', [1]), BoxConvolution('CONV-1', [1], True)]:
            box.add(10)
            self.assertEqual(box.input(), 10)
            self.assertEqual(box.size(), 0)
            self.assertEqual(box.output(), 0)
            box.step()
            self.assertEqual(box.input(), 0)
            self.assertEqual(box.size(), 0)
            self.assertEqual(box.output(), 10)

            box.step()
            self.assertEqual(box.input(2), 10)
            self.assertEqual(box.size(2), 0)
            self.assertEqual(box.output(2), 0)

            self.assertEqual(box.input(1), 0)
            self.assertEqual(box.size(1), 0)
            self.assertEqual(box.output(1), 10)

            self.assertEqual(box.input(), 0)
            self.assertEqual(box.size(), 0)
            self.assertEqual(box.output(), 10)  # nothing has been removed

    def test_box_convolution2(self):
        box = BoxConvolution('CONV-2', [0.4, 0.6])
        box.add(10)
        box.step()
        self.assertEqual(box.input(), 0)
        self.assertEqual(box.size(), 0.6 * 10)
        self.assertEqual(box.output(), 0.4 * 10)
        box.remove(0.4*10)
        box.add(20)
        box.step()
        self.assertEqual(box.input(), 0)
        self.assertEqual(box.size(), (0.6*10) + 20 - (0.6*10) - (0.4*20))
        self.assertEqual(box.output(), 0.6 * 10 + 0.4 * 20)

    def test_box_int_convolution2(self):
        box = BoxConvolution('CONV-2', [0.4, 0.6], True)
        box.add(10)
        box.step()
        self.assertEqual(box.input(), 0)
        self.assertEqual(box.size(), int(0.6 * 10))
        self.assertEqual(box.output(), int(0.4 * 10))
        box.remove(int(0.4*10))
        box.add(20)
        box.step()
        self.assertEqual(box.input(), 0)
        self.assertEqual(box.size(), int(0.6*10) +
                         20 - int(0.6*10) - int(0.4*20))
        self.assertEqual(box.output(), int(0.6 * 10) + int(0.4 * 20))

    def check_input_output(self, box, inputs, r, outputs):
        for i in range(len(inputs)):
            box.add(inputs[i])
            self.assertEqual(box.input(), inputs[i])
            box.step()
            self.assertEqual(box.size(), r[i])
            self.assertEqual(box.output(), outputs[i])
            box.remove(box.output())

    def test_box_convolution_delay1(self):
        for box in [BoxConvolution('CONV-1', [1]), BoxConvolution('CONV-1', [1], True)]:
            inputs = [1, 2, 4, 8, 10, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
            r = [0 for x in inputs]
            outputs = [1, 2, 4, 8, 10, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
            self.check_input_output(box, inputs, r, outputs)

    def test_box_convolution_delay2(self):
        for box in [BoxConvolution('CONV-1', [0, 1]), BoxConvolution('CONV-1', [0, 1], True)]:
            inputs = [1, 2, 4, 8, 10, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
            r = [1, 2, 4, 8, 10, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
            outputs = [0, 1, 2, 4, 8, 10, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
            self.check_input_output(box, inputs, r, outputs)

    def test_box_convolution_delay10(self):
        for box in [BoxConvolution('CONV-10', 9*[0]+[1]), BoxConvolution('CONV-10', 9*[0]+[1], True)]:
            inputs = [1, 2, 4, 8, 10, 12, 10, 9, 8, 7,
                      6, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            r = [1, 3, 7, 15, 25, 37, 47, 56, 64, 70, 74,
                 75, 71, 64, 54, 45, 36, 28, 21, 15, 10, 6, 3, 1, 0, 0]
            outputs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 4,
                       8, 10, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
            self.check_input_output(box, inputs, r, outputs)

    def test_box_force_output10(self):
        for box in [BoxConvolution('CONV-10', 9*[0]+[1]), BoxConvolution('CONV-10', 9*[0]+[1], True)]:
            inputs = [1, 2, 4, 8, 10, 12, 10, 9, 8, 7,
                      6, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            r = [1, 3, 7, 15, 25, 37, 47, 56, 64, 70, 74,
                 75, 71, 64, 54, 45, 36, 28, 21, 15, 10, 6, 3, 1, 0, 0]

            for i in range(4):
                box.add(inputs[i])
                box.step()
                box.remove(box.output())
            self.assertAlmostEqual(box.size(), r[3])
            self.assertAlmostEqual(box.output(), 0)

            box.force_output(10)
            self.assertAlmostEqual(box.size(), 15-10)

            box.force_output(10)
            self.assertAlmostEqual(box.size(), 0)

    def test_box_queue_increase_duration(self):
        box = BoxConvolution('DELAY', [0, 0, 0, 0, 1])
        inputs = [5]*5+[0]*5
        r = [5, 10, 15, 20, 20, 15, 10, 5, 0, 0]
        outputs = [0, 0, 0, 0, 5, 5, 5, 5, 5, 0]
        self.check_input_output(box, inputs, r, outputs)

        inputs = [5]*5+[0]*5
        r = [5, 10, 15, 20, 25, 25, 20, 15, 10, 5]
        outputs = [0, 0, 0, 0, 0, 0, 5, 5, 5, 5]
        for i in range(len(inputs)):
            if i == 3:
                box.set_output_coefficients([0, 0, 0, 0, 0, 0, 1])
            box.add(inputs[i])
            self.assertEqual(box.input(), inputs[i])
            box.step()
            self.assertEqual(box.size(), r[i])
            self.assertEqual(box.output(), outputs[i])
            box.remove(box.output())

    def test_box_queue_decrease_duration(self):
        box = BoxConvolution('DELAY', [0, 0, 0, 0, 1])
        inputs = [5]*5+[0]*5
        r = [5, 10, 15, 20, 20, 15, 10, 5, 0, 0]
        outputs = [0, 0, 0, 0, 5, 5, 5, 5, 5, 0]
        self.check_input_output(box, inputs, r, outputs)

        inputs = [5]*5+[0]*5
        r = [5, 10, 10, 10, 10, 5, 0, 0, 0, 0]
        outputs = [0, 0, 5, 5, 5, 5, 5, 0, 0, 0]
        for i in range(len(inputs)):
            if i == 2:
                box.set_output_coefficients([0, 0, 1])
            box.add(inputs[i])
            self.assertEqual(box.input(), inputs[i])
            box.step()
            self.assertEqual(box.size(), r[i])
            self.assertEqual(box.output(), outputs[i])
            box.remove(box.output())


if __name__ == '__main__':
    unittest.main()
