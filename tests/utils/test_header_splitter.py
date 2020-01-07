from unittest import TestCase

from eynnyd.internal.utils.header_helpers import HeaderSplitter


class TestHeaderSplitter(TestCase):

    def test_split_to_kv(self):
        kv = HeaderSplitter.split_to_kv("foo= bar;123 =456")
        self.assertDictEqual({"foo": "bar", "123": "456"}, kv)

    def test_split_to_multi_values_by_key(self):
        kv = HeaderSplitter.split_to_multi_values_by_key("foo= bar;123 =456;foo=bam")
        self.assertDictEqual({"foo": ["bar", "bam"], "123": ["456"]}, kv)

