#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""vCards v3.0 (RFC 2426) class and parsing + validating functions

Default syntax:

./vcard.py [options] -|file...

Options:
-v,--verbose    Verbose mode

Example:

./vcard.py *.vcf
Validate all .vcf files in the current directory
"""

import codecs
import getopt
import re
import sys
import warnings

# Third party modules
import isodate

# Literals, RFC 2426 pages 27, 28
ALPHA_CHARS = u'\u0041-\u005A\u0061-\u007A'
CHAR_CHARS = u'\u0001-\u007F'
CR_CHAR = u'\u000D'
LF_CHAR = u'\u000A'
CRLF_CHARS = CR_CHAR + LF_CHAR
CTL_CHARS = u'\u0000-\u001F\u007F'
DIGIT_CHARS = u'\u0030-\u0039'
DQUOTE_CHAR = u'\u0022'
HTAB_CHAR = u'\u0009'
SP_CHAR = u'\u0020'
VCHAR_CHARS = u'\u0021-\u007E'
WSP_CHARS = SP_CHAR + HTAB_CHAR
NON_ASCII_CHARS = u'\u0080-\u00FF'
QSAFE_CHARS = WSP_CHARS + u'\u0021' + u'\u0023-\u007E' + NON_ASCII_CHARS
SAFE_CHARS = WSP_CHARS + u'\u0021' + u'\u0023-\u002B' + u'\u002D-\u0039' + \
             u'\u003C-\u007E' + NON_ASCII_CHARS
VALUE_CHARS = WSP_CHARS + VCHAR_CHARS + NON_ASCII_CHARS

# Known property names (RFC 2426 page 4)
MANDATORY_PROPERTIES = ['BEGIN', 'END', 'FN', 'N', 'VERSION']
PREDEFINED_PROPERTIES = ['BEGIN', 'END', 'NAME', 'PROFILE', 'SOURCE']
OTHER_PROPERTIES = [
    'ADR', 'AGENT', 'BDAY', 'CATEGORIES', 'CLASS', 'EMAIL', 'GEO', 'KEY',
    'LABEL', 'LOGO', 'MAILER', 'NICKNAME', 'NOTE', 'ORG', 'PHOTO', 'PRODID',
    'REV', 'ROLE', 'SORT-STRING', 'SOUND', 'TEL', 'TITLE', 'TZ', 'UID', 'URL']
ALL_PROPERTIES = list( # Remove duplicates
    set(
        MANDATORY_PROPERTIES + PREDEFINED_PROPERTIES + OTHER_PROPERTIES))

# IDs for group, name, iana-token, x-name, param-name (RFC 2426 page 29)
ID_CHARS = ALPHA_CHARS + DIGIT_CHARS + '-'

VCARD_LINE_MAX_LENGTH = 75 # RFC 2426 page 6

# Error literals
MSG_CONTINUATION_AT_START = 'Continuation line at start of vCard'
MSG_DOT_AT_LINE_START = 'Dot at start of line without group name'
MSG_EMPTY_LINE = 'Empty line found'
MSG_EMPTY_VCARD = 'vCard is empty'
MSG_INVALID_DATE = 'Invalid date'
MSG_INVALID_FIRST_LINE = 'Invalid first line'
MSG_INVALID_LANGUAGE_VALUE = 'Invalid language'
MSG_INVALID_LAST_LINE = 'Invalid last line'
MSG_INVALID_LINE_SEPARATOR = 'Invalid line ending; should be CRLF (\\r\\n)'
MSG_INVALID_PARAM_NAME = 'Invalid parameter name'
MSG_INVALID_PARAM_VALUE = 'Invalid parameter value'
MSG_INVALID_PROPERTY_NAME = 'Invalid property name'
MSG_INVALID_SUBVALUE = 'Invalid subvalue'
MSG_INVALID_SUBVALUE_COUNT = 'Invalid subvalue count'
MSG_INVALID_TIME = 'Invalid time'
MSG_INVALID_TIME_ZONE = 'Invalid time zone'
MSG_INVALID_VALUE = 'Invalid value'
MSG_INVALID_VALUE_COUNT = 'Invalid value count'
MSG_INVALID_X_NAME = 'Invalid X-name'
MSG_MISMATCH_GROUP = 'Group mismatch'
MSG_MISMATCH_PARAM = 'Parameter mismatch'
MSG_MISSING_GROUP = 'Missing group'
MSG_MISSING_PARAM = 'Parameter missing'
MSG_MISSING_PARAM_VALUE = 'Parameter value missing'
MSG_MISSING_PROPERTY = 'Mandatory property missing'
MSG_MISSING_VALUE_STRING = 'Missing value string'
MSG_NON_EMPTY_PARAM = 'Property should not have parameters'

# Warning literals
WARN_DEFAULT_TYPE_VALUE = 'Using default TYPE value; can be removed'
WARN_INVALID_DATE = 'Possible invalid date'
WARN_INVALID_EMAIL_TYPE = 'Possible invalid email TYPE'
WARN_MULTIPLE_NAMES = 'Possible split name (replace space with comma)'


# pylint: disable-msg=R0913,W0613,W0622,W0231
def _show_warning(
    message,
    category = UserWarning,
    filename = '',
    lineno = -1,
    file = sys.stderr,
    line = None):
    """Custom simple warning."""
    file.write(str(message) + '\n')
# pylint: enable-msg=R0913,W0613,W0622,W0231


class VCardFormatError(Exception):
    """Thrown if the text given is not a valid according to RFC 2426."""
    def __init__(
        self,
        message,
        context):
        """
        vCard format error.

        @param message: Error message
        @param context: Dictionary with context information

        Examples:
        >>> raise VCardFormatError('test', {})
        Traceback (most recent call last):
        VCardFormatError: test
        >>> raise VCardFormatError('with path', {'path': '/home/user/test.vcf'})
        Traceback (most recent call last):
        VCardFormatError: with path
        File: /home/user/test.vcf
        """
        Exception.__init__(self)
        self.message = message.encode('utf-8')
        self.context = context


    def __str__(self):
        """Outputs error with ordered context info."""
        message = self.message

        for key, value in self.context.items():
            message += '\n'
            if key == 'path':
                message += 'File'
            elif key == 'file_line':
                message += 'File line number'
                value += 1
            elif key == 'vcard_line':
                message += 'vCard line number'
                value += 1
            elif key == 'property':
                message += 'Property'
            elif key == 'property_line':
                message += 'Property line'
            else:
                message += key

            message += ': ' + str(value)

        return message


def validate_date(text):
    """
    Based on http://tools.ietf.org/html/rfc2425#section-5.8.4 and the fact
    that it specifies a subset of ISO 8601.

    @param text: String

    Examples:
    >>> validate_date('20000101')
    >>> validate_date('2000-01-01')
    >>> validate_date('2000:01:01') # Wrong separator
    Traceback (most recent call last):
    VCardFormatError: Invalid date: 2000:01:01
    >>> validate_date('2000101') # Too short
    Traceback (most recent call last):
    VCardFormatError: Invalid date: 2000101
    >>> validate_date('20080229')
    >>> validate_date('20100229') # Not a leap year
    Traceback (most recent call last):
    VCardFormatError: Invalid date: 20100229
    >>> validate_date('19000229') # Not a leap year (divisible by 100)
    Traceback (most recent call last):
    VCardFormatError: Invalid date: 19000229
    >>> validate_date('20000229') # Leap year (divisible by 400)
    >>> validate_date('aaaa-bb-cc')
    Traceback (most recent call last):
    VCardFormatError: Invalid date: aaaa-bb-cc
    """
    if re.match(r'^\d{4}-?\d{2}-?\d{2}$', text) is None:
        raise VCardFormatError(MSG_INVALID_DATE + ': %s' % text, {})

    try:
        isodate.parse_date(text)
    except (isodate.ISO8601Error, ValueError):
        raise VCardFormatError(MSG_INVALID_DATE + ': %s' % text, {})


def validate_time_zone(text):
    """
    Based on http://tools.ietf.org/html/rfc2425#section-5.8.4 and the fact
    that it specifies a subset of ISO 8601.

    @param text: String

    Examples:
    >>> validate_time_zone('Z')
    >>> validate_time_zone('+01:00')
    >>> validate_time_zone('-12:30')
    >>> validate_time_zone('+23:59')
    >>> validate_time_zone('-0001')
    >>> validate_time_zone('-00:30')
    >>> validate_time_zone('+00:30')
    >>> validate_time_zone('Z+01:00') # Can't combine Z and offset
    Traceback (most recent call last):
    VCardFormatError: Invalid time zone: Z+01:00
    >>> validate_time_zone('+1:00') # Need preceding zero
    Traceback (most recent call last):
    VCardFormatError: Invalid time zone: +1:00
    >>> validate_time_zone('0100') # Need + or -
    Traceback (most recent call last):
    VCardFormatError: Invalid time zone: 0100
    >>> validate_time_zone('01') # Need colon and minutes
    Traceback (most recent call last):
    VCardFormatError: Invalid time zone: 01
    >>> validate_time_zone('01:') # Need minutes
    Traceback (most recent call last):
    VCardFormatError: Invalid time zone: 01:
    >>> validate_time_zone('01:1') # Need preceding zero
    Traceback (most recent call last):
    VCardFormatError: Invalid time zone: 01:1
    """
    if not re.match(r'^(Z|[+-]\d{2}:?\d{2})$', text):
        raise VCardFormatError(MSG_INVALID_TIME_ZONE + ': %s' % text, {})

    try:
        isodate.parse_tzinfo(text.replace('+', 'Z+').replace('-', 'Z-'))
    except (isodate.ISO8601Error, ValueError):
        raise VCardFormatError(MSG_INVALID_TIME_ZONE + ': %s' % text, {})


def validate_time(text):
    """
    Based on http://tools.ietf.org/html/rfc2425#section-5.8.4 and the fact
    that it specifies a subset of ISO 8601.

    @param text: String

    Examples:
    >>> validate_time('00:00:00')
    >>> validate_time('000000')
    >>> validate_time('01:02:03Z')
    >>> validate_time('01:02:03+01:30')
    >>> validate_time('01:02:60')
    Traceback (most recent call last):
    VCardFormatError: Invalid time: 01:02:60
    >>> validate_time('01:60:59')
    Traceback (most recent call last):
    VCardFormatError: Invalid time: 01:60:59
    >>> validate_time('24:00:00')
    Traceback (most recent call last):
    VCardFormatError: Invalid time: 24:00:00
    """
    time_timezone = re.match(r'^(\d{2}:?\d{2}:?\d{2}(?:,\d+)?)(.*)$', text)
    if time_timezone is None:
        raise VCardFormatError(MSG_INVALID_TIME + ': %s' % text, {})

    time_str, timezone_str = time_timezone.groups()
    try:
        isodate.parse_time(time_str)
    except (isodate.ISO8601Error, ValueError):
        raise VCardFormatError(MSG_INVALID_TIME + ': %s' % text, {})

    if timezone_str == '':
        return

    validate_time_zone(timezone_str)


def find_unescaped(text, char, escape_char = '\\'):
    """
    Find occurrence of an unescaped character.

    @param text: String
    @param char: Character to find
    @param escape_char: Escape character
    @return: Index of first match, None if no match
    """
    unescaped_regex = '(?<!' + escape_char + ')' + \
            '(?:' + escape_char + escape_char + ')*' + \
            '(' + char + ')'
    regex = re.compile(unescaped_regex)

    char_match = regex.search(text)

    if char_match is None:
        return None
    return char_match.start(1)


def split_unescaped(text, separator, escape_char = '\\\\'):
    """
    Find strings separated by an unescaped character.

    @param text: String
    @param separator: Separator
    @param escape_char: Escape character
    @return: List of strings between separators, excluding the separator
    """
    result = []
    while True:
        index = find_unescaped(text, separator, escape_char)
        if index is not None:
            result.append(text[:index])
            text = text[index + 1:]
        else:
            result.append(text)
            return result


def unfold_vcard_lines(lines):
    """
    Unsplit lines in vCard, warning about short lines. RFC 2426 page 8.

    @param lines: List of potentially folded vCard lines
    @return: List of lines, one per property
    """
    property_lines = []
    for index in range(len(lines)):
        line = lines[index]
        if not line.endswith(CRLF_CHARS):
            raise VCardFormatError(
                MSG_INVALID_LINE_SEPARATOR,
                {'file_line': index})
        if len(line) > VCARD_LINE_MAX_LENGTH + len(CRLF_CHARS):
            warnings.warn('Long line in vCard: %s' % line.encode('utf-8'))

        if line.startswith(' '):
            if index == 0:
                raise VCardFormatError(
                    MSG_CONTINUATION_AT_START,
                    {'file_line': 0})
            elif len(lines[index - 1]) < VCARD_LINE_MAX_LENGTH:
                warnings.warn('Short folded line at line %i' % (index - 1))
            elif line == SP_CHAR + CRLF_CHARS:
                warnings.warn('Empty folded line at line %i' % index)
            property_lines[-1] = property_lines[-1][:-len(CRLF_CHARS)] + \
                                 line[1:]
        else:
            property_lines.append(line)

    return property_lines


def get_vcard_group(lines):
    """
    Get & validate group. RFC 2426 pages 28, 29.

    @param lines: List of unfolded vCard lines
    @return: Group name if one exists, None otherwise
    """
    group = None

    group_re = re.compile('^([' + ID_CHARS + ']*)\.')

    group_match = group_re.match(lines[0])
    if group_match is not None:
        group = group_match.group(1)

        # Validate
        if len(group) == 0:
            raise VCardFormatError(MSG_DOT_AT_LINE_START, {})

        for index in range(len(lines)):
            line = lines[index]
            next_match = group_re.match(line)
            if not next_match:
                raise VCardFormatError(MSG_MISSING_GROUP, {'file_line': index})
            if next_match.group(1) != group:
                raise VCardFormatError(
                    MSG_MISMATCH_GROUP + ': %s != %s' % (
                        next_match.group(1),
                        group),
                    {'file_line': index})
    else:
        # Make sure there are no groups elsewhere
        for index in range(len(lines)):
            if group_re.match(lines[index]):
                raise VCardFormatError(
                    MSG_MISMATCH_GROUP + ': %s != %s' % (
                        next_match.group(1),
                        group),
                    {'file_line': index})

    return group


def remove_vcard_groups(lines, group):
    """
    Remove groups from vCard. RFC 2426 pages 28, 29.

    @param lines: List of unfolded vCard lines
    @return: Lines without groups and dot separator
    """
    if group:
        for index in range(len(lines)):
            lines[index] = lines[index][len(group):]
    return lines


def get_vcard_property_param_values(values_string):
    """
    Get the parameter values. RFC 2426 page 29.

    @param text: Comma separated values
    @return: Set of values. Assumes that sequence doesn't matter and that
    duplicate values can be discarded, even though RFC 2426 doesn't explicitly
    say this. I.e., assumes that TYPE=WORK,VOICE,WORK === TYPE=VOICE,WORK.
    """
    values = set(split_unescaped(values_string, ','))

    # Validate
    for value in values:
        if not re.match(
            '^[' + SAFE_CHARS + ']+$|^"[' + QSAFE_CHARS + ']+"$',
            value):
            raise VCardFormatError(MSG_INVALID_VALUE + ': %s' % value, {})

    return values


def get_vcard_property_param(param_string):
    """
    Get the parameter name and value(s). RFC 2426 page 29.

    @param param_string: Single parameter and values
    @return: Dictionary with a parameter name and values
    """
    try:
        param_name, values_string = split_unescaped(param_string, '=')
    except ValueError as error:
        raise VCardFormatError(MSG_MISSING_PARAM_VALUE + ': %s' % error, {})

    values = get_vcard_property_param_values(values_string)

    # Validate
    if not re.match('^[' + ID_CHARS + ']+$', param_name):
        raise VCardFormatError(
            MSG_INVALID_PARAM_NAME + ': %s' % param_name,
            {})

    return {'name': param_name, 'values': values}


def get_vcard_property_params(params_string):
    """
    Get the parameters and their values. RFC 2426 page 28.

    @param params_string: Part of a vCard line between the first semicolon
    and the first colon.
    @return: Dictionary of parameters. Assumes that
    TYPE=WORK;TYPE=WORK,VOICE === TYPE=VOICE,WORK === TYPE=VOICE;TYPE=WORK.
    """
    params = {}
    if not params_string:
        return params

    for param_string in split_unescaped(params_string, ';'):
        param = get_vcard_property_param(param_string)
        param_name = param['name'].upper() # To be able to merge TYPE & type
        if param_name not in params:
            params[param_name] = param['values']
        else:
            # Merge
            params[param_name] = params[param_name].union(
                param['values'])

    return params


def get_vcard_property_subvalues(value_string):
    """
    Get the parts of the value.

    @param value_string: Single value string
    @return: List of values (RFC 2426 page 9)
    """
    subvalues = split_unescaped(value_string, ',')

    # Validate string
    for subvalue in subvalues:
        if not re.match('^[' + VALUE_CHARS + ']*$', subvalue):
            raise VCardFormatError(MSG_INVALID_SUBVALUE + ': %s' % subvalue, {})

    return subvalues


def get_vcard_property_values(values_string):
    """
    Get the property values.

    @param values_string: Multiple value string
    @return: List of values (RFC 2426 page 12)
    """
    values = []

    # Strip line ending
    values_string = values_string[:-len(CRLF_CHARS)]

    subvalue_strings = split_unescaped(values_string, ';')
    for sub in subvalue_strings:
        values.append(get_vcard_property_subvalues(sub))

    return values


def validate_language_tag(language):
    """
    langval, as defined by RFC 1766 <http://tools.ietf.org/html/rfc1766>

    @param language: String

    Examples:
    >>> validate_language_tag('en')
    >>> validate_language_tag('-US') # Need primary tag
    Traceback (most recent call last):
    VCardFormatError: Invalid language: -us
    >>> validate_language_tag('en-') # Can't end with dash
    Traceback (most recent call last):
    VCardFormatError: Invalid language: en-
    >>> validate_language_tag('en-US')

    """
    language = language.lower() # Case insensitive

    if re.match(r'^([a-z]{1,8})(-[a-z]{1,8})*$', language) is None:
        raise VCardFormatError(
            MSG_INVALID_LANGUAGE_VALUE + ': %s' % language,
            {})

    # TODO: Extend to validate according to referenced ISO/RFC standards


def validate_x_name(name):
    """
    @param parameter: Single parameter name

    Examples:
    >>> validate_x_name('X-abc')
    >>> validate_x_name('X-' + ID_CHARS)
    >>> validate_x_name('X-') # Have to have more characters
    Traceback (most recent call last):
    VCardFormatError: Invalid X-name: X-
    >>> validate_x_name('') # Have to start with X-
    Traceback (most recent call last):
    VCardFormatError: Invalid X-name: 
    >>> validate_x_name('x-abc') # X must be upper case
    Traceback (most recent call last):
    VCardFormatError: Invalid X-name: x-abc
    >>> validate_x_name('foo') # Have to start with X-
    Traceback (most recent call last):
    VCardFormatError: Invalid X-name: foo
    """
    if re.match(r'^X-[' + ID_CHARS + ']+$', name) is None:
        raise VCardFormatError(MSG_INVALID_X_NAME + ': %s' % name, {})


def validate_ptext(text):
    """
    ptext, as described on page 28
    <http://tools.ietf.org/html/rfc2426#section-4>

    @param text: String

    Examples:
    >>> validate_ptext('')
    >>> validate_ptext(SAFE_CHARS)
    >>> validate_ptext(u'\u000B') #doctest: +ELLIPSIS
    Traceback (most recent call last):
    VCardFormatError: Invalid parameter value: ...
    """
    if re.match('^[' + SAFE_CHARS + ']*$', text) is None:
        raise VCardFormatError(MSG_INVALID_PARAM_VALUE + ': %s' % text, {})


def validate_quoted_string(text):
    """
    quoted-string, as described on page 28
    <http://tools.ietf.org/html/rfc2426#section-4>

    @param text: String

    Examples:
    >>> validate_quoted_string(DQUOTE_CHAR + QSAFE_CHARS[0] + DQUOTE_CHAR)
    >>> validate_quoted_string(DQUOTE_CHAR + DQUOTE_CHAR)
    Traceback (most recent call last):
    VCardFormatError: Invalid parameter value: ""
    >>> validate_quoted_string(DQUOTE_CHAR + QSAFE_CHARS[-1]*2 + DQUOTE_CHAR)
    Traceback (most recent call last):
    VCardFormatError: Invalid parameter value: "ÿÿ"
    """
    if re.match(
        r'^' + DQUOTE_CHAR + '[' + QSAFE_CHARS + ']' + DQUOTE_CHAR + '$',
        text) is None:
        raise VCardFormatError(MSG_INVALID_PARAM_VALUE + ': %s' % text, {})


def validate_param_value(text):
    """
    param-value, as described on page 28
    <http://tools.ietf.org/html/rfc2426#section-4>

    @param text: Single parameter value
    """
    try:
        validate_ptext(text)
    except VCardFormatError:
        try:
            validate_quoted_string(text)
        except VCardFormatError:
            raise VCardFormatError(MSG_INVALID_PARAM_VALUE + ': %s' % text, {})


def validate_text_parameter(parameter):
    """
    text-param, as described on page 35
    <http://tools.ietf.org/html/rfc2426#section-4>

    @param parameter: Single parameter, as returned by get_vcard_property_param
    """
    param_name = parameter[0].upper()
    param_values = parameter[1]

    if param_name == 'VALUE' and param_values != set(['ptext']):
        raise VCardFormatError(
            MSG_INVALID_PARAM_VALUE + ': %s' % param_values,
            {})
    elif param_name == 'LANGUAGE':
        if len(param_values) != 1:
            raise VCardFormatError(
                MSG_INVALID_PARAM_VALUE + ': %s' % param_values,
                {})
        validate_language_tag(param_values[0])
    else:
        validate_x_name(param_name)
        if len(param_values) != 1:
            raise VCardFormatError(
                MSG_INVALID_PARAM_VALUE + ': %s' % param_values,
                {})
        validate_param_value(param_values[0])


def validate_float(text):
    """
    float value, as described on page 10 of RFC 2425
    <http://tools.ietf.org/html/rfc2425#section-5.8.4>

    Examples:
    >>> validate_float('12')
    >>> validate_float('12.345')
    >>> validate_float('+12.345')
    >>> validate_float('-12.345')
    >>> validate_float('12.')
    Traceback (most recent call last):
    VCardFormatError: Invalid subvalue, expected float value: 12.
    >>> validate_float('foo')
    Traceback (most recent call last):
    VCardFormatError: Invalid subvalue, expected float value: foo
    >>> validate_float('++12.345')
    Traceback (most recent call last):
    VCardFormatError: Invalid subvalue, expected float value: ++12.345
    >>> validate_float('--12.345')
    Traceback (most recent call last):
    VCardFormatError: Invalid subvalue, expected float value: --12.345
    >>> validate_float('12.34.5')
    Traceback (most recent call last):
    VCardFormatError: Invalid subvalue, expected float value: 12.34.5
    """
    if re.match(r'^[+-]?\d+(\.\d+)?$', text) is None:
        raise VCardFormatError(
            MSG_INVALID_SUBVALUE + ', expected float value: %s' % text,
            {})


# pylint: disable-msg=R0912,R0915
def validate_vcard_property(prop):
    """
    Checks any property according to
    <http://tools.ietf.org/html/rfc2426#section-3> and
    <http://tools.ietf.org/html/rfc2426#section-4>. Checks are grouped by
    property to allow easy overview rather than a short function.

    @param property: Formatted property
    """
    property_name = prop['name'].upper()

    try:
        if property_name == 'FN':
            # <http://tools.ietf.org/html/rfc2426#section-3.1.1>
            if 'parameters' in prop:
                for parameter in prop['parameters'].items():
                    validate_text_parameter(parameter)
            if len(prop['values']) != 1:
                raise VCardFormatError(
                    MSG_INVALID_VALUE_COUNT + ': %d (expected 1)' % len(
                        prop['values']),
                    {})

        elif property_name == 'N':
            # <http://tools.ietf.org/html/rfc2426#section-3.1.2>
            if 'parameters' in prop:
                for parameter in prop['parameters'].items():
                    validate_text_parameter(parameter)
            if len(prop['values']) != 5:
                raise VCardFormatError(
                    MSG_INVALID_VALUE_COUNT + ': %d (expected 5)' % len(
                        prop['values']),
                    {})
            # Should names be split?
            for names in prop['values']:
                warnings.showwarning = _show_warning
                for name in names:
                    if name.find(SP_CHAR) != -1 and \
                           ''.join([''.join(names) \
                                    for names in prop['values']]) != name:
                        # Space in name
                        # Not just a single name
                        warnings.warn(
                            WARN_MULTIPLE_NAMES + ': %s' % name.encode('utf-8'))

        elif property_name == 'NICKNAME':
            # <http://tools.ietf.org/html/rfc2426#section-3.1.3>
            if 'parameters' in prop:
                for parameter in prop['parameters'].items():
                    validate_text_parameter(parameter)
            if len(prop['values']) != 1:
                raise VCardFormatError(
                    MSG_INVALID_VALUE_COUNT + ': %d (expected 1)' % len(
                        prop['values']),
                    {})

        elif property_name == 'PHOTO':
            # <http://tools.ietf.org/html/rfc2426#section-3.1.4>
            if not 'parameters' in prop:
                raise VCardFormatError(MSG_MISSING_PARAM, {})
            for param_name, param_values in prop['parameters'].items():
                if param_name.upper() == 'ENCODING':
                    if param_values != set(['b']):
                        raise VCardFormatError(
                            MSG_INVALID_PARAM_VALUE + ': %s' % param_values,
                            {})
                    if 'VALUE' in prop['parameters']:
                        raise VCardFormatError(
                            MSG_MISMATCH_PARAM  + ': %s and %s' % (
                                'ENCODING',
                                'VALUE'),
                            {})
                elif param_name.upper() == 'TYPE' and \
                       'ENCODING' not in prop['parameters']:
                    raise VCardFormatError(
                        MSG_MISSING_PARAM + ': %s' % 'ENCODING',
                        {})
                elif param_name.upper() == 'VALUE' and \
                     param_values != set(['uri']):
                    raise VCardFormatError(
                        MSG_INVALID_PARAM_VALUE + ': %s' % param_values,
                        {})
                elif param_name.upper() not in ['ENCODING', 'TYPE', 'VALUE']:
                    raise VCardFormatError(
                        MSG_INVALID_PARAM_NAME + ': %s' % param_name,
                        {})

        elif property_name == 'BDAY':
            # <http://tools.ietf.org/html/rfc2426#section-3.1.5>
            if 'parameters' in prop:
                raise VCardFormatError(
                    MSG_NON_EMPTY_PARAM + ': %s' % prop['parameters'],
                    {})
            if len(prop['values']) != 1:
                raise VCardFormatError(
                    MSG_INVALID_VALUE_COUNT + ': %d (expected 1)' % len(
                        prop['values']),
                    {})
            if len(prop['values'][0]) != 1:
                raise VCardFormatError(
                    MSG_INVALID_SUBVALUE_COUNT + ': %d (expected 1)' % len(
                        prop['values'][0]),
                    {})
            validate_date(prop['values'][0][0])

        elif property_name == 'ADR':
            # <http://tools.ietf.org/html/rfc2426#section-3.2.1>
            if len(prop['values']) != 7:
                raise VCardFormatError(
                    MSG_INVALID_VALUE_COUNT + ': %d (expected 7)' % len(
                        prop['values']),
                    {})
            if 'parameters' in prop:
                for param_name, param_values in prop['parameters'].items():
                    if param_name.upper() == 'TYPE':
                        for param_subvalue in param_values:
                            if param_subvalue not in [
                                'dom',
                                'intl',
                                'postal',
                                'parcel',
                                'home',
                                'work',
                                'pref']:
                                raise VCardFormatError(
                                    MSG_INVALID_PARAM_VALUE + \
                                    ': %s' % param_subvalue,
                                    {})
                        if param_values == set([
                            'intl',
                            'postal',
                            'parcel',
                            'work']):
                            warnings.warn(
                                WARN_DEFAULT_TYPE_VALUE + \
                                ': %s' % prop['values'])
                    else:
                        validate_text_parameter(parameter)

        elif property_name == 'LABEL':
            # <http://tools.ietf.org/html/rfc2426#section-3.2.2>
            if len(prop['values']) != 1:
                raise VCardFormatError(
                    MSG_INVALID_VALUE_COUNT + ': %d (expected 1)' % len(
                        prop['values']),
                    {})
            if 'parameters' in prop:
                for param_name, param_values in prop['parameters'].items():
                    if param_name.upper() == 'TYPE':
                        for param_subvalue in param_values:
                            if param_subvalue not in [
                                'dom',
                                'intl',
                                'postal',
                                'parcel',
                                'home',
                                'work',
                                'pref']:
                                raise VCardFormatError(
                                    MSG_INVALID_PARAM_VALUE + ': %s' % \
                                    param_subvalue,
                                    {})
                        if param_values == set([
                            'intl',
                            'postal',
                            'parcel',
                            'work']):
                            warnings.warn(
                                WARN_DEFAULT_TYPE_VALUE + ': %s' % \
                                prop['values'])
                    else:
                        validate_text_parameter(parameter)

        elif property_name == 'TEL':
            # <http://tools.ietf.org/html/rfc2426#section-3.3.1>
            if len(prop['values']) != 1:
                raise VCardFormatError(
                    MSG_INVALID_VALUE_COUNT + ': %d (expected 1)' % len(
                        prop['values']),
                    {})
            if 'parameters' in prop:
                for param_name, param_values in prop['parameters'].items():
                    if param_name.upper() == 'TYPE':
                        for param_subvalue in param_values:
                            if param_subvalue.lower() not in [
                                'home',
                                'msg',
                                'work',
                                'pref',
                                'voice',
                                'fax',
                                'cell',
                                'video',
                                'pager',
                                'bbs',
                                'modem',
                                'car',
                                'isdn',
                                'pcs']:
                                raise VCardFormatError(
                                    MSG_INVALID_PARAM_VALUE + \
                                    ': %s' % param_subvalue,
                                    {})
                        if set([value.lower() for value in param_values]) == \
                               set(['voice']):
                            warnings.warn(
                                WARN_DEFAULT_TYPE_VALUE + ': %s' % \
                                prop['values'])
                    else:
                        raise VCardFormatError(
                            MSG_INVALID_PARAM_NAME + ': %s' % param_name,
                            {})

        elif property_name == 'EMAIL':
            # <http://tools.ietf.org/html/rfc2426#section-3.3.2>
            if len(prop['values']) != 1:
                raise VCardFormatError(
                    MSG_INVALID_VALUE_COUNT + ': %d (expected 1)' % len(
                        prop['values']),
                    {})
            if 'parameters' in prop:
                for param_name, param_values in prop['parameters'].items():
                    if param_name.upper() == 'TYPE':
                        for param_subvalue in param_values:
                            if param_subvalue.lower() not in [
                                'internet',
                                'x400',
                                'pref',
                                'dom', # IANA registered address types?
                                'intl',
                                'postal',
                                'parcel',
                                'home',
                                'work']:
                                warnings.warn(
                                    WARN_INVALID_EMAIL_TYPE + \
                                    ': %s' % param_subvalue)
                        if set([value.lower() for value in param_values]) == \
                               set(['internet']):
                            warnings.warn(
                                WARN_DEFAULT_TYPE_VALUE + ': %s' % \
                                prop['values'])
                    else:
                        raise VCardFormatError(
                            MSG_INVALID_PARAM_NAME + ': %s' % param_name,
                            {})

        elif property_name == 'MAILER':
            # <http://tools.ietf.org/html/rfc2426#section-3.3.3>
            if 'parameters' in prop:
                raise VCardFormatError(
                    MSG_NON_EMPTY_PARAM + ': %s' % prop['parameters'],
                    {})
            if len(prop['values']) != 1:
                raise VCardFormatError(
                    MSG_INVALID_VALUE_COUNT + ': %d (expected 1)' % len(
                        prop['values']),
                    {})

        elif property_name == 'TZ':
            # <http://tools.ietf.org/html/rfc2426#section-3.4.1>
            if 'parameters' in prop:
                raise VCardFormatError(
                    MSG_NON_EMPTY_PARAM + ': %s' % prop['parameters'],
                    {})
            if len(prop['values']) != 1:
                raise VCardFormatError(
                    MSG_INVALID_VALUE_COUNT + ': %d (expected 1)' % len(
                        prop['values']),
                    {})
            if len(prop['values'][0]) != 1:
                raise VCardFormatError(
                    MSG_INVALID_SUBVALUE_COUNT + ': %d (expected 1)' % len(
                        prop['values'][0]),
                    {})
            value = prop['values'][0][0]
            validate_time_zone(value)

        elif property_name == 'GEO':
            # <http://tools.ietf.org/html/rfc2426#section-3.4.2>
            if 'parameters' in prop:
                raise VCardFormatError(
                    MSG_NON_EMPTY_PARAM + ': %s' % prop['parameters'],
                    {})
            if len(prop['values']) != 2:
                raise VCardFormatError(
                    MSG_INVALID_VALUE_COUNT + ': %d (expected 2)' % len(
                        prop['values']),
                    {})
            for value in prop['values']:
                if len(value) != 1:
                    raise VCardFormatError(
                        MSG_INVALID_SUBVALUE_COUNT + ': %d (expected 1)' % len(
                            prop['values'][0]),
                        {})
                validate_float(value[0])
    except VCardFormatError as error:
        error.context['property'] = property_name
        raise VCardFormatError(error.message, error.context)
# pylint: enable-msg=R0912,R0915


def get_vcard_property(property_line):
    """
    Get a single property.

    @param property_line: Single unfolded vCard line
    @return: Dictionary with name, parameters and values
    """
    prop = {}

    property_parts = split_unescaped(property_line, ':')
    if len(property_parts) < 2:
        raise VCardFormatError(
            MSG_MISSING_VALUE_STRING + ': %s' % property_line,
            {})
    elif len(property_parts) > 2:
        # Merge - Colon doesn't have to be escaped in values
        property_parts[1] = ':'.join(property_parts[1:])
        property_parts = property_parts[:2]
    property_string, values_string = property_parts

    # Split property name and property parameters
    property_name_and_params = split_unescaped(property_string, ';')

    prop['name'] = property_name_and_params.pop(0)

    # String validation
    if not prop['name'].upper() in ALL_PROPERTIES and not re.match(
        '^X-[' + ID_CHARS + ']+$',
        prop['name'],
        re.IGNORECASE):
        raise VCardFormatError(
            MSG_INVALID_PROPERTY_NAME + ': %s' % prop['name'],
            {})

    try:
        if len(property_name_and_params) != 0:
            prop['parameters'] = get_vcard_property_params(
                ';'.join(property_name_and_params))
        prop['values'] = get_vcard_property_values(values_string)

        # Validate
        validate_vcard_property(prop)
    except VCardFormatError as error:
        # Add parameter name to error
        error.context['property_line'] = property_line
        raise VCardFormatError(error.message, error.context)

    return prop


def get_vcard_properties(lines):
    """
    Get the properties for each line. RFC 2426 pages 28, 29.

    @param properties: List of unfolded vCard lines
    @return: List of properties, for simplicity. AFAIK sequence doesn't matter
    and duplicates add no information, but ignoring this to make sure vCard
    output looks like the original.
    """
    properties = []
    for index in range(len(lines)):
        property_line = lines[index]
        if property_line != CRLF_CHARS:
            try:
                properties.append(get_vcard_property(property_line))
            except VCardFormatError as error:
                error.context['vcard_line'] = index
                raise VCardFormatError(error.message, error.context)

    for mandatory_property in MANDATORY_PROPERTIES:
        if mandatory_property not in [
            prop['name'].upper() for prop in properties]:
            raise VCardFormatError(
                MSG_MISSING_PROPERTY + ': %s' % mandatory_property,
                {'property': mandatory_property})

    return properties


# pylint: disable-msg=R0903
class VCard():
    """Container for structured and unstructured vCard contents."""
    def __init__(self, text, filename = None):
        """
        Create vCard object from text string. Includes text (the entire
        unprocessed vCard), group (optional prefix on each line) and properties.

        @param text: String containing a single vCard
        """
        if text == '':
            raise VCardFormatError(
                MSG_EMPTY_VCARD,
                {'vcard_line': 0, 'file_line': 0})

        self.text = text

        self.filename = filename

        lines = unfold_vcard_lines(self.text.splitlines(True))

        # Groups
        self.group = get_vcard_group(lines)
        lines = remove_vcard_groups(lines, self.group)

        # Properties
        self.properties = get_vcard_properties(lines)

    def __str__(self):
        return self.text
# pylint: enable-msg=R0903


def validate_file(filename, verbose = False):
    """
    Create object for each vCard in a file, and show the error output.

    @param filename: Path to file
    @param verbose: Verbose mode
    @return: Debugging output from creating vCards
    """
    if filename == '-':
        file_pointer = sys.stdin
    else:
        file_pointer = codecs.open(filename, 'r', 'utf-8')

    contents = file_pointer.read().splitlines(True)

    vcard_text = ''
    result = ''
    try:
        for index in range(len(contents)):
            line = contents[index]
            vcard_text += line

            if line == CRLF_CHARS:
                try:
                    vcard = VCard(vcard_text, filename)
                    vcard_text = ''
                    if verbose:
                        print(vcard)
                except VCardFormatError as error:
                    error.context['path'] = filename
                    error.context['file_line'] = index
                    raise VCardFormatError(error.message, error.context)

    except VCardFormatError as error:
        result += unicode(error.__str__())

    if vcard_text != '' and result == '':
        result += 'Could not process entire %s - %i lines remain' % (
            filename,
            len(vcard_text.splitlines()))

    if result == '':
        return None
    return result


# pylint: disable-msg=W0231
class Usage(Exception):
    """Raise in case of invalid parameters."""
    def __init__(self, message):
        self.message = message
# pylint: enable-msg=W0231


def main(argv = None):
    """Argument handling."""

    if argv is None:
        argv = sys.argv

    # Defaults
    verbose = False

    try:
        try:
            opts, args = getopt.getopt(
                argv[1:],
                'v',
                ['verbose'])
        except getopt.GetoptError, err:
            raise Usage(err.message)

        if len(opts) != 0:
            for option in opts[0]:
                if option in ('-v', '--verbose'):
                    verbose = True
                else:
                    raise Usage('Unhandled option %s' % option)

        if not args:
            raise Usage(__doc__)

    except Usage, err:
        sys.stderr.write(err.message + '\n')
        return 2

    for filename in args:
        result = validate_file(filename, verbose)
        if result is not None:
            print(result.encode('utf-8') + '\n')


if __name__ == '__main__':
    sys.exit(main())
