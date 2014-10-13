__author__ = 'hemant_singh'


import unittest
from problem import *


class ProblemTestCase(unittest.TestCase):
    """Tests for `problem.py`"""

    def setUp(self):
        self.seq = list(range(10))

    def test_load_sample_data_from_csv(self):

        """is able to load data from sample file in list format"""
        data = load_data('sample.csv')
        self.assertEqual(type(data), list)

        if len(data) > 0:
            self.assertEqual(type(data[0]), list)


    def test_validate_data(self):

        presenters = [['rohit', '2', '100'], ['rajeev', '3', '50'], ['sanjeev', '4', '200'], ['saksham', '5', '300'],
                        ['hemant', '1', '200']]
        validated_list = validate_data(presenters, 8)

        # as 5 > 8/2 so it should not be in list
        self.assertFalse(['saksham', '5', '300'] in validated_list)


    def test_validate_data_length(self):
        presenters = [['rohit', '2', '100'], ['rajeev', '3', '50']]
        validated_list = validate_data(presenters, 8)

        # there must be atleast 3 items in the list
        self.assertTrue(validated_list is None)



    def test_subset_sum(self):
        """test if max no of presenters are selected"""

        presenters = [['rohit', '2', '100'], ['rajeev', '3', '50'], ['sanjeev', '4', '200'], ['saksham', '5', '300'],
                        ['hemant', '1', '200']]
        selected_list = subset_sum(presenters,8)

        self.assertEqual(selected_list, [[['rohit', '2', '100'], ['rajeev', '3', '50'], ['hemant', '1', '200']],
                                       [['rohit', '2', '100'], ['sanjeev', '4', '200'], ['hemant', '1', '200']],
                                       [['rohit', '2', '100'], ['saksham', '5', '300'], ['hemant', '1', '200']],
                                       [['rajeev', '3', '50'], ['sanjeev', '4', '200'], ['hemant', '1', '200']]])

    def test_select_less_expensive(self):
        """test if lest expensive presenter is selected"""

        presenters_list = [[['rohit', '2', '100'], ['rajeev', '3', '50'], ['hemant', '1', '200']],
                                       [['rohit', '2', '100'], ['sanjeev', '4', '200'], ['hemant', '1', '200']],
                                       [['rohit', '2', '100'], ['saksham', '5', '300'], ['hemant', '1', '200']],
                                       [['rajeev', '3', '50'], ['sanjeev', '4', '200'], ['hemant', '1', '200']]]
        selected_list = select_less_expensive(presenters_list)
        self.assertEqual(selected_list, [['rohit', '2', '100'], ['rajeev', '3', '50'], ['hemant', '1', '200']])

    def test_split_chunks(self):
        """test if they are diveded into sessions"""

        sessions = split_chunks([['rohit', '2', '100'], ['rajeev', '3', '50'], ['hemant', '1', '200']], 3)
        self.assertEqual(sessions, [[['rohit', '2', '100']], [['rajeev', '3', '50']], [['hemant', '1', '200']]])




if __name__ == '__main__':
    unittest.main()
