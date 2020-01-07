import unittest

from eynnyd.internal.utils.uri_components_converter import URIComponentsConverter
from eynnyd.exceptions import InvalidURIException


class TestURIComponentsConverter(unittest.TestCase):

    def test_empty_path_raises(self):
        with self.assertRaises(InvalidURIException):
            URIComponentsConverter.from_uri("")

    def test_single_slash_returns_single_empty_component(self):
        components = URIComponentsConverter.from_uri("/")
        self.assertEqual(0, len(components))

    def test_multiple_neighboring_slashes_raises(self):
        with self.assertRaises(InvalidURIException):
            URIComponentsConverter.from_uri("/foo///bar")

    def test_no_leading_slash_raises(self):
        with self.assertRaises(InvalidURIException):
            URIComponentsConverter.from_uri("foo/bar")

    def test_trailing_slash_is_ignored(self):
        without_trailing_slash_components = URIComponentsConverter.from_uri("/foo/bar")
        with_trailing_slash_components = URIComponentsConverter.from_uri("/foo/bar/")
        self.assertListEqual(without_trailing_slash_components, with_trailing_slash_components)

    def test_component_extraction(self):
        components = URIComponentsConverter.from_uri("/foo/bar/99/buzz")
        self.assertListEqual(["foo", "bar", "99", "buzz"], components)

