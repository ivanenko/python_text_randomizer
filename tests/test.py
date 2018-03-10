import unittest
import math
from text_randomizer.text_randomizer import TextRandomizer


class TestRandomizer(unittest.TestCase):

    def test_variants(self):
        text_rnd = TextRandomizer('{1|2|3}')
        self.assertEqual(text_rnd.variants_number(), 3)

        text_rnd = TextRandomizer('[1|2|3|4]')
        self.assertEqual(text_rnd.variants_number(), math.factorial(4))

        text_rnd = TextRandomizer('{1|{2|3}}')
        self.assertEqual(text_rnd.variants_number(), 3)

    def test_functions(self):
        text_rnd = TextRandomizer('start $MY_FUNC end', parse=False)
        text_rnd.add_function('MY_FUNC_22', lambda: 'test_string')
        text_rnd.parse()
        self.assertEquals(text_rnd.get_text(), 'start $MY_FUNC end')

        text_rnd.add_function('MY_FUNC', lambda: 'test_string')
        text_rnd.reset()
        text_rnd.parse()
        self.assertEquals(text_rnd.get_text(), 'start test_string end')

        #text_rnd.add_function('AAA', {'callable': lambda x, y: randint(x,y), 'coerce': int})

if __name__ == '__main__':
    unittest.main()