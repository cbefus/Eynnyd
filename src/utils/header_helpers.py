

class HeaderSplitter:

    @staticmethod
    def split_to_kv(header_content):
        kv = {}
        for token in header_content.split(";"):
            k, v = token.strip().split("=")
            kv[k.strip()] = v.strip()
        return kv

    @staticmethod
    def split_to_multi_values_by_key(header_content):
        kv = {}
        for token in header_content.split(";"):
            k, v = token.strip().split("=")
            if k.strip() not in kv:
                kv[k.strip()] = []
            kv[k.strip()].append(v.strip())
        return kv
