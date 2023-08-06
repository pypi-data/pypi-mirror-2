# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0
#
# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
# the License for the specific language governing rights and
# limitations under the License.
#
# The Original Code is Pika.
#
# The Initial Developers of the Original Code are LShift Ltd, Cohesive
# Financial Technologies LLC, and Rabbit Technologies Ltd.  Portions
# created before 22-Nov-2008 00:00:00 GMT by LShift Ltd, Cohesive
# Financial Technologies LLC, or Rabbit Technologies Ltd are Copyright
# (C) 2007-2008 LShift Ltd, Cohesive Financial Technologies LLC, and
# Rabbit Technologies Ltd.
#
# Portions created by LShift Ltd are Copyright (C) 2007-2009 LShift
# Ltd. Portions created by Cohesive Financial Technologies LLC are
# Copyright (C) 2007-2009 Cohesive Financial Technologies
# LLC. Portions created by Rabbit Technologies Ltd are Copyright (C)
# 2007-2009 Rabbit Technologies Ltd.
#
# Portions created by Tony Garnock-Jones are Copyright (C) 2009-2010
# LShift Ltd and Tony Garnock-Jones.
#
# All Rights Reserved.
#
# Contributor(s): ______________________________________.
#
# Alternatively, the contents of this file may be used under the terms
# of the GNU General Public License Version 2 or later (the "GPL"), in
# which case the provisions of the GPL are applicable instead of those
# above. If you wish to allow use of your version of this file only
# under the terms of the GPL, and not to allow others to use your
# version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the
# notice and other provisions required by the GPL. If you do not
# delete the provisions above, a recipient may use your version of
# this file under the terms of any one of the MPL or the GPL.
#
# ***** END LICENSE BLOCK *****

from __future__ import nested_scopes

import sys
sys.path.append("../rabbitmq-codegen")  # in case we're next to an experimental revision
sys.path.append("codegen")              # in case we're building from a distribution package

from amqp_codegen import *
import re

DRIVER_METHODS = {
    "Exchange.Declare": ["Exchange.DeclareOk"],
    "Exchange.Delete": ["Exchange.DeleteOk"],
    "Queue.Declare": ["Queue.DeclareOk"],
    "Queue.Bind": ["Queue.BindOk"],
    "Queue.Purge": ["Queue.PurgeOk"],
    "Queue.Delete": ["Queue.DeleteOk"],
    "Queue.Unbind": ["Queue.UnbindOk"],
    "Basic.Qos": ["Basic.QosOk"],
    "Basic.Get": ["Basic.GetOk", "Basic.GetEmpty"],
    "Basic.Ack": [],
    "Basic.Reject": [],
    "Basic.Recover": ["Basic.RecoverOk"],
    "Basic.RecoverAsync": [],
    "Tx.Select": ["Tx.SelectOk"],
    "Tx.Commit": ["Tx.CommitOk"],
    "Tx.Rollback": ["Tx.RollbackOk"]
    }


def fieldvalue(v):
    if isinstance(v, unicode):
        return repr(v.encode('ascii'))
    else:
        return repr(v)


def normalize_separators(s):
    s = s.replace('-', '_')
    s = s.replace(' ', '_')
    return s


def pyize(s):
    s = normalize_separators(s)
    if s in ('global', 'class'):
        s += '_'
    return s


def camel(s):
    return normalize_separators(s).title().replace('_', '')


AmqpMethod.structName = lambda m: camel(m.klass.name) + '.' + camel(m.name)
AmqpClass.structName = lambda c: camel(c.name) + "Properties"


def constantName(s):
    return '_'.join(re.split('[- ]', s.upper()))


def flagName(c, f):
    if c:
        return c.structName() + '.' + constantName('flag_' + f.name)
    else:
        return constantName('flag_' + f.name)


