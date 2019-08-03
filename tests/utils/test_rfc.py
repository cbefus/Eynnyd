import unittest
import re

from src.utils import rfc


class TestGeneral(unittest.TestCase):

    def test_control_chars_inclusive(self):
        expression = re.compile(r"["+rfc._CONTROL_CHARS+"]")
        control_character_ordinals = frozenset([127]+[x for x in range(0,32)])
        for control_character_ordinal in control_character_ordinals:
            value_to_test = chr(control_character_ordinal)
            self.assertTrue(
                bool(expression.fullmatch(value_to_test)),
                msg="Character for ord '{o}' was not included".format(o=control_character_ordinal))

    def test_control_chars_exclusive(self):
        expression = re.compile(r"[" + rfc._CONTROL_CHARS + "]")
        control_character_ordinals = frozenset([x for x in range(32, 127)])
        for control_character_ordinal in control_character_ordinals:
            value_to_test = chr(control_character_ordinal)
            self.assertFalse(
                bool(expression.fullmatch(value_to_test)),
                msg="Character for ord '{o}' was included".format(o=control_character_ordinal))

    def test_space_char(self):
        expression = re.compile(r"[" + rfc._SPACE_CHAR + "]")
        self.assertTrue(bool(expression.fullmatch(" ")), msg="Space was not found")

    def test_tab_char(self):
        expression = re.compile(r"[" + rfc._TAB_CHAR + "]")
        self.assertTrue(bool(expression.fullmatch("\t")), msg="Tab was not found")

    def test_separators_inclusive(self):
        expression = re.compile(r"[" + rfc._SEPARATOR_CHARS + "]")
        separators = ["(", ")", "<", ">", "@", ",", ";", ":", "\\", "\"", "/", "[", "]", "?", "=", "{", "}", " ", "\t"]
        for separator in separators:
            self.assertTrue(
                bool(expression.fullmatch(separator)),
                msg="Separator '{s}' was not found".format(s=separator))

    def test_token_inclsive(self):
        expression = re.compile(rfc._TOKEN_REGEX)
        valid_tokens = [
            "a",
            "abcd",
            "abraca+dab_ra-goes",
            "other_syms!#$%^&*_-+|'~`."
        ]
        for valid_token in valid_tokens:
            self.assertTrue(
                bool(expression.fullmatch(valid_token)),
                msg="Valid Token '{t}' was flagged".format(t=valid_token))

    def test_token_exclusive(self):
        expression = re.compile(rfc._TOKEN_REGEX)
        invalid_tokens = [chr(127)]+[chr(x) for x in range(0,32)]
        invalid_tokens += ["(", ")", "<", ">", "@", ",", ";", ":", "\\", "\"", "/", "[", "]", "?", "=", "{", "}", " ", "\t"]
        for invalid_token in invalid_tokens:
            self.assertFalse(
                bool(expression.fullmatch("abc"+invalid_token+"def")),
                msg="Invalid Token 'abc{t}def' was not flagged".format(t=invalid_token))


