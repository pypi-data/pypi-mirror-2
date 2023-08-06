#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: GenericWrapper for ODF content objects
# Created: 03.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import etree, register_class, wrap

def safelen(text):
    # can handle `None` as input
    return len(text) if text else 0

@register_class
class GenericWrapper:
    TAG = 'GenericWrapper'

    def __init__(self, xmlnode=None):
        if xmlnode is not None:
            self.xmlnode = xmlnode
        else:
            self.xmlnode = etree.Element(self.TAG)

    def __iter__(self):
        return map(wrap, self.xmlnode.iterchildren())

    def __len__(self):
        """ Get count of children """
        return len(self.xmlnode)

    @property
    def text(self):
        return self.xmlnode.text
    @text.setter
    def text(self, value):
        self.xmlnode.text = value

    @property
    def tail(self):
        return self.xmlnode.tail
    @tail.setter
    def tail(self, value):
        self.xmlnode.tail = value

    @property
    def kind(self):
        return self.__class__.__name__

    ## Index operations

    def __getitem__(self, index):
        return self.get_child(index)
    def __setitem__(self, index, element):
        self.set_child(index, element)
    def __delitem__(self, index):
        self.del_child(index)

    def index(self, child):
        """ Get numeric index of `child`.

        :param GenericWrapper child: get index for this child
        :returns: int
        """
        return self.xmlnode.index(child.xmlnode)

    def insert(self, index, child):
        """ Insert child at position `index`.

        :param int index: insert position for child
        :param GenericWrapper child: child to insert
        :returns: GenericWrapper child
        """
        self.xmlnode.insert(int(index), child.xmlnode)
        return child # pass through

    def get_child(self, index):
        """ Get children at `index` as wrapped object.

        :param int index: child position
        :returns: GenericWrapper
        """
        xmlelement = self.xmlnode[int(index)]
        return wrap(xmlelement)

    def set_child(self, index, element):
        """ Set (replace) the child at position `index` by element.

        :param int index: child position
        :param GenericWrapper element: new child node
        """
        found = self.xmlnode[int(index)]
        self.xmlnode.replace(found, element.xmlnode)

    def del_child(self, index):
        """ Delete child at position `index`.

        :param int index: child position
        """
        del self.xmlnode[int(index)]

    def filter(self, kind):
        """ Filter child nodes by `kind`. """
        return filter(lambda e: e.kind == kind, iter(self))

    def findall(self, tag):
        """ Find all subelements by xml-tag (in Clark Notation). """
        return map(wrap, self.xmlnode.findall(tag))

    ## Attribute access for the xmlnode element

    def get_attr(self, key, default=None):
        """ Get the `key` attribute value of the xmlnode element or `default`
        if `key` does not exist.

        :param str key: name of key
        :param default: default value if `key` not found
        :return: str
        """
        value = self.xmlnode.get(key)
        if value is None:
            value = default
        return value

    def set_attr(self, key, value):
        """ Set the `key` attribute of the xmlnode element to `value`.

        :param str key: name of key
        :param value: value for key
        """
        if value:
            self.xmlnode.set(key, str(value))
        else:
            raise ValueError(value)

    ## List operations

    def append(self, child):
        """ Append `child` as to node.

        :param GenericWrapper child: child to append
        """
        self.xmlnode.append(child.xmlnode)
        return child # pass through

    def insert_before(self, target, child):
        """ Insert `child` before to `target`.

        :param GenericWrapper target: target node
        :param GenericWrapper child: new object
        :returns: GenericWrapper child
        """
        position = self.index(target)
        self.insert(position, child)
        return child # pass through

    def remove(self, child):
        """ Remove `child` object from node.

        :param GenericWrapper child: child to remove
        """
        self.xmlnode.remove(child.xmlnode)

    def clear(self):
        """ Remove all content from node. """
        self.xmlnode.clear()

    ## production code

    @property
    def textlen(self):
        """ Returns the character count of the plain text content as int. """
        # default implementation, does not respect child elements
        return safelen(self.xmlnode.text)

    def plaintext(self):
        """ Get content of node as plain (unformatted) text string. """
        # default implementation, does not respect child elements
        text = self.xmlnode.text
        return text if text else ""

