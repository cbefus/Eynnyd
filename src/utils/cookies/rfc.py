import re
"""
These are constants and expressions that match RFC guidelines laid out in the following docs
General: https://www.ietf.org/rfc/rfc2616.txt  (sec 2.2)
Dates: https://www.ietf.org/rfc/rfc2616.txt (sec 3.3)
Domains: https://www.ietf.org/rfc/rfc1034.txt (sec 3.5) and https://www.ietf.org/rfc/rfc1123.txt (sec 2.1)
Cookies: https://www.ietf.org/rfc/rfc6265.txt (sec 4)

"""

### General

_CONTROL_CHARS = r"\x00-\x1F\x7F"
_SPACE_CHAR = r"\x20"
_TAB_CHAR = r"\x09"
_SEPARATOR_CHARS = r"\x28\x29\x3C\x3E\x40\x2C\x3B\x3A\x5C\x22\x2F\x5B\x5D\x3F\x3D\x7B\x7D" + _SPACE_CHAR + "" + _TAB_CHAR
_TOKEN_REGEX = r"^([^" + _CONTROL_CHARS + _SEPARATOR_CHARS + "])+$"

### Dates (GMT Only)
"""
Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123
Sunday, 06-Nov-94 08:49:37 GMT ; RFC 850, obsoleted by RFC 1036
Sun Nov  6 08:49:37 1994       ; ANSI C's asctime() format
"""
_1_DIGIT_REGEX = r"([0-9]){1}"
_2_DIGIT_REGEX = r"([0-9]){2}"
_4_DIGIT_REGEX = r"([0-9]){4,4}"
_TIME_ZONE_SUFFIX = r"GMT"
_TIME_REGEX = r"(" + _2_DIGIT_REGEX + ":" + _2_DIGIT_REGEX + ":" + _2_DIGIT_REGEX + ")"  # note the dont force reasonable numbers in RFC
_MONTH_REGEX = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec){1}"
_WEEKDAY_REGEX = r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday){1}"
_WKDAY_REGEX = r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun){1}"
_ASCTIME_DATE_REGEX = r"(" + _MONTH_REGEX + _SPACE_CHAR + "(" + _2_DIGIT_REGEX + "|(" + _SPACE_CHAR + _1_DIGIT_REGEX + "){1}){1}" + "){1}"
_RFC850_DATE_REGEX = r"(" + _2_DIGIT_REGEX + "-" + _MONTH_REGEX + "-" + _2_DIGIT_REGEX + "){1}"
_RFC1123_DATE_REGEX = r"(" + _2_DIGIT_REGEX + _SPACE_CHAR + _MONTH_REGEX + _SPACE_CHAR + _4_DIGIT_REGEX + "){1}"
_ASCTIME_DATETIME_REGEX = r"(" + _WKDAY_REGEX + _SPACE_CHAR + _ASCTIME_DATE_REGEX + _SPACE_CHAR + _TIME_REGEX + _SPACE_CHAR + _4_DIGIT_REGEX + "){1}"
_RFC850_DATETIME_REGEX = r"(" + _WEEKDAY_REGEX + "," + _SPACE_CHAR + _RFC850_DATE_REGEX + _SPACE_CHAR + _TIME_REGEX + _SPACE_CHAR + _TIME_ZONE_SUFFIX + "){1}"
_RFC1123_DATETIME_REGEX = r"(" + _WKDAY_REGEX + "," + _SPACE_CHAR + _RFC1123_DATE_REGEX + _SPACE_CHAR + _TIME_REGEX + _SPACE_CHAR + _TIME_ZONE_SUFFIX + "){1}"
_HTTP_DATE_REGEX = r"(" + _RFC1123_DATETIME_REGEX + "|" + _RFC850_DATETIME_REGEX + "|" + _ASCTIME_DATETIME_REGEX + "){1}"


### Domains

_LETTERS_REGEX = r"([A-Za-z])"
_LETTERS_DIGITS_REGEX = r"([A-Za-z0-9])"
_LETTER_DIGITS_HYPHENS_REGEX = r"([A-Za-z0-9\-])"
_LABEL_REGEX = r"((" + _LETTERS_REGEX + "+(" + _LETTER_DIGITS_HYPHENS_REGEX + "*" + _LETTERS_DIGITS_REGEX + "+)*)){1,63}"
_SUBDOMAIN_REGEX = r"(" + _LABEL_REGEX + "(." + _LABEL_REGEX + ")*){1}"

_IPV4_IP_REGEX = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?){1}"
_IPV6_IP_REGEX = r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])){1}"
_IP_REGEX = r"(" + _IPV4_IP_REGEX + "|" + _IPV6_IP_REGEX + "){1}"

_DOMAIN_REGEX = r"(" + _SUBDOMAIN_REGEX + "|" + _IP_REGEX + "){1}"
VALID_RFC_DOMAIN = re.compile(_DOMAIN_REGEX)

### Cookies

_COOKIE_NAME_REGEX = _TOKEN_REGEX
VALID_RFC_COOKIE_NAME = re.compile(_COOKIE_NAME_REGEX)
_COOKIE_OCTET_REGEX = r"([\x21\x23-\x2B\x2D-\x3A\x3C-\x5B\x5D-\x7E]){1}"
_COOKIE_VALUE_REGEX = r"((" + _COOKIE_OCTET_REGEX + ")+|(\"(" + _COOKIE_OCTET_REGEX + ")+\")){1}"
VALID_RFC_COOKIE_VALUE = re.compile(_COOKIE_VALUE_REGEX)
_EXPIRES_AV_REGEX = r"(Expires=" + _HTTP_DATE_REGEX + "){1}"
_MAX_AGE_REGEX = r"([1-9])+"
VALID_RFC_MAX_AGE = re.compile(_MAX_AGE_REGEX)
_MAX_AGE_AV_REGEX = r"(Max-Age=" + _MAX_AGE_REGEX + "){1}"
_DOMAIN_AV_REGEX = r"(Domain=" + _DOMAIN_REGEX + "){1}"
_PATH_REGEX = r"([^" + _CONTROL_CHARS + ";])+"
VALID_RFC_PATH = re.compile(_PATH_REGEX)
_PATH_AV_REGEX = r"(Path=" + _PATH_REGEX + "){1}"
_SECURE_AV_REGEX = r"(Secure){1}"
_HTTP_ONLY_AV_REGEX = r"(HttpOnly){1}"
_EXTENTION_AV_REGEX = r"(([^" + _CONTROL_CHARS + ";])+){1}"
_COOKIE_AV_REGEX = r"(" + _EXPIRES_AV_REGEX + "|" + _MAX_AGE_AV_REGEX + "|" + _DOMAIN_AV_REGEX + "|" + _PATH_AV_REGEX + "|" + _SECURE_AV_REGEX + "|" + _HTTP_ONLY_AV_REGEX + "|" + _EXTENTION_AV_REGEX + ")*"
_COOKIE_PAIR_REGEX = r"(" + _COOKIE_NAME_REGEX + "=" + _COOKIE_VALUE_REGEX + "){1}"
_SET_COOKIE_STRING_REGEX = r"(" + _COOKIE_PAIR_REGEX + "(;" + _SPACE_CHAR + _COOKIE_AV_REGEX + ")*" + "){1}"
_SET_COOKIE_HEADER_REGEX = r"(Set-Cookie:" + _SPACE_CHAR + _SET_COOKIE_STRING_REGEX + "){1}"