class TestDates(unittest.TestCase):

    def test_1_digit(self):
        expression = re.compile(rfc._1_DIGIT_REGEX)
        self.assertTrue(bool(expression.fullmatch("3")))
        self.assertFalse(bool(expression.fullmatch("34")))
        self.assertFalse(bool(expression.fullmatch("a")))
        self.assertFalse(bool(expression.fullmatch("8a")))

    def test_2_digit(self):
        expression = re.compile(rfc._2_DIGIT_REGEX)
        self.assertTrue(bool(expression.fullmatch("38")))
        self.assertFalse(bool(expression.fullmatch("4")))
        self.assertFalse(bool(expression.fullmatch("a")))
        self.assertFalse(bool(expression.fullmatch("48a")))

    def test_4_digit(self):
        expression = re.compile(rfc._4_DIGIT_REGEX)
        self.assertTrue(bool(expression.fullmatch("3878")))
        self.assertFalse(bool(expression.fullmatch("432")))
        self.assertFalse(bool(expression.fullmatch("43234")))
        self.assertFalse(bool(expression.fullmatch("a")))
        self.assertFalse(bool(expression.fullmatch("2348a")))

    def test_time_regex_inclusive(self):
        expression = re.compile(rfc._TIME_REGEX)
        self.assertTrue(bool(expression.fullmatch("12:22:06")))
        self.assertTrue(bool(expression.fullmatch("00:00:00")))

    def test_time_regex_exclusive(self):
        expression = re.compile(rfc._TIME_REGEX)
        bad_times = [
            "a",
            "one o' clock",
            "9:52",
            "9:52am",
            "6:34:27",
            "19:4:27",
            "19:34:7",
            "12:34:27pm"
        ]
        for bad_time in bad_times:
            self.assertFalse(
                bool(expression.fullmatch(bad_time)),
                msg="Bad Time '{t}' was not flagged".format(t=bad_time))

    def test_month_inclusive(self):
        expression = re.compile(rfc._MONTH_REGEX)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for month in months:
            self.assertTrue(
                bool(expression.fullmatch(month)),
                msg="Month '{m}' was not included in regex.".format(m=month))

    def test_month_exclusive(self):
        expression = re.compile(rfc._MONTH_REGEX)
        bad_months = [
            "January",
            "February",
            "March",
            "April",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
            "Abc",
            "Ja",
            ""
        ]
        for bad_month in bad_months:
            self.assertFalse(
                bool(expression.fullmatch(bad_month)),
                msg="Bad Month Encoding '{m}' was matched and shouldn't have been".format(m=bad_month))

    def test_weekday_inclusive(self):
        expression = re.compile(rfc._WEEKDAY_REGEX)
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for weekday in weekdays:
            self.assertTrue(
                bool(expression.fullmatch(weekday)),
                msg="Weekday '{w}' was not included in regex.".format(w=weekday))

    def test_weekday_exclusive(self):
        expression = re.compile(rfc._WEEKDAY_REGEX)
        bad_weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Abc", "Tu", ""]
        for bad_weekday in bad_weekdays:
            self.assertFalse(
                bool(expression.fullmatch(bad_weekday)),
                msg="Bad Weekday Encoding '{m}' was matched and shouldn't have been".format(m=bad_weekday))

    def test_wkday_inclusive(self):
        expression = re.compile(rfc._WKDAY_REGEX)
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for weekday in weekdays:
            self.assertTrue(
                bool(expression.fullmatch(weekday)),
                msg="Weekday '{w}' was not included in regex.".format(w=weekday))

    def test_wkday_exclusive(self):
        expression = re.compile(rfc._WKDAY_REGEX)
        bad_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Abc", "Tu", ""]
        for bad_weekday in bad_weekdays:
            self.assertFalse(
                bool(expression.fullmatch(bad_weekday)),
                msg="Bad Weekday Encoding '{m}' was matched and shouldn't have been".format(m=bad_weekday))

    def test_asctime_date_inclusive(self):
        expression = re.compile(rfc._ASCTIME_DATE_REGEX)
        good_dates = ["Jan 21", "Feb  3"]
        for good_date in good_dates:
            self.assertTrue(
                bool(expression.fullmatch(good_date)),
                msg="Good date format '{d}' didnt match regex".format(d=good_date))

    def test_asctime_date_exclusive(self):
        expression = re.compile(rfc._ASCTIME_DATE_REGEX)
        bad_dates = [
            "Feb 3",
            "January 3",
            "Feb 3 1997",
            "January 3 1997",
            "Something else",
            "07/23",
            "07/23/97",
            "23-Jan-98",
            "23-Jan-1998",
            "23-07-1998",
            "23-07-98",
            "31 Oct 1982"
        ]
        for bad_date in bad_dates:
            self.assertFalse(
                bool(expression.fullmatch(bad_date)),
                msg="Bad date '{d}' didn't match regex".format(d=bad_date))

    def test_rfc850_date_inclusive(self):
        expression = re.compile(rfc._RFC850_DATE_REGEX)
        good_dates = ["31-Oct-82", "01-Jan-23"]
        for good_date in good_dates:
            self.assertTrue(
                bool(expression.fullmatch(good_date)),
                msg="Good date format '{d}' didnt match regex".format(d=good_date))

    def test_rfc850_date_exclusive(self):
        expression = re.compile(rfc._RFC850_DATE_REGEX)
        bad_dates = [
            "Jan 21",
            "Feb  3",
            "Feb 3",
            "January 3",
            "Feb 3 1997",
            "January 3 1997",
            "Something else",
            "07/23",
            "07/23/97",
            "23-Jan-1998",
            "23-07-1998",
            "23-07-98",
            "31 Oct 1982"
        ]
        for bad_date in bad_dates:
            self.assertFalse(
                bool(expression.fullmatch(bad_date)),
                msg="Bad date '{d}' didn't match regex".format(d=bad_date))

    def test_rfc1123_date_inclusive(self):
        expression = re.compile(rfc._RFC1123_DATE_REGEX)
        good_dates = ["31 Oct 1982", "01 Jan 2023"]
        for good_date in good_dates:
            self.assertTrue(
                bool(expression.fullmatch(good_date)),
                msg="Good date format '{d}' didnt match regex".format(d=good_date))

    def test_rfc1123_date_exclusive(self):
        expression = re.compile(rfc._RFC1123_DATE_REGEX)
        bad_dates = [
            "Jan 21",
            "Feb  3",
            "Feb 3",
            "January 3",
            "Feb 3 1997",
            "January 3 1997",
            "Something else",
            "07/23",
            "07/23/97",
            "23-Jan-1998",
            "23-07-1998",
            "23-07-98",
            "31-Oct-82"
        ]
        for bad_date in bad_dates:
            self.assertFalse(
                bool(expression.fullmatch(bad_date)),
                msg="Bad date '{d}' didn't match regex".format(d=bad_date))

    def test_asc_datetime_inclusive(self):
        expression = re.compile(rfc._ASCTIME_DATETIME_REGEX)
        good_examples = [
            "Mon Jan  3 03:21:45 2045",
            "Thu Oct 31 20:34:22 1982"
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good asctime datetime '{d}' didn't match regex".format(d=good_example))

    def test_asc_datetime_exclusive(self):
        expression = re.compile(rfc._ASCTIME_DATETIME_REGEX)
        bad_examples = [
            "Mon, 31 Oct 1982 03:21:45 GMT",
            "Thu, 01 Feb 2045 20:34:22 GMT",
            "Monday, 31-Oct-82 03:21:45 GMT",
            "Thursday, 01-Feb-45 20:34:22 GMT",
            "Something else"
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad asctime datetime '{d}' matched regex".format(d=bad_example))

    def test_rfc850_datetime_inclusive(self):
        expression = re.compile(rfc._RFC850_DATETIME_REGEX)
        good_examples = [
            "Monday, 31-Oct-82 03:21:45 GMT",
            "Thursday, 01-Feb-45 20:34:22 GMT"
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good rfc850 datetime '{d}' didn't match regex".format(d=good_example))

    def test_rfc850_datetime_exclusive(self):
        expression = re.compile(rfc._RFC850_DATETIME_REGEX)
        bad_examples = [
            "Mon Jan  3 03:21:45 2045",
            "Thu Oct 31 20:34:22 1982",
            "Monday, 31-Oct-82 03:21:45",
            "Monday 31-Oct-82 03:21:45 GMT",
            "Mon, 31 Oct 1982 03:21:45 GMT",
            "Thu, 01 Feb 2045 20:34:22 GMT",
            "Something else"
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad rfc850 datetime '{d}' matched regex".format(d=bad_example))

    def test_rfc1123_datetime_inclusive(self):
        expression = re.compile(rfc._RFC1123_DATETIME_REGEX)
        good_examples = [
            "Mon, 31 Oct 1982 03:21:45 GMT",
            "Thu, 01 Feb 2045 20:34:22 GMT"
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good rfc1123 datetime '{d}' didn't match regex".format(d=good_example))

    def test_rfc1123_datetime_exclusive(self):
        expression = re.compile(rfc._RFC1123_DATETIME_REGEX)
        bad_examples = [
            "Mon Jan  3 03:21:45 2045",
            "Thu Oct 31 20:34:22 1982",
            "Mon 31 Oct 1982 03:21:45 GMT",
            "Thu, 01 Feb 2045 20:34:22",
            "Thu, 01 Feb  2045 20:34:22 GMT",
            "Monday, 31-Oct-82 03:21:45",
            "Monday 31-Oct-82 03:21:45 GMT",
            "Something else"
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad rfc850 datetime '{d}' matched regex".format(d=bad_example))

    def test_http_date_inclusive(self):
        expression = re.compile(rfc._HTTP_DATE_REGEX)
        good_dates = [
            "Mon Jan  3 03:21:45 2045",
            "Thu Oct 31 20:34:22 1982",
            "Monday, 31-Oct-82 03:21:45 GMT",
            "Thursday, 01-Feb-45 20:34:22 GMT",
            "Mon, 31 Oct 1982 03:21:45 GMT",
            "Thu, 01 Feb 2045 20:34:22 GMT"
        ]
        for good_date in good_dates:
            self.assertTrue(
                bool(expression.fullmatch(good_date)),
                msg="Good HTTP Date format '{d}' wasn't matched by regex".format(d=good_date))

    def test_http_date_exclusive(self):
        expression = re.compile(rfc._HTTP_DATE_REGEX)
        bad_dates = [
            "Something else",
            "Mon Jan 3 03:21:45 2045",
            "Mon, Jan  3 03:21:45 2045",
            "Mon Jan  3 03:1:45 2045",
            "Mon Jan  3 03:01:45 45",
            "Mon Jan  3 03:01:45 2045 GMT",
            "Thu Oct  31 20:34:22 1982",
            "Monday 31-Oct-82 03:21:45 GMT",
            "Monday, 31-Oct-82 03:21:45",
            "Monday, 31-Oct-1982 03:21:45 GMT",
            "Monday, 6-Oct-82 03:21:45 GMT",
            "Mon 31 Oct 1982 03:21:45 GMT",
            "Mon, 31 Oct 1982 03:21:45",
            "Mon, 31 Oct 82 03:21:45 GMT",
            "Mon, 6 Oct 1982 03:21:45 GMT"
        ]
        for bad_date in bad_dates:
            self.assertFalse(
                bool(expression.fullmatch(bad_date)),
                msg="Bad HTTP Date format '{d}' matched by regex".format(d=bad_date))


class TestDomains(unittest.TestCase):

    def test_letters_inclusive(self):
        expression = re.compile(rfc._LETTERS_REGEX)
        good_examples = [
            "a",
            "A"
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good letter '{l}' didnt match regex".format(l=good_example))

    def test_letters_exclusive(self):
        expression = re.compile(rfc._LETTERS_REGEX)
        bad_examples = [
            "7",
            "",
            "-",
            ";"
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad letter '{l}' matched regex".format(l=bad_example))

    def test_letters_digits_inclusive(self):
        expression = re.compile(rfc._LETTERS_DIGITS_REGEX)
        good_examples = [
            "a",
            "A",
            "7"
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good letter or digit '{l}' didnt match regex".format(l=good_example))

    def test_letters_digits_exclusive(self):
        expression = re.compile(rfc._LETTERS_DIGITS_REGEX)
        bad_examples = [
            "",
            "-",
            ";"
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad letter or digit '{l}' matched regex".format(l=bad_example))

    def test_letters_digits_hyphens_inclusive(self):
        expression = re.compile(rfc._LETTER_DIGITS_HYPHENS_REGEX)
        good_examples = [
            "a",
            "A",
            "7",
            "-"
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good letter or digit or hyphen '{l}' didnt match regex".format(l=good_example))

    def test_letters_digits_hyphens_exclusive(self):
        expression = re.compile(rfc._LETTER_DIGITS_HYPHENS_REGEX)
        bad_examples = [
            "",
            ";"
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad letter or digit or hyphen '{l}' matched regex".format(l=bad_example))

    def test_label_inclusive(self):
        expression = re.compile(rfc._LABEL_REGEX)
        good_examples = [
            "a",
            "a-7",
            "a77",
            "a7A",
            "foo-77"
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good Label '{l}' didn't match regex".format(l=good_example))

    def test_label_exclusive(self):
        expression = re.compile(rfc._LABEL_REGEX)
        bad_examples = [
            "7",
            "-",
            "-aa",
            "7aa",
            "a-",
            ""
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad Label '{l}' matched regex".format(l=bad_example))

    def test_subdomain_inclusive(self):
        expression = re.compile(rfc._SUBDOMAIN_REGEX)
        good_examples = [
            "a",
            "a-7",
            "foo-77.a-7.aa",
            "localhost",
            "foo.bar.com",
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good subdomain '{l}' didn't match regex".format(l=good_example))

    def test_subdomain_exclusive(self):
        expression = re.compile(rfc._SUBDOMAIN_REGEX)
        bad_examples = [
            "7",
            "-",
            "a.-aa",
            "a.7aa",
            "a-",
            "a.",
            ".a",
            ""
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad subdomain '{l}' matched regex".format(l=bad_example))

    def test_ipv4_inclusive(self):
        expression = re.compile(rfc._IPV4_IP_REGEX)
        good_examples = [
            "0.0.0.0",
            "127.0.0.1",
            "250.250.250.250",
            "255.255.255.255",
            "249.249.249.249",
            "200.200.200.200",
            "199.199.199.199",
            "100.100.100.100",
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good ipv4 address '{l}' didn't match regex".format(l=good_example))

    def test_ipv4_exclusive(self):
        expression = re.compile(rfc._SUBDOMAIN_REGEX)
        bad_examples = [
            "127.1.1",
            "127.a.1.1",
            "123:145a::1",
            "::1",
            ""
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad ipv4 '{l}' matched regex".format(l=bad_example))

    def test_ipv6_inclusive(self):
        expression = re.compile(rfc._IPV6_IP_REGEX)
        good_examples = [
            "2001:0db8:0000:0000:0000:ff00:0042:8329",
            "2001:db8:0:0:0:ff00:42:8329",
            "2001:db8::ff00:42:8329",
            "0000:0000:0000:0000:0000:0000:0000:0001",
            "::1"
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good ipv6 address '{l}' didn't match regex".format(l=good_example))

    def test_ipv6_exclusive(self):
        expression = re.compile(rfc._SUBDOMAIN_REGEX)
        bad_examples = [
            "127.0.0.1",
            "2001:0dg8:0000:0000:0000:ff00:0042:8329",
            "2",
            ""
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad ipv4 '{l}' matched regex".format(l=bad_example))

    def test_ip_inclusive(self):
        expression = re.compile(rfc._IP_REGEX)
        good_examples = [
            "0.0.0.0",
            "127.0.0.1",
            "250.250.250.250",
            "255.255.255.255",
            "249.249.249.249",
            "200.200.200.200",
            "199.199.199.199",
            "100.100.100.100",
            "2001:0db8:0000:0000:0000:ff00:0042:8329",
            "2001:db8:0:0:0:ff00:42:8329",
            "2001:db8::ff00:42:8329",
            "0000:0000:0000:0000:0000:0000:0000:0001",
            "::1"
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good ip address '{l}' didn't match regex".format(l=good_example))

    def test_ip_exclusive(self):
        expression = re.compile(rfc._IP_REGEX)
        bad_examples = [
            "127.1.1",
            "127.a.1.1",
            "2001:0dg8:0000:0000:0000:ff00:0042:8329",
            "2",
            ""
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad ip '{l}' matched regex".format(l=bad_example))

    def test_domain_inclusive(self):
        expression = re.compile(rfc._DOMAIN_REGEX)
        good_examples = [
            "a",
            "a-7",
            "foo-77.a-7.aa",
            "localhost",
            "foo.bar.com",
            "0.0.0.0",
            "127.0.0.1",
            "250.250.250.250",
            "255.255.255.255",
            "249.249.249.249",
            "200.200.200.200",
            "199.199.199.199",
            "100.100.100.100",
            "2001:0db8:0000:0000:0000:ff00:0042:8329",
            "2001:db8:0:0:0:ff00:42:8329",
            "2001:db8::ff00:42:8329",
            "0000:0000:0000:0000:0000:0000:0000:0001",
            "::1"
        ]
        for good_example in good_examples:
            self.assertTrue(
                bool(expression.fullmatch(good_example)),
                msg="Good domain '{l}' didn't match regex".format(l=good_example))

    def test_domain_exclusive(self):
        expression = re.compile(rfc._DOMAIN_REGEX)
        bad_examples = [
            "127.1.1",
            "127.a.1.1",
            "2001:0dg8:0000:0000:0000:ff00:0042:8329",
            "7",
            "-",
            "a.-aa",
            "a.7aa",
            "a-",
            "a.",
            ".a",
            ""
        ]
        for bad_example in bad_examples:
            self.assertFalse(
                bool(expression.fullmatch(bad_example)),
                msg="Bad domain '{l}' matched regex".format(l=bad_example))






