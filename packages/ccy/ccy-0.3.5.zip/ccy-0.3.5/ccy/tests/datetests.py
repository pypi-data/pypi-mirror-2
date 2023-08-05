from unittest import TestCase

from ccy import period


class PeriodTests(TestCase):
    
    def testPeriod(self):
        a = period('5Y')
        self.assertEqual(a.years,5)
        b = period('1y3m')
        self.assertEqual(b.years,1)
        self.assertEqual(b.months,3)
        c = period('-3m')
        self.assertEqual(c.years,0)
        self.assertEqual(c.months,-3)
        
    def testAdd(self):
        a = period('4Y')
        b = period('1Y3M')
        c = a + b
        self.assertEqual(c.years,5)
        self.assertEqual(c.months,3)
        
    def testSubtract(self):
        a = period('4Y')
        b = period('1Y')
        c = a - b
        self.assertEqual(c.years,3)
        self.assertEqual(c.months,0)
        c = period('3Y') - period('1Y3M')
        self.assertEqual(c.years,1)
        self.assertEqual(c.months,9)
        self.assertEqual(str(c),'1Y9M')
        
    def testCompare(self):
        a = period('4Y')
        b = period('4Y')
        c = period('1Y2M')
        self.assertTrue(a==b)
        self.assertTrue(a>=b)
        self.assertTrue(a<=b)
        self.assertTrue(c<=a)
        self.assertTrue(c<a)
        self.assertFalse(c==a)
        self.assertFalse(c>=b)
        self.assertTrue(c>a-b)
    