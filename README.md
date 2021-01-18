[![Donate via PayPal][donate-image]][donate-link]
[![Discord][discord-image]][discord-link]
[![Build][github-ci-image]][github-ci-link]
[![Coverage Status][codecov-image]][codecov-link]
[![PyPI Version][pypi-image]][pypi-link]
[![PyPI - Python Version][python-image]][pypi-link]
![License][license-image-mit]

# UniProps

The main purpose of this library is simply to provide Unicode Property strings for regular expression character groups.
This is done simply by specifying the Unicode Property and parameters (if relevant). The strings are formatted in such
a way so that they can easily be inserted into a regular expression character group with appropriate characters escaped.

UniProps was originally written for and shipped as part of `backrefs`, a wrapper around regular expressions that can
provide features such as Unicode Properties in Python's Re. The logic was broken out into this separate package as we
developed a second package (`wcmatch`: an alternative `fnmatch` and `glob` library) which also required the ability to
retrieve POSIX regular expression strings for certain character groups. This library feeds both of the aforementioned
packages with the appropriate Unicode Properties.

While UniProps is specifically designed for the previously mentioned packages, others are free to use it if they find it
helpful, but it is very opinionated and tailored specifically to work with how we are using it in `wcmatch` and
`backrefs`.

# API

It is important to note that the library is built for how it is used. Often the input mirrors how properties are
specified in regex, Unicode Properties.

Names of properties and values must be lowercase with spaces, underscores, and hyphens stripped out. For instance, the
`General Category` property name is fed in as `generalcategory` (or the alias `gc`). The library doesn't currently
process and format the inputs for the user in this manner, so the user must do this before passing them in.

Regardless of whether the strings are needed for a byte string or Unicode string, the properties are always returned as
Unicode. This is because the libraries it was designed for are assembling the regular expressions together as Unicode
strings and then converting them to byte strings, when needed, by encoding them using `latin-1`.

## Get POSIX property

```py
def get_posix_property(value, mode=POSIX):
    """Retrieve the posix category."""
```

This retrieves a property by its POSIX name. This does not use the locale and instead either returns the property in the
C locale or as a Unicode property only. Valid properties are: `alnum`, `alpha`, `ascii`, `blank`, `cntrl`, `digit`,
`graph`, `lower`, `print`, `punct`, `space`, `upper`, and `xdigit`.

A property can be inverted by adding the prefix `^`, in which case it will return all characters not within the
specified property.

Available modes are:

