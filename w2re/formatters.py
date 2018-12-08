from w2re.prefix_tree.primitives import PrefixTreeNode


class BaseFormatter:
    _DESCRIPTION = ''
    _CODE = ''

    @staticmethod
    def wrap_regexp(root_node: PrefixTreeNode) -> str:
        raise NotImplementedError()

    @classmethod
    def description(cls):
        assert cls._DESCRIPTION, "Sub-classes must override _DESCRIPTION"
        return cls._DESCRIPTION

    @classmethod
    def code(cls):
        assert cls._CODE, "Sub-classes must override _CODE"
        return cls._CODE


class PythonFormatter(BaseFormatter):
    _DESCRIPTION = 'Python regular expression'
    _CODE = 'py'
    _EMPTY_STRING_MATCH = r"\A\Z"

    @staticmethod
    def wrap_regexp(root_node: PrefixTreeNode) -> str:
        regexp = root_node.to_regexp()

        if regexp:
            return regexp

        return PythonFormatter._EMPTY_STRING_MATCH


class PythonWordMatchFormatter(PythonFormatter):
    _DESCRIPTION = 'Python word matching regular expression'
    _CODE = 'pyw'

    @staticmethod
    def wrap_regexp(root_node: PrefixTreeNode) -> str:
        regexp = root_node.to_regexp()

        if regexp:
            return r"(?:\W+|\A)({})(?=\W+|\Z)".format(regexp)

        return PythonFormatter._EMPTY_STRING_MATCH


ALL_FORMATTERS = (PythonFormatter, PythonWordMatchFormatter)
