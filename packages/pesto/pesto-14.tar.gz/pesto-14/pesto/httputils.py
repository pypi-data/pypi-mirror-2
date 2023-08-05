# Copyright (c) 2009 Oliver Cope. All rights reserved.
# See LICENSE.txt for terms of redistribution and use.

"""
pesto.httputils
---------------

Utility functions to handle HTTP data
"""
import email.message
import email.parser
import re
from urllib import unquote_plus
from shutil import copyfileobj

from pesto.utils import ExpandableOutput, SizeLimitedInput, PutbackInput, DelimitedInput

KB = 1024
MB = 1024 * KB

class RequestParseError(Exception):
    """
    Error encountered while parsing the HTTP request
    """
    def response(self):
        """
        Return a ``pesto.response.Response`` object to represent this error condition
        """
        from pesto.response import Response
        return Response.bad_request().add_header('X-Pesto-Exception', repr(self))

class TooBig(RequestParseError):
    """
    Request body is too big
    """
    def response(self):
        """
        Return a ``pesto.response.Response`` object to represent this error condition
        """
        from pesto.response import Response
        return Response.request_entity_too_large()

class MissingContentLength(RequestParseError):
    """
    No ``Content-Length`` header given
    """
    def response(self):
        """
        Return a ``pesto.response.Response`` object to represent this error condition
        """
        from pesto.response import Response
        return Response.length_required()

def dequote(s):
    """
    Example usage::

        >>> dequote('foo')
        'foo'
        >>> dequote('"foo"')
        'foo'
    """
    if len(s) > 1 and s[0] == '"' == s[-1]:
        return s[1:-1]
    return s

def parse_header(header):
    """
    Given a header, return a tuple of ``(value, [(parameter_name, parameter_value)])``.

    Example usage::

        >>> parse_header("text/html; charset=UTF-8")
        ('text/html', {'charset': 'UTF-8'})
        >>> parse_header("multipart/form-data; boundary=---------------------------7d91772e200be")
        ('multipart/form-data', {'boundary': '---------------------------7d91772e200be'})
    """
    items = header.split(';')
    pairs = [
        (name, dequote(value))
             for name, value in (
                 item.lstrip().split('=', 1)
                    for item in items[1:]
            )
    ]
    return (items[0], dict(pairs))

def parse_querystring(
    data,
    charset=None,
    strict=False,
    keep_blank_values=True,
    pairsplitter=re.compile('[;&]').split
):
    """
    Return ``(key, value)`` pairs from the given querystring::

        >>> list(parse_querystring('green%20eggs=ham;me=sam+i+am'))
        [(u'green eggs', u'ham'), (u'me', u'sam i am')]

    charset
        Character encoding used to decode values. If not specified,
        ``pesto.DEFAULT_CHARSET`` will be used.

    keep_blank_values
        if True, keys without associated values will be returned
        as empty strings. if False, no key, value pair will be returned.

    strict
        if ``True``, a ``ValueError`` will be raised on parsing errors.
    """

    if charset is None:
        charset = DEFAULT_CHARSET

    for item in pairsplitter(data):
        if not item:
            continue
        try:
            key, value = item.split('=', 1)
        except ValueError:
            if strict:
                raise RequestParseError("bad query field: %r" % (item,))
            if not keep_blank_values:
                continue
            key, value = item, ''

        try:
            yield unquote_plus(key).decode(charset), unquote_plus(value).decode(charset)
        except UnicodeDecodeError:
            raise RequestParseError("Invalid character data: can't decode using %r" % (charset,))

def parse_post(environ, fp, default_charset=None, max_size=16*KB, max_multipart_size=2*MB):
    """
    Parse the contents of an HTTP POST request, which may be either
    application/x-www-form-urlencoded or multipart/form-data encoded.

    Returned items are either tuples of (name, value) for simple string values
    or (name, FileUpload) for uploaded files.

    max_multipart_size
        Maximum size of total data for a multipart form submission

    max_size
        The maximum size of data allowed to be read into memory.

        For a application/x-www-form-urlencoded submission, this is the maximum
        size of the entire data.

        For a multipart/form-data submission, this is the maximum size of any
        single non file-upload field.
    """
    content_type, content_type_params = parse_header(
        environ.get('CONTENT_TYPE', 'application/x-www-form-urlencoded')
    )

    if default_charset is None:
        default_charset = DEFAULT_CHARSET
    charset = content_type_params.get('charset', default_charset)

    try:
        content_length = int(environ['CONTENT_LENGTH'])
    except (TypeError, ValueError, KeyError):
        raise MissingContentLength()

    if content_type == 'application/x-www-form-urlencoded':

        if content_length > max_size:
            raise TooBig("Content Length exceeds permitted size")
        return parse_querystring(SizeLimitedInput(fp, content_length).read(), charset)

    else:
        if content_length > max_multipart_size:
            raise TooBig("Content Length exceeds permitted size")
        try:
            boundary = content_type_params['boundary']
        except KeyError:
            raise RequestParseError("No boundary given in multipart/form-data content-type")
        return parse_multipart(SizeLimitedInput(fp, content_length), boundary, charset, max_size)

