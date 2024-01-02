# pylint: skip-file


class Dialog:
    def ok(self, header: str, msg: str):
        print("--- {0} --- {1}".format(header, msg))
