from website_parse import *
import unittest


class TestTree(unittest.TestCase):
    # Start simple
    def test_trees(self):
        tree = build_tree("( sam OR jeff ) OR harry")
        evaluate_tree(tree, "jeff")
        self.assertEqual(tree.get_root_value(), True)
        tree = build_tree('NOT ( ( ( frank AND joe ) OR mary ) AND jerry )')
        evaluate_tree(tree, 'jerry mary')
        self.assertEqual(tree.get_root_value(), True)
        tree = build_tree('( NOT ( ( frank AND joe ) OR mary ) AND jerry )')
        evaluate_tree(tree, 'jerry mary')
        self.assertEqual(tree.get_root_value(), True)
        tree = build_tree('( NOT ( NOT ( frank AND joe ) OR mary ) AND jerry )')
        evaluate_tree(tree, 'jerry mary')
        self.assertEqual(tree.get_root_value(), True)
        tree = build_tree('( NOT ( NOT ( frank AND joe ) OR mary ) AND NOT jerry )')
        evaluate_tree(tree, 'jerry mary ')
        self.assertEqual(tree.get_root_value(), True)
        tree = build_tree('( nation AND social ) AND NOT amazon')
        evaluate_tree(tree, 'nation social')
        self.assertEqual(tree.get_root_value(), True)

    def test_query(self):
        self.assertEqual(query('nation AND social AND NOT amazon', 'https://www.influenster.com'), True)
        self.assertEqual(query('entertainment OR nation', 'https://www.influenster.com/reviews'), True)
        self.assertEqual(query('entertainment AND NOT supplies', 'https://www.influenster.com/reviews/pets'), False)
        self.assertEqual(query('NOT horse AND supplies', 'https://www.influenster.com/reviews/pets'), True)

    def test_exceptions(self):
        # uppercase check
        self.assertRaises(SyntaxError, check_format, 'not horse', "http://somewebsite.com")
        self.assertRaises(SyntaxError, check_format, 'NOT book and cat', "http://somewebsite.com")
        # parenthesis are spaced
        self.assertRaises(SyntaxError, check_format, '( NOT horse)', "http://somewebsite.com")
        # Make sure compound statements have parenthesis
        self.assertRaises(SyntaxError, check_format, 'NOT horse AND FACE OR home', "http://somewebsite.com")
        self.assertRaises(SyntaxError, check_format, 'NOT horse AND FACE OR home', "http://somewebsite.com")
        self.assertRaises(SyntaxError, check_format, "horse", "htp://somewebsite.com")

if __name__ == "__main__":
    unittest.main()
