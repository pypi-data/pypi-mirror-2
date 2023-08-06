#
# Copyright (c) 2006-2010, Prometheus Research, LLC
# Authors: Clark C. Evans <cce@clarkevans.com>,
#          Kirill Simonov <xi@resolvent.net>
#


"""
:mod:`htsql.fmt.json`
=====================

This module implements the JSON renderer.
"""


from ..adapter import adapts
from .format import Format, Formatter, Renderer
from ..domain import (Domain, BooleanDomain, NumberDomain, FloatDomain,
                      StringDomain, EnumDomain, DateDomain)
from .entitle import entitle
import re


class JSONRenderer(Renderer):

    # Note: see `http://www.ietf.org/rfc/rfc4627.txt`.
    name = 'application/json'
    aliases = ['json']

    def render(self, product):
        status = self.generate_status(product)
        headers = self.generate_headers(product)
        body = self.generate_body(product)
        return status, headers, body

    def generate_status(self, product):
        return "200 OK"

    def generate_headers(self, product):
        filename = str(product.profile.segment.syntax)
        filename = filename.replace('\\', '\\\\').replace('"', '\\"')
        return [('Content-Type', 'application/json'),
                ('Content-Disposition',
                 'attachment; filename="(%s).json"' % filename)]

    def generate_body(self, product):
        titles = [escape(entitle(element.binding))
                  for element in product.profile.segment.elements]
        domains = [element.domain
                   for element in product.profile.segment.elements]
        tool = JSONFormatter(self)
        formats = [Format(self, domain, tool) for domain in domains]
        yield "[\n"
        items = titles
        for record in product:
            yield "  [%s],\n" % ", ".join(items)
            items = [format(value)
                     for format, value in zip(formats, record)]
        yield "  [%s]\n" % ", ".join(items)
        yield "]\n"


class JSONFormatter(Formatter):

    adapts(JSONRenderer)


class FormatDomain(Format):

    adapts(JSONRenderer, Domain)

    def __call__(self, value):
        if value is None:
            return "null"
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        else:
            value = str(value)
        try:
            value.decode('utf-8')
        except UnicodeDecodeError:
            value = repr(value)
        return escape(value)


class FormatBoolean(Format):

    adapts(JSONRenderer, BooleanDomain)

    def __call__(self, value):
        if value is None:
            return "null"
        if value is True:
            return "true"
        if value is False:
            return "false"


class FormatNumber(Format):

    adapts(JSONRenderer, NumberDomain)

    def __call__(self, value):
        if value is None:
            return "null"
        return str(value)


class FormatFloat(Format):

    adapts(JSONRenderer, FloatDomain)

    def __call__(self, value):
        if value is None:
            return "null"
        return repr(value)


class FormatString(Format):

    adapts(JSONRenderer, StringDomain)

    def __call__(self, value):
        if value is None:
            return "null"
        return escape(value)


class FormatEnum(Format):

    adapts(JSONRenderer, EnumDomain)

    def __call__(self, value):
        if value is None:
            return "null"
        return escape(value)


class FormatDate(Format):

    adapts(JSONRenderer, DateDomain)

    def __call__(self, value):
        if value is None:
            return "null"
        return str(value)


class Escape(object):

    escape_pattern = r"""[\x00-\x1F\\/"]"""
    escape_regexp = re.compile(escape_pattern)
    escape_table = {
            '"': '"',
            '\\': '\\',
            '/': '/',
            '\x08': 'b',
            '\x0C': 'f',
            '\x0A': 'n',
            '\x0D': 'r',
            '\x09': 't',
    }

    @classmethod
    def replace(cls, match):
        char = match.group()
        if char in cls.escape_table:
            return '\\'+cls.escape_table[char]
        return '\\u%04X' % ord(char)

    @classmethod
    def escape(cls, value):
        value = value.decode('utf-8')
        value = cls.escape_regexp.sub(cls.replace, value)
        value = value.encode('utf-8')
        return '"%s"' % value


escape = Escape.escape