def generate(specPath):
    spec = AmqpSpec(specPath)

    def genSingleDecode(prefix, cLvalue, unresolved_domain):
        type = spec.resolveDomain(unresolved_domain)
        if type == 'shortstr':
            print prefix + "length = struct.unpack_from('B', encoded, offset)[0]"
            print prefix + "offset += 1"
            print prefix + "%s = encoded[offset:offset + length]" % (cLvalue,)
            print prefix + "offset += length"
        elif type == 'longstr':
            print prefix + "length = struct.unpack_from('>I', encoded, offset)[0]"
            print prefix + "offset += 4"
            print prefix + "%s = encoded[offset:offset + length]" % (cLvalue,)
            print prefix + "offset += length"
        elif type == 'octet':
            print prefix + "%s = struct.unpack_from('B', encoded, offset)[0]" % (cLvalue,)
            print prefix + "offset += 1"
        elif type == 'short':
            print prefix + "%s = struct.unpack_from('>H', encoded, offset)[0]" % (cLvalue,)
            print prefix + "offset += 2"
        elif type == 'long':
            print prefix + "%s = struct.unpack_from('>I', encoded, offset)[0]" % (cLvalue,)
            print prefix + "offset += 4"
        elif type == 'longlong':
            print prefix + "%s = struct.unpack_from('>Q', encoded, offset)[0]" % (cLvalue,)
            print prefix + "offset += 8"
        elif type == 'timestamp':
            print prefix + "%s = struct.unpack_from('>Q', encoded, offset)[0]" % (cLvalue,)
            print prefix + "offset += 8"
        elif type == 'bit':
            raise "Can't decode bit in genSingleDecode"
        elif type == 'table':
            print prefix + "(%s, offset) = pika.table.decode_table(encoded, offset)" % \
                  (cLvalue,)
        else:
            raise "Illegal domain in genSingleDecode", type

    def genSingleEncode(prefix, cValue, unresolved_domain):
        type = spec.resolveDomain(unresolved_domain)
        if type == 'shortstr':
            print prefix + "pieces.append(struct.pack('B', len(%s)))" % (cValue,)
            print prefix + "pieces.append(%s)" % (cValue,)
        elif type == 'longstr':
            print prefix + "pieces.append(struct.pack('>I', len(%s)))" % (cValue,)
            print prefix + "pieces.append(%s)" % (cValue,)
        elif type == 'octet':
            print prefix + "pieces.append(struct.pack('B', %s))" % (cValue,)
        elif type == 'short':
            print prefix + "pieces.append(struct.pack('>H', %s))" % (cValue,)
        elif type == 'long':
            print prefix + "pieces.append(struct.pack('>I', %s))" % (cValue,)
        elif type == 'longlong':
            print prefix + "pieces.append(struct.pack('>Q', %s))" % (cValue,)
        elif type == 'timestamp':
            print prefix + "pieces.append(struct.pack('>Q', %s))" % (cValue,)
        elif type == 'bit':
            raise "Can't encode bit in genSingleEncode"
        elif type == 'table':
            print prefix + "pika.table.encode_table(pieces, %s)" % (cValue,)
        else:
            raise "Illegal domain in genSingleEncode", type

    def genDecodeMethodFields(m):
        print "        def decode(self, encoded, offset=0):"
        bitindex = None
        for f in m.arguments:
            if spec.resolveDomain(f.domain) == 'bit':
                if bitindex is None:
                    bitindex = 0
                if bitindex >= 8:
                    bitindex = 0
                if not bitindex:
                    print "            bit_buffer = struct.unpack_from('B', encoded, offset)[0]"
                    print "            offset += 1"
                print "            self.%s = (bit_buffer & (1 << %d)) != 0" % \
                      (pyize(f.name), bitindex)
                bitindex += 1
            else:
                bitindex = None
                genSingleDecode("            ", "self.%s" % (pyize(f.name),), f.domain)
        print "            return self"
        print

    def genDecodeProperties(c):
        print "    def decode(self, encoded, offset=0):"
        print "        flags = 0"
        print "        flagword_index = 0"
        print "        while True:"
        print "            partial_flags = struct.unpack_from('>H', encoded, offset)[0]"
        print "            offset += 2"
        print "            flags = flags | (partial_flags << (flagword_index * 16))"
        print "            if not (partial_flags & 1):"
        print "                break"
        print "            flagword_index += 1"
        for f in c.fields:
            if spec.resolveDomain(f.domain) == 'bit':
                print "        self.%s = (flags & %s) != 0" % (pyize(f.name), flagName(c, f))
            else:
                print "        if flags & %s:" % (flagName(c, f),)
                genSingleDecode("            ", "self.%s" % (pyize(f.name),), f.domain)
                print "        else:"
                print "            self.%s = None" % (pyize(f.name),)
        print "        return self"
        print

    def genEncodeMethodFields(m):
        print "        def encode(self):"
        print "            pieces = list()"
        bitindex = None

        def finishBits():
            if bitindex is not None:
                print "            pieces.append(struct.pack('B', bit_buffer))"
        for f in m.arguments:
            if spec.resolveDomain(f.domain) == 'bit':
                if bitindex is None:
                    bitindex = 0
                    print "            bit_buffer = 0"
                if bitindex >= 8:
                    finishBits()
                    print "            bit_buffer = 0"
                    bitindex = 0
                print "            if self.%s:" % pyize(f.name)
                print "                bit_buffer = bit_buffer | (1 << %d)" % \
                    bitindex
                bitindex += 1
            else:
                finishBits()
                bitindex = None
                genSingleEncode("            ", "self.%s" % (pyize(f.name),), f.domain)
        finishBits()
        print "            return pieces"
        print

    def genEncodeProperties(c):
        print "    def encode(self):"
        print "        pieces = list()"
        print "        flags = 0"
        for f in c.fields:
            if spec.resolveDomain(f.domain) == 'bit':
                print "        if self.%s: flags = flags | %s" % (pyize(f.name), flagName(c, f))
            else:
                print "        if self.%s is not None:" % (pyize(f.name),)
                print "            flags = flags | %s" % (flagName(c, f),)
                genSingleEncode("            ", "self.%s" % (pyize(f.name),), f.domain)
        print "        flag_pieces = list()"
        print "        while True:"
        print "            remainder = flags >> 16"
        print "            partial_flags = flags & 0xFFFE"
        print "            if remainder != 0:"
        print "                partial_flags |= 1"
        print "            flag_pieces.append(struct.pack('>H', partial_flags))"
        print "            flags = remainder"
        print "            if not flags:"
        print "                break"
        print "        return flag_pieces + pieces"
        print

    def fieldDeclList(fields):
        return ''.join([", %s=%s" % (pyize(f.name), fieldvalue(f.defaultvalue)) for f in fields])

    def fieldInitList(prefix, fields):
        if fields:
            return ''.join(["%sself.%s = %s\n" % (prefix, pyize(f.name), pyize(f.name)) \
                            for f in fields])
        else:
            return '%spass\n' % (prefix,)

    print '# Autogenerated code by codegen.py, do not edit'
    print
    print 'import struct'
    print 'import pika.object'
    print 'import pika.table as table'
    print
    print "PROTOCOL_VERSION = (%d, %d, %d)" % (spec.major, spec.minor,
                                               spec.revision)
    print "PORT = %d" % spec.port
    print

    for c, v, cls in spec.constants:
        print "%s = %s" % (constantName(c), v)
    print

    for c in spec.allClasses():
        print
        print 'class %s(pika.object.Class):' % (camel(c.name),)
        print
        print "    INDEX = 0x%.04X  # %d" % (c.index, c.index)
        print "    NAME = %s" % (fieldvalue(camel(c.name)),)
        print

        for m in c.allMethods():
            print '    class %s(pika.object.Method):' % (camel(m.name),)
            print
            methodid = m.klass.index << 16 | m.index
            print "        INDEX = 0x%.08X  # %d, %d; %d" % \
                  (methodid,
                   m.klass.index,
                   m.index,
                   methodid)
            print "        NAME = %s" % (fieldvalue(m.structName(),))
            print
            print "        def __init__(self%s):" % (fieldDeclList(m.arguments),)
            print fieldInitList('            ', m.arguments)
            print "        @property"
            print "        def synchronous(self):"
            print "            return %s" % m.isSynchronous
            print
            genDecodeMethodFields(m)
            genEncodeMethodFields(m)

    for c in spec.allClasses():
        if c.fields:
            print
            print 'class %s(pika.object.Properties):' % (c.structName(),)
            print
            print "    CLASS = %s" % (camel(c.name),)
            print "    INDEX = 0x%.04X  # %d" % (c.index, c.index)
            print "    NAME = %s" % (fieldvalue(c.structName(),))
            print

            index = 0
            if c.fields:
                for f in c.fields:
                    if index % 16 == 15:
                        index += 1
                    shortnum = index / 16
                    partialindex = 15 - (index % 16)
                    bitindex = shortnum * 16 + partialindex
                    print '    %s = (1 << %d)' % (flagName(None, f), bitindex)
                    index += 1
                print

            print "    def __init__(self%s):" % (fieldDeclList(c.fields),)
            print fieldInitList('        ', c.fields)
            genDecodeProperties(c)
            genEncodeProperties(c)

    print "methods = {"
    print ',\n'.join(["    0x%08X: %s" % (m.klass.index << 16 | m.index, m.structName()) \
                      for m in spec.allMethods()])
    print "}"
    print

    print "props = {"
    print ',\n'.join(["    0x%04X: %s" % (c.index, c.structName()) \
                      for c in spec.allClasses() \
                      if c.fields])
    print "}"
    print
    print

    print "def has_content(methodNumber):"
    print
    for m in spec.allMethods():
        if m.hasContent:
            print '    if methodNumber == %s.INDEX:' % m.structName()
            print '        return True'
    print "    return False"
    print
    print

    print "class DriverMixin(object):"

    for m in spec.allMethods():
        if m.structName() in DRIVER_METHODS:
            acceptable_replies = DRIVER_METHODS[m.structName()]
            print
            anchor = pyize("%s.%s" % (m.klass.name, m.name))
            if m.isSynchronous:

                #Synchronous events have a CPS callback parameter
                print "    def %s(self, callback=None%s):" % \
                      (pyize("%s_%s" % (m.klass.name, m.name)),
                      fieldDeclList(m.arguments))
                print '        """'
                print '        Implements the %s AMQP command. For context and usage:' % m.structName()
                print
                print '          http://www.rabbitmq.com/amqp-0-9-1-quickref.html#%s' % anchor
                print
                print '        This is a synchronous method that will not allow other commands to be'
                print '        send to the AMQP broker until it has completed. It is recommended to'
                print '        pass in a parameter to callback to be notified when this command has'
                print '        completed.'
                print '        """'
                print
                print "        return self.transport.rpc(%s(%s), callback," % \
                       (m.structName(),
                       ', '.join(["%s=%s" % (pyize(f.name), pyize(f.name))
                       for f in m.arguments]))
                print "                                  [%s])" % \
                      ', '.join(acceptable_replies)

            else:
                print "    def %s(self%s):" % \
                      (pyize("%s_%s" % (m.klass.name, m.name)),
                      fieldDeclList(m.arguments))
                print '        """'
                print '        Implements the %s.%s AMQP command. For context and usage:' % (m.klass.name, m.name)
                print
                print '          http://www.rabbitmq.com/amqp-0-9-1-quickref.html#%s' % anchor
                print '        """'
                print
                print "        return self.transport.rpc(%s(%s))" % \
                       (m.structName(),
                       ', '.join(["%s=%s" % (pyize(f.name), pyize(f.name))
                       for f in m.arguments]))

if __name__ == "__main__":
    do_main_dict({"spec": generate})
