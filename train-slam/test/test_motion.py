import numpy
from unittest import TestCase

from train_slam.motion import transform_acceleration

class TestParticle(TestCase):

    def test_train_inline(self):
        "should not update heading when no velocity"
        a_train = [1, 0]
        a_global = transform_acceleration(a_train, 0)
        self.assertListEqual(a_train, list(a_global))

    def test_train_right_angle(self):
        "should swap heading to y when heading right"
        a_train = [1, 0]
        a_global = transform_acceleration(a_train, numpy.pi/2)
        self.assertAlmostEqual(float(a_global[0]), 0)
        self.assertAlmostEqual(float(a_global[1]), 1)

    def test_train_heading_down(self):
        "should move acceleration to negative from down direction"
        a_train = [1, 0]
        a_global = transform_acceleration(a_train, numpy.pi)
        self.assertAlmostEqual(float(a_global[0]), -1)
        self.assertAlmostEqual(float(a_global[1]), 0)
