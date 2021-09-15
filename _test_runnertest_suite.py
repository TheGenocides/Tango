import unittest
from main import *


class UnitTests(unittest.TestCase):

  def test_e(self):
      self.assertEquals(add(1, 2), 3)

