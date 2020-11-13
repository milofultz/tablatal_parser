from textwrap import dedent
import unittest

import add_field
import utilities


class TestAddFieldFunctions(unittest.TestCase):

    def test_get_tablatal_data(self):
        test_filepath = "test.tbtl"
        self.assertEqual(utilities.load_data(test_filepath), "TEST DATA")

    def test_find_header_in_data(self):
        test_data_1 = dedent(
            """\
            ; The horaire is a collection of logs.
            ; https://wiki.xxiivv.com/site/tablatal.html
            ;     CODE HOST                 PIC NAME
            ;     7    12                   33  37
            20X09 +300 talk                     Talk at Speakers Series, SNSYC
            20X07 +300 talk                     Grundlagen der digitalen Kommunikation
            20V08 -332 orca
            """
        )
        self.assertEqual(add_field.find_header_line(test_data_1),
                         ';     CODE HOST                 PIC NAME')
        test_data_2 = dedent(
            """\
            ; Evi Database
            ;
            DATE   TIME   CAT PROJECT            SESSION                  SUMMARY
            201103 00:51  Cod Track v2           Finish MVP               Added input validation and basic CLI use. MVP achieved
            201103 00:17  Cod Track v2           Add database print       Added basic print
            201103 00:04  Ref Machado Podcasts   Send episode             I think I'm going to keep it in house
            201103 00:03  Cod Git Course         Section 3                Too simple, nothing to learn
            201103 00:42  Cod Git Course         Self Study               Learned some git, but I think it's still too early for me to worry about it
            """
        )
        self.assertEqual(add_field.find_header_line(test_data_2),
                         'DATE   TIME   CAT PROJECT            SESSION                  SUMMARY')

    def test_get_header_info_from_line(self):
        test_header_1 = "TEST DATA"
        self.assertEqual(utilities.get_headers_info_from_line(test_header_1),
                         [{'name': 'TEST', 'start': 0, 'length': 5},
                          {'name': 'DATA', 'start': 5, 'length': None}])
        test_header_2 = "DATE   TIME   CAT PROJECT            SESSION                  SUMMARY"
        self.assertEqual(utilities.get_headers_info_from_line(test_header_2),
                         [{'name': 'DATE', 'start': 0, 'length': 7},
                          {'name': 'TIME', 'start': 7, 'length': 7},
                          {'name': 'CAT', 'start': 14, 'length': 4},
                          {'name': 'PROJECT', 'start': 18, 'length': 19},
                          {'name': 'SESSION', 'start': 37, 'length': 25},
                          {'name': 'SUMMARY', 'start': 62, 'length': None}])

    def test_get_last_field_length(self):
        test_data_1 = dedent(
            """\
            ; Evi Database
            ;
            DATE   TIME   CAT PROJECT            SESSION                  SUMMARY
            201103 00:51  Cod Track v2           Finish MVP               Added input validation and basic CLI use. MVP achieved
            201103 00:17  Cod Track v2           Add database print       Added basic print
            201103 00:04  Ref Machado Podcasts   Send episode             I think I'm going to keep it in house
            201103 00:03  Cod Git Course         Section 3                Too simple, nothing to learn
            201103 00:42  Cod Git Course         Self Study               Learned some git, but I think it's still too early for me to worry about it
            """
        )
        test_header_info_1 = [{'name': 'DATE', 'start': 0, 'length': 7},
                              {'name': 'TIME', 'start': 7, 'length': 7},
                              {'name': 'CAT', 'start': 14, 'length': 4},
                              {'name': 'PROJECT', 'start': 18, 'length': 19},
                              {'name': 'SESSION', 'start': 37, 'length': 25},
                              {'name': 'SUMMARY', 'start': 62, 'length': None}]
        self.assertEqual(
            add_field.get_last_field_length(test_data_1, test_header_info_1), 75)

    def test_add_new_field_to_header_info(self):
        test_new_field_1 = {'name': 'NEW', 'length': 10, 'index': 1}
        test_header_info_1 = [{'name': 'TEST', 'start': 0, 'length': 5},
                              {'name': 'DATA', 'start': 5, 'length': 5}]
        self.assertEqual(
            add_field.add_new_field_to_headers_info(test_new_field_1,
                                                    test_header_info_1),
            [{'name': 'TEST', 'start': 0, 'length': 5},
             {'name': 'NEW', 'start': 5, 'length': 10},
             {'name': 'DATA', 'start': 15, 'length': 5}]
        )



if __name__ == '__main__':
    unittest.main()