1. `POSIX`: acquire the POSIX property returning characters based on the POSIX definition (which are ASCII characters)
   specified within the Unicode range. For example, `alnum` is defined as `[a-zA-Z0-9]`. Because this returns strings in
   the Unicode range, the inverse of `alnum` `(^alnum)` would extend all the way to `\U0010ffff`.

    ```py
    >>> uniprops.get_posix_property("alnum", mode=uniprops.POSIX)
    '0-9A-Za-z'
    >>> uniprops.get_posix_property("^alnum", mode=uniprops.POSIX)
    '\x00-/:-@\\[-`{-\U0010ffff'
    ```

2. `POSIX_ASCII`: acquire the POSIX property returning characters based on the POSIX definition (which are ASCII
   characters) specified within the range of byte strings range. For example, `alnum` is defined as `[a-zA-Z0-9]`.
   Because this returns strings in the range of byte strings, the inverse of `alnum` `(^alnum)` would only extend to
   `\xff`. It is recommended to encode these to byte string by using the encoding `latin-1`.

    ```py
    >>> uniprops.get_posix_property("alnum", mode=uniprops.POSIX_BYTES).encode('latin-1')
    b'0-9A-Za-z'
    >>> uniprops.get_posix_property("^alnum", mode=uniprops.POSIX_BYTES).encode('latin-1')
    b'\x00-/:-@\\[-`{-\xff'
    ```

3. `POSIX_UNICODE`: acquire the POSIX property returning characters based on Unicode definition which are Unicode
   characters specified in the Unicode range. For instance, `alnum` is equivalent to the regular expression of
   `\p{L&}\p{Nd}` (in regular expression engines that support Unicode properties).

## Get Unicode Property

```py
def get_unicode_property(prop, value=None, limit_ascii=False):
    """Retrieve the Unicode category from the table."""
```

This retrieves a Unicode property by its name and its value. If the result string is desired to be within a byte
string's range, set `limit_ascii` to `True`. Remember, to format for a byte string, simply encode as `latin-1`.

To use, simply specify the Unicode property and its value.

```py
uniprops.get_unicode_property('gc', 'l')
```

Setting the `prop` with a prefix of `^` will get the inverse result:

```py
uniprops.get_unicode_property('^gc', 'l')
```

Binary properties don't really need a `value` as the value is implied to be "true" unless it is prefixed with `^` and is
then implied to be false. But you can optionally specify `true`, `yes`, `y`, or `t` for an explicit "true" or `false`,
`no`, `f`, or `n` for a "false".

The following are equivalent

```py
uniprops.get_unicode_property('alphabetic')
uniprops.get_unicode_property('alphabetic', 'true')
```

There are a few exceptions to the rules above. Like in Perl regular expressions, you can pass script extension and
block property value names, and they will be detected appropriately. Same goes for values under the general category
property. Properties that only provide a single parameter like this are evaluated in the order: general category,
scripts, blocks, and binary properties.

As an example, these are equivalent:

```py
uniprops.get_unicode_property('gc', 'l')
uniprops.get_unicode_property('l')
```

When passing a value as the property name, you can invert the result by placing the `^` directly on the value.

```py
uniprops.get_unicode_property('^gc', 'l')
uniprops.get_unicode_property('^l')
```

These are also equivalent

```py
uniprops.get_unicode_property('blk', 'basiclatin')
uniprops.get_unicode_property('basiclatin')
```

The last exception are properties specified with the `Is` and `In` prefix. We model the 3rd party
[regex](https://bitbucket.org/mrabarnett/mrab-regex/src/hg/) library for Python with this support. `Is` will assume the
property is a script extension or binary property while `In` will assume a `block` property. Generally this usage is
discouraged as future Unicode versions may break such behavior with naming conflicts, but currently we support this.

These are all equivalent:

```py
uniprops.get_unicode_property('inbasiclatin')
uniprops.get_unicode_property('blk', 'basiclatin')
uniprops.get_unicode_property('basiclatin')
```

# License

Released under the MIT license.

[github-ci-image]: https://github.com/facelessuser/uniprops/workflows/build/badge.svg?branch=master&event=push
[github-ci-link]: https://github.com/facelessuser/uniprops/actions?query=workflow%3Abuild+branch%3Amaster
[discord-image]: https://img.shields.io/discord/678289859768745989?logo=discord&logoColor=aaaaaa&color=mediumpurple&labelColor=333333
[discord-link]:https://discord.gg/TWs8Tgr
[codecov-image]: https://img.shields.io/codecov/c/github/facelessuser/uniprops/master.svg?logo=codecov&logoColor=aaaaaa&labelColor=333333
[codecov-link]: https://codecov.io/github/facelessuser/uniprops
[pypi-image]: https://img.shields.io/pypi/v/uniprops.svg?logo=pypi&logoColor=aaaaaa&labelColor=333333
[pypi-link]: https://pypi.python.org/pypi/uniprops
[python-image]: https://img.shields.io/pypi/pyversions/uniprops?logo=python&logoColor=aaaaaa&labelColor=333333
[license-image-mit]: https://img.shields.io/badge/license-MIT-blue.svg?labelColor=333333
[donate-image]: https://img.shields.io/badge/Donate-PayPal-3fabd1?logo=paypal
[donate-link]: https://www.paypal.me/facelessuser
