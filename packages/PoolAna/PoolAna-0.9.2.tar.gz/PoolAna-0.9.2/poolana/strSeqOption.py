from optparse import Option, OptionValueError
from copy import copy

class strSeqOption(Option):
    def check_string_seq(option, opt, value):
        try:
            return value.split(",")
        except ValueError:
            raise OptionValueError(
                "option %s: invalid string sequence value: %r" % (opt, value))

    TYPES = Option.TYPES + ("string-seq",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["string-seq"] = check_string_seq
