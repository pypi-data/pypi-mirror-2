from django.test import TestCase
from stdnet import orm


class jFlowTest(TestCase):
    
    def tearDown(self):
        orm.clearall()