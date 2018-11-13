import numpy
from unittest import TestCase

from train_slam.particle import create_particle, move_particle, calculate_average_particle

class TestParticle(TestCase):

    def test_move_particle_zero_velocity(self):
        "should not update heading when no velocity"
        p1 = create_particle(1, 0, 0, 1, 0)
        p2 = move_particle(p1, 0, 1, 1)
        self.assertEqual(p1.h, p2.h)

    def test_move_particle_large_velocity(self):
        "should update heading with new velocity"
        p1 = create_particle([0,0], [10, 0], [0, 0], 1, 0)
        p2 = move_particle(p1, numpy.array([0, 0]), 1, 1)
        self.assertListEqual(list(p2.s), [10, 0])
        self.assertListEqual(list(p2.v), [10, 0])
        self.assertListEqual(list(p2.a), [0, 0])
        self.assertEqual(p2.h, numpy.pi/2)


    def test_calculate_average_particle(self):
        p1 = create_particle([0,1], [10, 0], [0, 0], 1, 0.5)
        p2 = create_particle([0,2], [8, 0], [0, 0], 3, 0.5)
        p = calculate_average_particle([p1, p2])
        self.assertListEqual(list(p.s), [0, 1.5])
        self.assertListEqual(list(p.v), [9, 0])
        self.assertListEqual(list(p.a), [0, 0])
        self.assertEqual(p.h, 2)
        self.assertEqual(p.w, 1)