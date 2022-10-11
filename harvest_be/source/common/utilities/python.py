# -*- coding: utf-8 -*-


class PythonUtil
    @classmethod
    def get_class_full_import_path(cls, _class):
        return _class.__module__ + '.' + _class.__name__
