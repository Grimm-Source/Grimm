import re

from sqlalchemy.orm import class_mapper


def serialize(model):
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


def variable_name_pythonic(s):
    """
    Use regular expressions to deform and decompose strings into words, and add _ as a separator to combine them
    inner sub: re.sub(pattern, repl, string, count=0, flags=0) match the words
    repl: lambda mo: ' ' + mo.group(0).lower() split the words and convert to lower letters
    outer sub: replace space、_、- to space。then split with space
    finally join with _
    :param s: pickImpairedNo
    :return: pick_impaired_no
    """
    return '_'.join(re.sub(r"(\s|_|-)+", " ",
                           re.sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
                                  lambda mo: ' ' + mo.group(0).lower(), s)).split())