class HTTPMessage(email.message.Message):
    """
    Represent HTTP request message headers
    """

CHUNK_SIZE = 8192

def parse_multipart(fp, boundary, default_charset, max_size):
    """
    Parse data encoded as ``multipart/form-data``. Generate tuples of::

        (<field-name>, <data>)

    Where ``data`` will be a string in the case of a regular input field, or a
    ``FileUpload`` instance if a file was uploaded.

    fp
        input stream from which to read data
    boundary
        multipart boundary string, as specified by the ``Content-Disposition`` header
    default_charset
        character set to use for encoding, if not specified by a content-type header.
        In practice web browsers don't supply a content-type header so this
        needs to contain a sensible value.
    max_size
        Maximum size in bytes for any non file upload part
    """

    boundary_size = len(boundary)
    if not boundary.startswith('--'):
        raise RequestParseError("Malformed boundary string: must start with '--' (rfc 2046)")
    if boundary_size > 72:
        raise RequestParseError("Malformed boundary string: must be no more than 70 characters, not counting the two leading hyphens (rfc 2046)")

    assert boundary_size + 2 < CHUNK_SIZE, "CHUNK_SIZE cannot be smaller than the boundary string"

    if fp.read(2) != '--':
        raise RequestParseError("Malformed POST data: expected two hypens")

    if fp.read(boundary_size) != boundary:
        raise RequestParseError("Malformed POST data (expected boundary)")

    if fp.read(2) != '\r\n':
        raise RequestParseError("Malformed POST data (expected CRLF)")

    fp = PutbackInput(fp)

    while True:
        headers, data = _read_multipart_field(fp, boundary)
        try:
            disposition_type, params = parse_header(headers['Content-Disposition'])
        except KeyError:
            raise RequestParseError("Missing Content-Disposition header")

        try:
            name = params['name']
        except KeyError:
            raise RequestParseError("Missing name parameter in Content-Disposition header")

        is_file_upload = 'Content-Type' in headers and 'filename' in params
        if is_file_upload:
            io = data._io
            io.seek(0)
            yield name, FileUpload(params['filename'], headers, io)

        else:
            charset = parse_header(headers.get('Content-Type', ''))[1].get('charset', default_charset)
            if data.tell() > max_size:
                raise TooBig("Data block exceeds maximum permitted size")
            try:
                data.seek(0)
                yield name, data.read().decode(charset)
            except UnicodeDecodeError:
                raise RequestParseError("Invalid character data: can't decode using %r" % (charset,))

        chunk = fp.read(2)
        if chunk == '--':
            if fp.peek(3) != '\r\n':
                raise RequestParseError("Expected terminating CRLF at end of stream")
            break

        if chunk != '\r\n':
            raise RequestParseError("Expected CRLF after boundary")

CONTENT_DISPOSITION_FORM_DATA = 'form-data'
CONTENT_DISPOSITION_FILE_UPLOAD = 'file-upload'

def _read_multipart_field(fp, boundary):
    """
    Read a single part from a multipart/form-data message and return a tuple of
    ``(headers, data)``. Stream ``fp`` must be positioned at the start of the
    header block for the field.

    Return a tuple of ('<headers>', '<data>')

    ``headers`` is an instance of ``email.message.Message``.

    ``data`` is an instance of ``ExpandableOutput``.

    Note that this currently cannot handle nested multipart sections.
    """
    data = ExpandableOutput()
    parser = email.parser.Parser(_class=HTTPMessage)
    headers = parser.parse(DelimitedInput(fp, '\r\n\r\n'), headersonly=True)
    fp = DelimitedInput(fp, '\r\n--' + boundary)
    # XXX: handle base64 encoding etc
    for chunk in iter(lambda: fp.read(CHUNK_SIZE), ''):
        data.write(chunk)
    data.flush()

    # Fallen off the end of the input without having read a complete field?
    if not fp.delimiter_found:
        raise RequestParseError("Incomplete data (expected boundary)")

    return headers, data


class FileUpload(object):

    """
    Represent a file uploaded in an HTTP form submission
    """

    def __init__(self, filename, headers, fileob):

        self.filename = filename
        self.headers = headers
        self.file = fileob

        # UNC/Windows path
        if self.filename[:2] == '\\\\' or self.filename[1:3] == ':\\':
            self.filename = self.filename[self.filename.rfind('\\')+1:]

    def save(self, fileob):
        """
        Save the upload to the file object or path ``fileob``
        """
        if isinstance(fileob, basestring):
            fileob = open(fileob, 'w')
            try:
                return self.save(fileob)
            finally:
                fileob.close()

        self.file.seek(0)
        copyfileobj(self.file, fileob)

# Imports at end to avoid circular dependencies
from pesto import DEFAULT_CHARSET
