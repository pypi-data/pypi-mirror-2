# -*- encoding: utf-8 -*-
#
# Copyright (c) 2001 Richard Jones, richard@bofh.asn.au.
# This module is free software, and you may redistribute it and/or modify
# under the same terms as Python, so long as this copyright message and
# disclaimer are retained in their original form.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# $Id: test_mailgw.py,v 1.96 2008-08-19 01:40:59 richard Exp $

# TODO: test bcc

import unittest, tempfile, os, shutil, errno, imp, sys, difflib, rfc822, time

from cStringIO import StringIO

if not os.environ.has_key('SENDMAILDEBUG'):
    os.environ['SENDMAILDEBUG'] = 'mail-test.log'
SENDMAILDEBUG = os.environ['SENDMAILDEBUG']

from roundup import mailgw, i18n, roundupdb
from roundup.mailgw import MailGW, Unauthorized, uidFromAddress, \
    parseContent, IgnoreLoop, IgnoreBulk, MailUsageError, MailUsageHelp
from roundup import init, instance, password, rfc2822, __version__
from roundup.anypy.sets_ import set

#import db_test_base
import memorydb

class Message(rfc822.Message):
    """String-based Message class with equivalence test."""
    def __init__(self, s):
        rfc822.Message.__init__(self, StringIO(s.strip()))

    def __eq__(self, other):
        return (self.dict == other.dict and
                self.fp.read() == other.fp.read())

class Tracker(object):
    def open(self, journaltag):
        return self.db

class DiffHelper:
    def compareMessages(self, new, old):
        """Compare messages for semantic equivalence."""
        new, old = Message(new), Message(old)

        # all Roundup-generated messages have "Precedence: bulk"
        old['Precedence'] = 'bulk'

        # don't try to compare the date
        del new['date'], old['date']

        if not new == old:
            res = []

            replace = {}
            for key in new.keys():
                if key.startswith('from '):
                    # skip the unix from line
                    continue
                if key.lower() == 'x-roundup-version':
                    # version changes constantly, so handle it specially
                    if new[key] != __version__:
                        res.append('  %s: %r != %r' % (key, __version__,
                            new[key]))
                elif key.lower() == 'content-type' and 'boundary=' in new[key]:
                    # handle mime messages
                    newmime = new[key].split('=',1)[-1].strip('"')
                    oldmime = old.get(key, '').split('=',1)[-1].strip('"')
                    replace ['--' + newmime] = '--' + oldmime
                    replace ['--' + newmime + '--'] = '--' + oldmime + '--'
                elif new.get(key, '') != old.get(key, ''):
                    res.append('  %s: %r != %r' % (key, old.get(key, ''),
                        new.get(key, '')))

            body_diff = self.compareStrings(new.fp.read(), old.fp.read(),
                replace=replace)
            if body_diff:
                res.append('')
                res.extend(body_diff)

            if res:
                res.insert(0, 'Generated message not correct (diff follows, expected vs. actual):')
                raise AssertionError, '\n'.join(res)

    def compareStrings(self, s2, s1, replace={}):
        '''Note the reversal of s2 and s1 - difflib.SequenceMatcher wants
           the first to be the "original" but in the calls in this file,
           the second arg is the original. Ho hum.
           Do replacements over the replace dict -- used for mime boundary
        '''
        l1 = s1.strip().split('\n')
        l2 = [replace.get(i,i) for i in s2.strip().split('\n')]
        if l1 == l2:
            return
        s = difflib.SequenceMatcher(None, l1, l2)
        res = []
        for value, s1s, s1e, s2s, s2e in s.get_opcodes():
            if value == 'equal':
                for i in range(s1s, s1e):
                    res.append('  %s'%l1[i])
            elif value == 'delete':
                for i in range(s1s, s1e):
                    res.append('- %s'%l1[i])
            elif value == 'insert':
                for i in range(s2s, s2e):
                    res.append('+ %s'%l2[i])
            elif value == 'replace':
                for i, j in zip(range(s1s, s1e), range(s2s, s2e)):
                    res.append('- %s'%l1[i])
                    res.append('+ %s'%l2[j])

        return res

class MailgwTestCase(unittest.TestCase, DiffHelper):
    count = 0
    schema = 'classic'
    def setUp(self):
        self.old_translate_ = mailgw._
        roundupdb._ = mailgw._ = i18n.get_translation(language='C').gettext
        MailgwTestCase.count = MailgwTestCase.count + 1

        # and open the database / "instance"
        self.db = memorydb.create('admin')
        self.instance = Tracker()
        self.instance.db = self.db
        self.instance.config = self.db.config
        self.instance.MailGW = MailGW

        self.chef_id = self.db.user.create(username='Chef',
            address='chef@bork.bork.bork', realname='Bork, Chef', roles='User')
        self.richard_id = self.db.user.create(username='richard',
            address='richard@test.test', roles='User')
        self.mary_id = self.db.user.create(username='mary',
            address='mary@test.test', roles='User', realname='Contrary, Mary')
        self.john_id = self.db.user.create(username='john',
            address='john@test.test', roles='User', realname='John Doe',
            alternate_addresses='jondoe@test.test\njohn.doe@test.test')
        self.rgg_id = self.db.user.create(username='rgg',
            address='rgg@test.test', roles='User')

    def tearDown(self):
        roundupdb._ = mailgw._ = self.old_translate_
        if os.path.exists(SENDMAILDEBUG):
            os.remove(SENDMAILDEBUG)
        self.db.close()

    def _create_mailgw(self, message, args=()):
        class MailGW(self.instance.MailGW):
            def handle_message(self, message):
                return self._handle_message(message)
        handler = MailGW(self.instance, args)
        handler.db = self.db
        return handler

    def _handle_mail(self, message, args=()):
        handler = self._create_mailgw(message, args)
        handler.trapExceptions = 0
        return handler.main(StringIO(message))

    def _get_mail(self):
        f = open(SENDMAILDEBUG)
        try:
            return f.read()
        finally:
            f.close()

    def testEmptyMessage(self):
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing...

''')
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.issue.get(nodeid, 'title'), 'Testing...')

    def testMessageWithFromInIt(self):
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing...

From here to there!
''')
        assert not os.path.exists(SENDMAILDEBUG)
        msgid = self.db.issue.get(nodeid, 'messages')[0]
        self.assertEqual(self.db.msg.get(msgid, 'content'), 'From here to there!')

    def testNoMessageId(self):
        self.instance.config['MAIL_DOMAIN'] = 'example.com'
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Subject: [issue] Testing...

Hi there!
''')
        assert not os.path.exists(SENDMAILDEBUG)
        msgid = self.db.issue.get(nodeid, 'messages')[0]
        messageid = self.db.msg.get(msgid, 'messageid')
        x1, x2 = messageid.split('@')
        self.assertEqual(x2, 'example.com>')
        x = x1.split('.')[-1]
        self.assertEqual(x, 'issueNone')
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: [issue%(nodeid)s] Testing...

Just a test reply
'''%locals())
        msgid = self.db.issue.get(nodeid, 'messages')[-1]
        messageid = self.db.msg.get(msgid, 'messageid')
        x1, x2 = messageid.split('@')
        self.assertEqual(x2, 'example.com>')
        x = x1.split('.')[-1]
        self.assertEqual(x, "issue%s"%nodeid)

    def testOptions(self):
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id>
Reply-To: chef@bork.bork.bork
Subject: [issue] Testing...

Hi there!
''', (('-C', 'issue'), ('-S', 'status=chatting;priority=critical')))
        self.assertEqual(self.db.issue.get(nodeid, 'status'), '3')
        self.assertEqual(self.db.issue.get(nodeid, 'priority'), '1')

    def testOptionsMulti(self):
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id>
Reply-To: chef@bork.bork.bork
Subject: [issue] Testing...

Hi there!
''', (('-C', 'issue'), ('-S', 'status=chatting'), ('-S', 'priority=critical')))
        self.assertEqual(self.db.issue.get(nodeid, 'status'), '3')
        self.assertEqual(self.db.issue.get(nodeid, 'priority'), '1')

    def testOptionClass(self):
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id>
Reply-To: chef@bork.bork.bork
Subject: [issue] Testing... [status=chatting;priority=critical]

Hi there!
''', (('-c', 'issue'),))
        self.assertEqual(self.db.issue.get(nodeid, 'title'), 'Testing...')
        self.assertEqual(self.db.issue.get(nodeid, 'status'), '3')
        self.assertEqual(self.db.issue.get(nodeid, 'priority'), '1')

    def doNewIssue(self):
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing...

This is a test submission of a new issue.
''')
        assert not os.path.exists(SENDMAILDEBUG)
        l = self.db.issue.get(nodeid, 'nosy')
        l.sort()
        self.assertEqual(l, [self.chef_id, self.richard_id])
        return nodeid

    def testNewIssue(self):
        self.doNewIssue()

    def testNewIssueNosy(self):
        self.instance.config.ADD_AUTHOR_TO_NOSY = 'yes'
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing...

This is a test submission of a new issue.
''')
        assert not os.path.exists(SENDMAILDEBUG)
        l = self.db.issue.get(nodeid, 'nosy')
        l.sort()
        self.assertEqual(l, [self.chef_id, self.richard_id])

    def testAlternateAddress(self):
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: John Doe <john.doe@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing...

This is a test submission of a new issue.
''')
        userlist = self.db.user.list()
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(userlist, self.db.user.list(),
            "user created when it shouldn't have been")

    def testNewIssueNoClass(self):
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Message-Id: <dummy_test_message_id>
Subject: Testing...

This is a test submission of a new issue.
''')
        assert not os.path.exists(SENDMAILDEBUG)

    def testNewIssueAuthMsg(self):
        # TODO: fix the damn config - this is apalling
        self.db.config.MESSAGES_TO_AUTHOR = 'yes'
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing... [nosy=mary; assignedto=richard]

This is a test submission of a new issue.
''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, mary@test.test, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, mary@test.test, richard@test.test
From: "Bork, Chef" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: unread
Content-Transfer-Encoding: quoted-printable


New submission from Bork, Chef <chef@bork.bork.bork>:

This is a test submission of a new issue.

----------
assignedto: richard
messages: 1
nosy: Chef, mary, richard
status: unread
title: Testing...

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testNewIssueNoAuthorInfo(self):
        self.db.config.MAIL_ADD_AUTHORINFO = 'no'
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing... [nosy=mary; assignedto=richard]

This is a test submission of a new issue.
''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, mary@test.test, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: mary@test.test, richard@test.test
From: "Bork, Chef" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: unread
Content-Transfer-Encoding: quoted-printable

This is a test submission of a new issue.

----------
assignedto: richard
messages: 1
nosy: Chef, mary, richard
status: unread
title: Testing...

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testNewIssueNoAuthorEmail(self):
        self.db.config.MAIL_ADD_AUTHOREMAIL = 'no'
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing... [nosy=mary; assignedto=richard]

This is a test submission of a new issue.
''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, mary@test.test, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: mary@test.test, richard@test.test
From: "Bork, Chef" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: unread
Content-Transfer-Encoding: quoted-printable

New submission from Bork, Chef:

This is a test submission of a new issue.

----------
assignedto: richard
messages: 1
nosy: Chef, mary, richard
status: unread
title: Testing...

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    multipart_msg = '''From: mary <mary@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...
Content-Type: multipart/mixed; boundary="bxyzzy"
Content-Disposition: inline


--bxyzzy
Content-Type: multipart/alternative; boundary="bCsyhTFzCvuiizWE"
Content-Disposition: inline

--bCsyhTFzCvuiizWE
Content-Type: text/plain; charset=us-ascii
Content-Disposition: inline

test attachment first text/plain

--bCsyhTFzCvuiizWE
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="first.dvi"
Content-Transfer-Encoding: base64

SnVzdCBhIHRlc3QgAQo=

--bCsyhTFzCvuiizWE
Content-Type: text/plain; charset=us-ascii
Content-Disposition: inline

test attachment second text/plain

--bCsyhTFzCvuiizWE
Content-Type: text/html
Content-Disposition: inline

<html>
to be ignored.
</html>

--bCsyhTFzCvuiizWE--

--bxyzzy
Content-Type: multipart/alternative; boundary="bCsyhTFzCvuiizWF"
Content-Disposition: inline

--bCsyhTFzCvuiizWF
Content-Type: text/plain; charset=us-ascii
Content-Disposition: inline

test attachment third text/plain

--bCsyhTFzCvuiizWF
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="second.dvi"
Content-Transfer-Encoding: base64

SnVzdCBhIHRlc3QK

--bCsyhTFzCvuiizWF--

--bxyzzy--
'''

    multipart_msg_latin1 = '''From: mary <mary@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...
Content-Type: multipart/alternative; boundary=001485f339f8f361fb049188dbba


--001485f339f8f361fb049188dbba
Content-Type: text/plain; charset=ISO-8859-1
Content-Transfer-Encoding: quoted-printable

umlaut =E4=F6=FC=C4=D6=DC=DF

--001485f339f8f361fb049188dbba
Content-Type: text/html; charset=ISO-8859-1
Content-Transfer-Encoding: quoted-printable

<html>umlaut =E4=F6=FC=C4=D6=DC=DF</html>

--001485f339f8f361fb049188dbba--
'''

    multipart_msg_rfc822 = '''From: mary <mary@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...
Content-Type: multipart/mixed; boundary=001485f339f8f361fb049188dbba

This is a multi-part message in MIME format.
--001485f339f8f361fb049188dbba
Content-Type: text/plain; charset=ISO-8859-15
Content-Transfer-Encoding: 7bit

First part: Text

--001485f339f8f361fb049188dbba
Content-Type: message/rfc822; name="Fwd: Original email subject.eml"
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="Fwd: Original email subject.eml"

Message-Id: <followup_dummy_id_2>
In-Reply-To: <dummy_test_message_id_2>
MIME-Version: 1.0
Subject: Fwd: Original email subject
Date: Mon, 23 Aug 2010 08:23:33 +0200
Content-Type: multipart/alternative; boundary="090500050101020406060002"

This is a multi-part message in MIME format.
--090500050101020406060002
Content-Type: text/plain; charset=ISO-8859-15; format=flowed
Content-Transfer-Encoding: 7bit

some text in inner email
========================

--090500050101020406060002
Content-Type: text/html; charset=ISO-8859-15
Content-Transfer-Encoding: 7bit

<html>
some text in inner email
========================
</html>

--090500050101020406060002--

--001485f339f8f361fb049188dbba--
'''

    def testMultipartKeepAlternatives(self):
        self.doNewIssue()
        self._handle_mail(self.multipart_msg)
        messages = self.db.issue.get('1', 'messages')
        messages.sort()
        msg = self.db.msg.getnode (messages[-1])
        assert(len(msg.files) == 5)
        names = {0 : 'first.dvi', 4 : 'second.dvi'}
        content = {3 : 'test attachment third text/plain\n',
                   4 : 'Just a test\n'}
        for n, id in enumerate (msg.files):
            f = self.db.file.getnode (id)
            self.assertEqual(f.name, names.get (n, 'unnamed'))
            if n in content :
                self.assertEqual(f.content, content [n])
        self.assertEqual(msg.content, 'test attachment second text/plain')

    def testMultipartKeepFiles(self):
        self.doNewIssue()
        self._handle_mail(self.multipart_msg)
        messages = self.db.issue.get('1', 'messages')
        messages.sort()
        msg = self.db.msg.getnode (messages[-1])
        assert(len(msg.files) == 5)
        issue = self.db.issue.getnode ('1')
        assert(len(issue.files) == 5)
        names = {0 : 'first.dvi', 4 : 'second.dvi'}
        content = {3 : 'test attachment third text/plain\n',
                   4 : 'Just a test\n'}
        for n, id in enumerate (msg.files):
            f = self.db.file.getnode (id)
            self.assertEqual(f.name, names.get (n, 'unnamed'))
            if n in content :
                self.assertEqual(f.content, content [n])
        self.assertEqual(msg.content, 'test attachment second text/plain')
        self._handle_mail('''From: mary <mary@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id2>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...

This ist a message without attachment
''')
        issue = self.db.issue.getnode ('1')
        assert(len(issue.files) == 5)
        self.assertEqual(issue.files, ['1', '2', '3', '4', '5'])

    def testMultipartDropAlternatives(self):
        self.doNewIssue()
        self.db.config.MAILGW_IGNORE_ALTERNATIVES = True
        self._handle_mail(self.multipart_msg)
        messages = self.db.issue.get('1', 'messages')
        messages.sort()
        msg = self.db.msg.getnode (messages[-1])
        assert(len(msg.files) == 2)
        names = {1 : 'second.dvi'}
        content = {0 : 'test attachment third text/plain\n',
                   1 : 'Just a test\n'}
        for n, id in enumerate (msg.files):
            f = self.db.file.getnode (id)
            self.assertEqual(f.name, names.get (n, 'unnamed'))
            if n in content :
                self.assertEqual(f.content, content [n])
        self.assertEqual(msg.content, 'test attachment second text/plain')

    def testMultipartCharsetUTF8NoAttach(self):
        c = 'umlaut \xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f'
        self.doNewIssue()
        self.db.config.NOSY_MAX_ATTACHMENT_SIZE = 0
        self._handle_mail(self.multipart_msg_latin1)
        messages = self.db.issue.get('1', 'messages')
        messages.sort()
        msg = self.db.msg.getnode (messages[-1])
        assert(len(msg.files) == 1)
        name = 'unnamed'
        content = '<html>' + c + '</html>\n'
        for n, id in enumerate (msg.files):
            f = self.db.file.getnode (id)
            self.assertEqual(f.name, name)
            self.assertEqual(f.content, content)
        self.assertEqual(msg.content, c)
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: "Contrary, Mary" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
X-Roundup-Issue-Files: unnamed
Content-Transfer-Encoding: quoted-printable


Contrary, Mary <mary@test.test> added the comment:

umlaut =C3=A4=C3=B6=C3=BC=C3=84=C3=96=C3=9C=C3=9F
File 'unnamed' not attached - you can download it from http://tracker.examp=
le/cgi-bin/roundup.cgi/bugs/file1.

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testMultipartCharsetLatin1NoAttach(self):
        c = 'umlaut \xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f'
        self.doNewIssue()
        self.db.config.NOSY_MAX_ATTACHMENT_SIZE = 0
        self.db.config.MAIL_CHARSET = 'iso-8859-1'
        self._handle_mail(self.multipart_msg_latin1)
        messages = self.db.issue.get('1', 'messages')
        messages.sort()
        msg = self.db.msg.getnode (messages[-1])
        assert(len(msg.files) == 1)
        name = 'unnamed'
        content = '<html>' + c + '</html>\n'
        for n, id in enumerate (msg.files):
            f = self.db.file.getnode (id)
            self.assertEqual(f.name, name)
            self.assertEqual(f.content, content)
        self.assertEqual(msg.content, c)
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: text/plain; charset="iso-8859-1"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: "Contrary, Mary" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
X-Roundup-Issue-Files: unnamed
Content-Transfer-Encoding: quoted-printable


Contrary, Mary <mary@test.test> added the comment:

umlaut =E4=F6=FC=C4=D6=DC=DF
File 'unnamed' not attached - you can download it from http://tracker.examp=
le/cgi-bin/roundup.cgi/bugs/file1.

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testMultipartCharsetUTF8AttachFile(self):
        c = 'umlaut \xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f'
        self.doNewIssue()
        self._handle_mail(self.multipart_msg_latin1)
        messages = self.db.issue.get('1', 'messages')
        messages.sort()
        msg = self.db.msg.getnode (messages[-1])
        assert(len(msg.files) == 1)
        name = 'unnamed'
        content = '<html>' + c + '</html>\n'
        for n, id in enumerate (msg.files):
            f = self.db.file.getnode (id)
            self.assertEqual(f.name, name)
            self.assertEqual(f.content, content)
        self.assertEqual(msg.content, c)
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: multipart/mixed; boundary="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: "Contrary, Mary" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
X-Roundup-Issue-Files: unnamed
Content-Transfer-Encoding: quoted-printable


--utf-8
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: quoted-printable


Contrary, Mary <mary@test.test> added the comment:

umlaut =C3=A4=C3=B6=C3=BC=C3=84=C3=96=C3=9C=C3=9F

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
--utf-8
Content-Type: text/html
MIME-Version: 1.0
Content-Transfer-Encoding: base64
Content-Disposition: attachment;
 filename="unnamed"

PGh0bWw+dW1sYXV0IMOkw7bDvMOEw5bDnMOfPC9odG1sPgo=

--utf-8--
''')

    def testMultipartCharsetLatin1AttachFile(self):
        c = 'umlaut \xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f'
        self.doNewIssue()
        self.db.config.MAIL_CHARSET = 'iso-8859-1'
        self._handle_mail(self.multipart_msg_latin1)
        messages = self.db.issue.get('1', 'messages')
        messages.sort()
        msg = self.db.msg.getnode (messages[-1])
        assert(len(msg.files) == 1)
        name = 'unnamed'
        content = '<html>' + c + '</html>\n'
        for n, id in enumerate (msg.files):
            f = self.db.file.getnode (id)
            self.assertEqual(f.name, name)
            self.assertEqual(f.content, content)
        self.assertEqual(msg.content, c)
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: multipart/mixed; boundary="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: "Contrary, Mary" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
X-Roundup-Issue-Files: unnamed
Content-Transfer-Encoding: quoted-printable


--utf-8
MIME-Version: 1.0
Content-Type: text/plain; charset="iso-8859-1"
Content-Transfer-Encoding: quoted-printable


Contrary, Mary <mary@test.test> added the comment:

umlaut =E4=F6=FC=C4=D6=DC=DF

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
--utf-8
Content-Type: text/html
MIME-Version: 1.0
Content-Transfer-Encoding: base64
Content-Disposition: attachment;
 filename="unnamed"

PGh0bWw+dW1sYXV0IMOkw7bDvMOEw5bDnMOfPC9odG1sPgo=

--utf-8--
''')

    def testMultipartRFC822(self):
        self.doNewIssue()
        self._handle_mail(self.multipart_msg_rfc822)
        messages = self.db.issue.get('1', 'messages')
        messages.sort()
        msg = self.db.msg.getnode (messages[-1])
        assert(len(msg.files) == 1)
        name = "Fwd: Original email subject.eml"
        for n, id in enumerate (msg.files):
            f = self.db.file.getnode (id)
            self.assertEqual(f.name, name)
        self.assertEqual(msg.content, 'First part: Text')
        self.compareMessages(self._get_mail(),
'''TO: chef@bork.bork.bork, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: "Contrary, Mary" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
X-Roundup-Issue-Files: Fwd: Original email subject.eml
Content-Transfer-Encoding: quoted-printable


--utf-8
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: quoted-printable


Contrary, Mary <mary@test.test> added the comment:

First part: Text

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
--utf-8
Content-Type: message/rfc822
MIME-Version: 1.0
Content-Disposition: attachment;
 filename="Fwd: Original email subject.eml"

Message-Id: <followup_dummy_id_2>
In-Reply-To: <dummy_test_message_id_2>
MIME-Version: 1.0
Subject: Fwd: Original email subject
Date: Mon, 23 Aug 2010 08:23:33 +0200
Content-Type: multipart/alternative; boundary="090500050101020406060002"

This is a multi-part message in MIME format.
--090500050101020406060002
Content-Type: text/plain; charset=ISO-8859-15; format=flowed
Content-Transfer-Encoding: 7bit

some text in inner email
========================

--090500050101020406060002
Content-Type: text/html; charset=ISO-8859-15
Content-Transfer-Encoding: 7bit

<html>
some text in inner email
========================
</html>

--090500050101020406060002--

--utf-8--
''')

    def testMultipartRFC822Unpack(self):
        self.doNewIssue()
        self.db.config.MAILGW_UNPACK_RFC822 = True
        self._handle_mail(self.multipart_msg_rfc822)
        messages = self.db.issue.get('1', 'messages')
        messages.sort()
        msg = self.db.msg.getnode (messages[-1])
        self.assertEqual(len(msg.files), 2)
        t = 'some text in inner email\n========================\n'
        content = {0 : t, 1 : '<html>\n' + t + '</html>\n'}
        for n, id in enumerate (msg.files):
            f = self.db.file.getnode (id)
            self.assertEqual(f.name, 'unnamed')
            if n in content :
                self.assertEqual(f.content, content [n])
        self.assertEqual(msg.content, 'First part: Text')

    def testSimpleFollowup(self):
        self.doNewIssue()
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: mary <mary@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...

This is a second followup
''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: "Contrary, Mary" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


Contrary, Mary <mary@test.test> added the comment:

This is a second followup

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testFollowup(self):
        self.doNewIssue()

        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing... [assignedto=mary; nosy=+john]

This is a followup
''')
        l = self.db.issue.get('1', 'nosy')
        l.sort()
        self.assertEqual(l, [self.chef_id, self.richard_id, self.mary_id,
            self.john_id])

        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, john@test.test, mary@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, john@test.test, mary@test.test
From: richard <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


richard <richard@test.test> added the comment:

This is a followup

----------
assignedto:  -> mary
nosy: +john, mary
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testFollowupNoSubjectChange(self):
        self.db.config.MAILGW_SUBJECT_UPDATES_TITLE = 'no'
        self.doNewIssue()

        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Wrzlbrmft... [assignedto=mary; nosy=+john]

This is a followup
''')
        l = self.db.issue.get('1', 'nosy')
        l.sort()
        self.assertEqual(l, [self.chef_id, self.richard_id, self.mary_id,
            self.john_id])

        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, john@test.test, mary@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, john@test.test, mary@test.test
From: richard <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


richard <richard@test.test> added the comment:

This is a followup

----------
assignedto:  -> mary
nosy: +john, mary
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')
        self.assertEqual(self.db.issue.get('1','title'), 'Testing...')

    def testFollowupExplicitSubjectChange(self):
        self.doNewIssue()

        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Wrzlbrmft... [assignedto=mary; nosy=+john; title=new title]

This is a followup
''')
        l = self.db.issue.get('1', 'nosy')
        l.sort()
        self.assertEqual(l, [self.chef_id, self.richard_id, self.mary_id,
            self.john_id])

        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, john@test.test, mary@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] new title
To: chef@bork.bork.bork, john@test.test, mary@test.test
From: richard <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


richard <richard@test.test> added the comment:

This is a followup

----------
assignedto:  -> mary
nosy: +john, mary
status: unread -> chatting
title: Testing... -> new title

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testNosyGeneration(self):
        self.db.issue.create(title='test')

        # create a nosy message
        msg = self.db.msg.create(content='This is a test',
            author=self.richard_id, messageid='<dummy_test_message_id>')
        self.db.journaltag = 'richard'
        l = self.db.issue.create(title='test', messages=[msg],
            nosy=[self.chef_id, self.mary_id, self.john_id])

        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, john@test.test, mary@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue2] test
To: chef@bork.bork.bork, john@test.test, mary@test.test
From: richard <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: unread
Content-Transfer-Encoding: quoted-printable


New submission from richard <richard@test.test>:

This is a test

----------
messages: 1
nosy: Chef, john, mary, richard
status: unread
title: test

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue2>
_______________________________________________________________________
''')

    def testPropertyChangeOnly(self):
        self.doNewIssue()
        oldvalues = self.db.getnode('issue', '1').copy()
        oldvalues['assignedto'] = None
        # reconstruct old behaviour: This would reuse the
        # database-handle from the doNewIssue above which has committed
        # as user "Chef". So we close and reopen the db as that user.
        #self.db.close() actually don't close 'cos this empties memorydb
        self.db = self.instance.open('Chef')
        self.db.issue.set('1', assignedto=self.chef_id)
        self.db.commit()
        self.db.issue.nosymessage('1', None, oldvalues)

        new_mail = ""
        for line in self._get_mail().split("\n"):
            if "Message-Id: " in line:
                continue
            if "Date: " in line:
                continue
            new_mail += line+"\n"

        self.compareMessages(new_mail, """
FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: "Bork, Chef" <issue_tracker@your.tracker.email.domain.example>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: unread
X-Roundup-Version: 1.3.3
In-Reply-To: <dummy_test_message_id>
MIME-Version: 1.0
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
Content-Transfer-Encoding: quoted-printable


Change by Bork, Chef <chef@bork.bork.bork>:


----------
assignedto:  -> Chef

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
""")


    #
    # FOLLOWUP TITLE MATCH
    #
    def testFollowupTitleMatch(self):
        self.doNewIssue()
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
Subject: Re: Testing... [assignedto=mary; nosy=+john]

This is a followup
''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, john@test.test, mary@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, john@test.test, mary@test.test
From: richard <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


richard <richard@test.test> added the comment:

This is a followup

----------
assignedto:  -> mary
nosy: +john, mary
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testFollowupTitleMatchMultiRe(self):
        nodeid1 = self.doNewIssue()
        nodeid2 = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
Subject: Re: Testing... [assignedto=mary; nosy=+john]

This is a followup
''')

        nodeid3 = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup2_dummy_id>
Subject: Ang: Re: Testing...

This is a followup
''')
        self.assertEqual(nodeid1, nodeid2)
        self.assertEqual(nodeid1, nodeid3)

    def testFollowupTitleMatchNever(self):
        nodeid = self.doNewIssue()
        self.db.config.MAILGW_SUBJECT_CONTENT_MATCH = 'never'
        self.assertNotEqual(self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
Subject: Re: Testing...

This is a followup
'''), nodeid)

    def testFollowupTitleMatchNeverInterval(self):
        nodeid = self.doNewIssue()
        # force failure of the interval
        time.sleep(2)
        self.db.config.MAILGW_SUBJECT_CONTENT_MATCH = 'creation 00:00:01'
        self.assertNotEqual(self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
Subject: Re: Testing...

This is a followup
'''), nodeid)


    def testFollowupTitleMatchInterval(self):
        nodeid = self.doNewIssue()
        self.db.config.MAILGW_SUBJECT_CONTENT_MATCH = 'creation +1d'
        self.assertEqual(self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
Subject: Re: Testing...

This is a followup
'''), nodeid)


    def testFollowupNosyAuthor(self):
        self.doNewIssue()
        self.db.config.ADD_AUTHOR_TO_NOSY = 'yes'
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: john@test.test
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...

This is a followup
''')

        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: John Doe <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


John Doe <john@test.test> added the comment:

This is a followup

----------
nosy: +john
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________

''')

    def testFollowupNosyRecipients(self):
        self.doNewIssue()
        self.db.config.ADD_RECIPIENTS_TO_NOSY = 'yes'
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard@test.test
To: issue_tracker@your.tracker.email.domain.example
Cc: john@test.test
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...

This is a followup
''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork
From: richard <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


richard <richard@test.test> added the comment:

This is a followup

----------
nosy: +john
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________

''')

    def testFollowupNosyAuthorAndCopy(self):
        self.doNewIssue()
        self.db.config.ADD_AUTHOR_TO_NOSY = 'yes'
        self.db.config.MESSAGES_TO_AUTHOR = 'yes'
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: john@test.test
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...

This is a followup
''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, john@test.test, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, john@test.test, richard@test.test
From: John Doe <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


John Doe <john@test.test> added the comment:

This is a followup

----------
nosy: +john
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________

''')

    def testFollowupNoNosyAuthor(self):
        self.doNewIssue()
        self.instance.config.ADD_AUTHOR_TO_NOSY = 'no'
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: john@test.test
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...

This is a followup
''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: John Doe <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


John Doe <john@test.test> added the comment:

This is a followup

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________

''')

    def testFollowupNoNosyRecipients(self):
        self.doNewIssue()
        self.instance.config.ADD_RECIPIENTS_TO_NOSY = 'no'
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard@test.test
To: issue_tracker@your.tracker.email.domain.example
Cc: john@test.test
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...

This is a followup
''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork
From: richard <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


richard <richard@test.test> added the comment:

This is a followup

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________

''')

    def testFollowupEmptyMessage(self):
        self.doNewIssue()

        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing... [assignedto=mary; nosy=+john]

''')
        l = self.db.issue.get('1', 'nosy')
        l.sort()
        self.assertEqual(l, [self.chef_id, self.richard_id, self.mary_id,
            self.john_id])

        # should be no file created (ie. no message)
        assert not os.path.exists(SENDMAILDEBUG)

    def testFollowupEmptyMessageNoSubject(self):
        self.doNewIssue()

        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] [assignedto=mary; nosy=+john]

''')
        l = self.db.issue.get('1', 'nosy')
        l.sort()
        self.assertEqual(l, [self.chef_id, self.richard_id, self.mary_id,
            self.john_id])

        # should be no file created (ie. no message)
        assert not os.path.exists(SENDMAILDEBUG)

    def testNosyRemove(self):
        self.doNewIssue()

        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing... [nosy=-richard]

''')
        l = self.db.issue.get('1', 'nosy')
        l.sort()
        self.assertEqual(l, [self.chef_id])

        # NO NOSY MESSAGE SHOULD BE SENT!
        assert not os.path.exists(SENDMAILDEBUG)

    def testNewUserAuthor(self):
        self.db.commit()
        l = self.db.user.list()
        l.sort()
        message = '''Content-Type: text/plain;
  charset="iso-8859-1"
From: fubar <fubar@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing...

This is a test submission of a new issue.
'''
        self.db.security.role['anonymous'].permissions=[]
        anonid = self.db.user.lookup('anonymous')
        self.db.user.set(anonid, roles='Anonymous')
        try:
            self._handle_mail(message)
        except Unauthorized, value:
            body_diff = self.compareMessages(str(value), """
You are not a registered user.

Unknown address: fubar@bork.bork.bork
""")
            assert not body_diff, body_diff
        else:
            raise AssertionError, "Unathorized not raised when handling mail"

        # Add Web Access role to anonymous, and try again to make sure
        # we get a "please register at:" message this time.
        p = [
            self.db.security.getPermission('Register', 'user'),
            self.db.security.getPermission('Web Access', None),
        ]
        self.db.security.role['anonymous'].permissions=p
        try:
            self._handle_mail(message)
        except Unauthorized, value:
            body_diff = self.compareMessages(str(value), """
You are not a registered user. Please register at:

http://tracker.example/cgi-bin/roundup.cgi/bugs/user?template=register

...before sending mail to the tracker.

Unknown address: fubar@bork.bork.bork
""")
            assert not body_diff, body_diff
        else:
            raise AssertionError, "Unathorized not raised when handling mail"

        # Make sure list of users is the same as before.
        m = self.db.user.list()
        m.sort()
        self.assertEqual(l, m)

        # now with the permission
        p = [
            self.db.security.getPermission('Register', 'user'),
            self.db.security.getPermission('Email Access', None),
        ]
        self.db.security.role['anonymous'].permissions=p
        self._handle_mail(message)
        m = self.db.user.list()
        m.sort()
        self.assertNotEqual(l, m)

    def testNewUserAuthorEncodedName(self):
        l = set(self.db.user.list())
        # From: name has Euro symbol in it
        message = '''Content-Type: text/plain;
  charset="iso-8859-1"
From: =?utf8?b?SOKCrGxsbw==?= <fubar@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing...

This is a test submission of a new issue.
'''
        p = [
            self.db.security.getPermission('Register', 'user'),
            self.db.security.getPermission('Email Access', None),
            self.db.security.getPermission('Create', 'issue'),
            self.db.security.getPermission('Create', 'msg'),
        ]
        self.db.security.role['anonymous'].permissions = p
        self._handle_mail(message)
        m = set(self.db.user.list())
        new = list(m - l)[0]
        name = self.db.user.get(new, 'realname')
        self.assertEquals(name, 'H€llo')

    def testUnknownUser(self):
        l = set(self.db.user.list())
        message = '''Content-Type: text/plain;
  charset="iso-8859-1"
From: Nonexisting User <nonexisting@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing nonexisting user...

This is a test submission of a new issue.
'''
        handler = self._create_mailgw(message)
        # we want a bounce message:
        handler.trapExceptions = 1
        ret = handler.main(StringIO(message))
        self.compareMessages(self._get_mail(),
'''FROM: Roundup issue tracker <roundup-admin@your.tracker.email.domain.example>
TO: nonexisting@bork.bork.bork
From nobody Tue Jul 14 12:04:11 2009
Content-Type: multipart/mixed; boundary="===============0639262320=="
MIME-Version: 1.0
Subject: Failed issue tracker submission
To: nonexisting@bork.bork.bork
From: Roundup issue tracker <roundup-admin@your.tracker.email.domain.example>
Date: Tue, 14 Jul 2009 12:04:11 +0000
Precedence: bulk
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Version: 1.4.8
MIME-Version: 1.0

--===============0639262320==
Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit



You are not a registered user. Please register at:

http://tracker.example/cgi-bin/roundup.cgi/bugs/user?template=register

...before sending mail to the tracker.

Unknown address: nonexisting@bork.bork.bork

--===============0639262320==
Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

Content-Type: text/plain;
  charset="iso-8859-1"
From: Nonexisting User <nonexisting@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing nonexisting user...

This is a test submission of a new issue.

--===============0639262320==--
''')

    def testEnc01(self):
        self.db.user.set(self.mary_id,
            realname='\xe4\xf6\xfc\xc4\xd6\xdc\xdf, Mary'.decode
            ('latin-1').encode('utf-8'))
        self.doNewIssue()
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: mary <mary@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...
Content-Type: text/plain;
        charset="iso-8859-1"
Content-Transfer-Encoding: quoted-printable

A message with encoding (encoded oe =F6)

''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: =?utf-8?b?w6TDtsO8w4TDlsOcw58sIE1hcnk=?=
 <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


=C3=A4=C3=B6=C3=BC=C3=84=C3=96=C3=9C=C3=9F, Mary <mary@test.test> added the=
 comment:

A message with encoding (encoded oe =C3=B6)

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testEncNonUTF8(self):
        self.doNewIssue()
        self.instance.config.EMAIL_CHARSET = 'iso-8859-1'
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: mary <mary@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...
Content-Type: text/plain;
        charset="iso-8859-1"
Content-Transfer-Encoding: quoted-printable

A message with encoding (encoded oe =F6)

''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: text/plain; charset="iso-8859-1"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: "Contrary, Mary" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


Contrary, Mary <mary@test.test> added the comment:

A message with encoding (encoded oe =F6)

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')


    def testMultipartEnc01(self):
        self.doNewIssue()
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: mary <mary@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...
Content-Type: multipart/mixed;
        boundary="----_=_NextPart_000_01"

This message is in MIME format. Since your mail reader does not understand
this format, some or all of this message may not be legible.

------_=_NextPart_000_01
Content-Type: text/plain;
        charset="iso-8859-1"
Content-Transfer-Encoding: quoted-printable

A message with first part encoded (encoded oe =F6)

''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork, richard@test.test
From: "Contrary, Mary" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


Contrary, Mary <mary@test.test> added the comment:

A message with first part encoded (encoded oe =C3=B6)

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testContentDisposition(self):
        self.doNewIssue()
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: mary <mary@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [issue1] Testing...
Content-Type: multipart/mixed; boundary="bCsyhTFzCvuiizWE"
Content-Disposition: inline


--bCsyhTFzCvuiizWE
Content-Type: text/plain; charset=us-ascii
Content-Disposition: inline

test attachment binary

--bCsyhTFzCvuiizWE
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="main.dvi"
Content-Transfer-Encoding: base64

SnVzdCBhIHRlc3QgAQo=

--bCsyhTFzCvuiizWE--
''')
        messages = self.db.issue.get('1', 'messages')
        messages.sort()
        file = self.db.file.getnode (self.db.msg.get(messages[-1], 'files')[0])
        self.assertEqual(file.name, 'main.dvi')
        self.assertEqual(file.content, 'Just a test \001\n')

    def testFollowupStupidQuoting(self):
        self.doNewIssue()

        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: Re: "[issue1] Testing... "

This is a followup
''')
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: chef@bork.bork.bork
From: richard <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


richard <richard@test.test> added the comment:

This is a followup

----------
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testEmailQuoting(self):
        self.instance.config.EMAIL_KEEP_QUOTED_TEXT = 'no'
        self.innerTestQuoting('''This is a followup
''')

    def testEmailQuotingRemove(self):
        self.instance.config.EMAIL_KEEP_QUOTED_TEXT = 'yes'
        self.innerTestQuoting('''Blah blah wrote:
> Blah bklaskdfj sdf asdf jlaskdf skj sdkfjl asdf
>  skdjlkjsdfalsdkfjasdlfkj dlfksdfalksd fj
>

This is a followup
''')

    def innerTestQuoting(self, expect):
        nodeid = self.doNewIssue()

        messages = self.db.issue.get(nodeid, 'messages')

        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: Re: [issue1] Testing...

Blah blah wrote:
> Blah bklaskdfj sdf asdf jlaskdf skj sdkfjl asdf
>  skdjlkjsdfalsdkfjasdlfkj dlfksdfalksd fj
>

This is a followup
''')
        # figure the new message id
        newmessages = self.db.issue.get(nodeid, 'messages')
        for msg in messages:
            newmessages.remove(msg)
        messageid = newmessages[0]

        self.compareMessages(self.db.msg.get(messageid, 'content'), expect)

    def testUserLookup(self):
        i = self.db.user.create(username='user1', address='user1@foo.com')
        self.assertEqual(uidFromAddress(self.db, ('', 'user1@foo.com'), 0), i)
        self.assertEqual(uidFromAddress(self.db, ('', 'USER1@foo.com'), 0), i)
        i = self.db.user.create(username='user2', address='USER2@foo.com')
        self.assertEqual(uidFromAddress(self.db, ('', 'USER2@foo.com'), 0), i)
        self.assertEqual(uidFromAddress(self.db, ('', 'user2@foo.com'), 0), i)

    def testUserAlternateLookup(self):
        i = self.db.user.create(username='user1', address='user1@foo.com',
                                alternate_addresses='user1@bar.com')
        self.assertEqual(uidFromAddress(self.db, ('', 'user1@bar.com'), 0), i)
        self.assertEqual(uidFromAddress(self.db, ('', 'USER1@bar.com'), 0), i)

    def testUserCreate(self):
        i = uidFromAddress(self.db, ('', 'user@foo.com'), 1)
        self.assertNotEqual(uidFromAddress(self.db, ('', 'user@bar.com'), 1), i)

    def testRFC2822(self):
        ascii_header = "[issue243] This is a \"test\" - with 'quotation' marks"
        unicode_header = '[issue244] \xd0\xb0\xd0\xbd\xd0\xb4\xd1\x80\xd0\xb5\xd0\xb9'
        unicode_encoded = '=?utf-8?q?[issue244]_=D0=B0=D0=BD=D0=B4=D1=80=D0=B5=D0=B9?='
        self.assertEqual(rfc2822.encode_header(ascii_header), ascii_header)
        self.assertEqual(rfc2822.encode_header(unicode_header), unicode_encoded)

    def testRegistrationConfirmation(self):
        otk = "Aj4euk4LZSAdwePohj90SME5SpopLETL"
        self.db.getOTKManager().set(otk, username='johannes')
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Message-Id: <dummy_test_message_id>
Subject: Re: Complete your registration to Roundup issue tracker
 -- key %s

This is a test confirmation of registration.
''' % otk)
        self.db.user.lookup('johannes')

    def testFollowupOnNonIssue(self):
        self.db.keyword.create(name='Foo')
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: [keyword1] Testing... [name=Bar]

''')
        self.assertEqual(self.db.keyword.get('1', 'name'), 'Bar')

    def testResentFrom(self):
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
Resent-From: mary <mary@test.test>
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Message-Id: <dummy_test_message_id>
Subject: [issue] Testing...

This is a test submission of a new issue.
''')
        assert not os.path.exists(SENDMAILDEBUG)
        l = self.db.issue.get(nodeid, 'nosy')
        l.sort()
        self.assertEqual(l, [self.richard_id, self.mary_id])
        return nodeid

    def testDejaVu(self):
        self.assertRaises(IgnoreLoop, self._handle_mail,
            '''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
X-Roundup-Loop: hello
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Message-Id: <dummy_test_message_id>
Subject: Re: [issue] Testing...

Hi, I've been mis-configured to loop messages back to myself.
''')

    def testItsBulkStupid(self):
        self.assertRaises(IgnoreBulk, self._handle_mail,
            '''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
Precedence: bulk
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Message-Id: <dummy_test_message_id>
Subject: Re: [issue] Testing...

Hi, I'm on holidays, and this is a dumb auto-responder.
''')

    def testAutoReplyEmailsAreIgnored(self):
        self.assertRaises(IgnoreBulk, self._handle_mail,
            '''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Message-Id: <dummy_test_message_id>
Subject: Re: [issue] Out of office AutoReply: Back next week

Hi, I am back in the office next week
''')

    def testNoSubject(self):
        self.assertRaises(MailUsageError, self._handle_mail,
            '''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')

    #
    # TEST FOR INVALID DESIGNATOR HANDLING
    #
    def testInvalidDesignator(self):
        self.assertRaises(MailUsageError, self._handle_mail,
            '''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: [frobulated] testing
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')
        self.assertRaises(MailUsageError, self._handle_mail,
            '''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: [issue12345] testing
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')

    def testInvalidClassLoose(self):
        self.instance.config.MAILGW_SUBJECT_PREFIX_PARSING = 'loose'
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: [frobulated] testing
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.issue.get(nodeid, 'title'),
            '[frobulated] testing')

    def testInvalidClassLooseReply(self):
        self.instance.config.MAILGW_SUBJECT_PREFIX_PARSING = 'loose'
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: Re: [frobulated] testing
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.issue.get(nodeid, 'title'),
            '[frobulated] testing')

    def testInvalidClassLoose(self):
        self.instance.config.MAILGW_SUBJECT_PREFIX_PARSING = 'loose'
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: [issue1234] testing
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.issue.get(nodeid, 'title'),
            '[issue1234] testing')

    def testClassLooseOK(self):
        self.instance.config.MAILGW_SUBJECT_PREFIX_PARSING = 'loose'
        self.db.keyword.create(name='Foo')
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: [keyword1] Testing... [name=Bar]
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.keyword.get('1', 'name'), 'Bar')

    def testClassStrictInvalid(self):
        self.instance.config.MAILGW_SUBJECT_PREFIX_PARSING = 'strict'
        self.instance.config.MAILGW_DEFAULT_CLASS = ''

        message = '''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: Testing...
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

'''
        self.assertRaises(MailUsageError, self._handle_mail, message)

    def testClassStrictValid(self):
        self.instance.config.MAILGW_SUBJECT_PREFIX_PARSING = 'strict'
        self.instance.config.MAILGW_DEFAULT_CLASS = ''

        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: [issue] Testing...
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')

        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.issue.get(nodeid, 'title'), 'Testing...')

    #
    # TEST FOR INVALID COMMANDS HANDLING
    #
    def testInvalidCommands(self):
        self.assertRaises(MailUsageError, self._handle_mail,
            '''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: testing [frobulated]
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')

    def testInvalidCommandPassthrough(self):
        self.instance.config.MAILGW_SUBJECT_SUFFIX_PARSING = 'none'
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: testing [frobulated]
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.issue.get(nodeid, 'title'),
            'testing [frobulated]')

    def testInvalidCommandPassthroughLoose(self):
        self.instance.config.MAILGW_SUBJECT_SUFFIX_PARSING = 'loose'
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: testing [frobulated]
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.issue.get(nodeid, 'title'),
            'testing [frobulated]')

    def testInvalidCommandPassthroughLooseOK(self):
        self.instance.config.MAILGW_SUBJECT_SUFFIX_PARSING = 'loose'
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: testing [assignedto=mary]
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.issue.get(nodeid, 'title'), 'testing')
        self.assertEqual(self.db.issue.get(nodeid, 'assignedto'), self.mary_id)

    def testCommandDelimiters(self):
        self.instance.config.MAILGW_SUBJECT_SUFFIX_DELIMITERS = '{}'
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: testing {assignedto=mary}
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.issue.get(nodeid, 'title'), 'testing')
        self.assertEqual(self.db.issue.get(nodeid, 'assignedto'), self.mary_id)

    def testPrefixDelimiters(self):
        self.instance.config.MAILGW_SUBJECT_SUFFIX_DELIMITERS = '{}'
        self.db.keyword.create(name='Foo')
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: richard <richard@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: {keyword1} Testing... {name=Bar}

''')
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.keyword.get('1', 'name'), 'Bar')

    def testCommandDelimitersIgnore(self):
        self.instance.config.MAILGW_SUBJECT_SUFFIX_DELIMITERS = '{}'
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: testing [assignedto=mary]
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')
        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.issue.get(nodeid, 'title'),
            'testing [assignedto=mary]')
        self.assertEqual(self.db.issue.get(nodeid, 'assignedto'), None)

    def testReplytoMatch(self):
        self.instance.config.MAILGW_SUBJECT_PREFIX_PARSING = 'loose'
        nodeid = self.doNewIssue()
        nodeid2 = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id2>
In-Reply-To: <dummy_test_message_id>
Subject: Testing...

Followup message.
''')

        nodeid3 = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id3>
In-Reply-To: <dummy_test_message_id2>
Subject: Testing...

Yet another message in the same thread/issue.
''')

        self.assertEqual(nodeid, nodeid2)
        self.assertEqual(nodeid, nodeid3)

    def testHelpSubject(self):
        message = '''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id2>
In-Reply-To: <dummy_test_message_id>
Subject: hElp


'''
        self.assertRaises(MailUsageHelp, self._handle_mail, message)

    def testMaillistSubject(self):
        self.instance.config.MAILGW_SUBJECT_SUFFIX_DELIMITERS = '[]'
        self.db.keyword.create(name='Foo')
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: [mailinglist-name] [keyword1] Testing.. [name=Bar]
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')

        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.keyword.get('1', 'name'), 'Bar')

    def testUnknownPrefixSubject(self):
        self.db.keyword.create(name='Foo')
        self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: VeryStrangeRe: [keyword1] Testing.. [name=Bar]
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

''')

        assert not os.path.exists(SENDMAILDEBUG)
        self.assertEqual(self.db.keyword.get('1', 'name'), 'Bar')

    def testOneCharSubject(self):
        message = '''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Subject: b
Cc: richard@test.test
Reply-To: chef@bork.bork.bork
Message-Id: <dummy_test_message_id>

'''
        try:
            self._handle_mail(message)
        except MailUsageError:
            self.fail('MailUsageError raised')

    def testIssueidLast(self):
        nodeid1 = self.doNewIssue()
        nodeid2 = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: mary <mary@test.test>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <followup_dummy_id>
In-Reply-To: <dummy_test_message_id>
Subject: New title [issue1]

This is a second followup
''')

        assert nodeid1 == nodeid2
        self.assertEqual(self.db.issue.get(nodeid2, 'title'), "Testing...")

    def testSecurityMessagePermissionContent(self):
        id = self.doNewIssue()
        issue = self.db.issue.getnode (id)
        self.db.security.addRole(name='Nomsg')
        self.db.security.addPermissionToRole('Nomsg', 'Email Access')
        for cl in 'issue', 'file', 'keyword':
            for p in 'View', 'Edit', 'Create':
                self.db.security.addPermissionToRole('Nomsg', p, cl)
        self.db.user.set(self.mary_id, roles='Nomsg')
        nodeid = self._handle_mail('''Content-Type: text/plain;
  charset="iso-8859-1"
From: Chef <chef@bork.bork.bork>
To: issue_tracker@your.tracker.email.domain.example
Message-Id: <dummy_test_message_id_2>
Subject: [issue%(id)s] Testing... [nosy=+mary]

Just a test reply
'''%locals())
        assert os.path.exists(SENDMAILDEBUG)
        self.compareMessages(self._get_mail(),
'''FROM: roundup-admin@your.tracker.email.domain.example
TO: chef@bork.bork.bork, richard@test.test
Content-Type: text/plain; charset="utf-8"
Subject: [issue1] Testing...
To: richard@test.test
From: "Bork, Chef" <issue_tracker@your.tracker.email.domain.example>
Reply-To: Roundup issue tracker
 <issue_tracker@your.tracker.email.domain.example>
MIME-Version: 1.0
Message-Id: <dummy_test_message_id_2>
In-Reply-To: <dummy_test_message_id>
X-Roundup-Name: Roundup issue tracker
X-Roundup-Loop: hello
X-Roundup-Issue-Status: chatting
Content-Transfer-Encoding: quoted-printable


Bork, Chef <chef@bork.bork.bork> added the comment:

Just a test reply

----------
nosy: +mary
status: unread -> chatting

_______________________________________________________________________
Roundup issue tracker <issue_tracker@your.tracker.email.domain.example>
<http://tracker.example/cgi-bin/roundup.cgi/bugs/issue1>
_______________________________________________________________________
''')

    def testOutlookAttachment(self):
        message = '''X-MimeOLE: Produced By Microsoft Exchange V6.5
Content-class: urn:content-classes:message
MIME-Version: 1.0
Content-Type: multipart/mixed;
	boundary="----_=_NextPart_001_01CACA65.40A51CBC"
Subject: Example of a failed outlook attachment e-mail
Date: Tue, 23 Mar 2010 01:43:44 -0700
Message-ID: <CA37F17219784343816CA6613D2E339205E7D0F9@nrcwstexb1.nrc.ca>
X-MS-Has-Attach: yes
X-MS-TNEF-Correlator: 
Thread-Topic: Example of a failed outlook attachment e-mail
Thread-Index: AcrKJo/t3pUBBwTpSwWNE3LE67UBDQ==
From: "Hugh" <richard@test.test>
To: <richard@test.test>
X-OriginalArrivalTime: 23 Mar 2010 08:45:57.0350 (UTC) FILETIME=[41893860:01CACA65]

This is a multi-part message in MIME format.

------_=_NextPart_001_01CACA65.40A51CBC
Content-Type: multipart/alternative;
	boundary="----_=_NextPart_002_01CACA65.40A51CBC"


------_=_NextPart_002_01CACA65.40A51CBC
Content-Type: text/plain;
	charset="us-ascii"
Content-Transfer-Encoding: quoted-printable


Hi Richard,

I suppose this isn't the exact message that was sent but is a resend of
one of my trial messages that failed.  For your benefit I changed the
subject line and am adding these words to the message body.  Should
still be as problematic, but if you like I can resend an exact copy of a
failed message changing nothing except putting your address instead of
our tracker.

Thanks very much for taking time to look into this.  Much appreciated.

 <<battery backup>>=20

------_=_NextPart_002_01CACA65.40A51CBC
Content-Type: text/html;
	charset="us-ascii"
Content-Transfer-Encoding: quoted-printable

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<HTML>
<HEAD>
<META HTTP-EQUIV=3D"Content-Type" CONTENT=3D"text/html; =
charset=3Dus-ascii">
<META NAME=3D"Generator" CONTENT=3D"MS Exchange Server version =
6.5.7654.12">
<TITLE>Example of a failed outlook attachment e-mail</TITLE>
</HEAD>
<BODY>
<!-- Converted from text/rtf format -->
<BR>

<P><FONT SIZE=3D2 FACE=3D"Arial">Hi Richard,</FONT>
</P>

<P><FONT SIZE=3D2 FACE=3D"Arial">I suppose this isn't the exact message =
that was sent but is a resend of one of my trial messages that =
failed.&nbsp; For your benefit I changed the subject line and am adding =
these words to the message body.&nbsp; Should still be as problematic, =
but if you like I can resend an exact copy of a failed message changing =
nothing except putting your address instead of our tracker.</FONT></P>

<P><FONT SIZE=3D2 FACE=3D"Arial">Thanks very much for taking time to =
look into this.&nbsp; Much appreciated.</FONT>
</P>
<BR>

<P><FONT FACE=3D"Arial" SIZE=3D2 COLOR=3D"#000000"> &lt;&lt;battery =
backup&gt;&gt; </FONT>
</P>

</BODY>
</HTML>
------_=_NextPart_002_01CACA65.40A51CBC--

------_=_NextPart_001_01CACA65.40A51CBC
Content-Type: message/rfc822
Content-Transfer-Encoding: 7bit

X-MimeOLE: Produced By Microsoft Exchange V6.5
MIME-Version: 1.0
Content-Type: multipart/alternative;
	boundary="----_=_NextPart_003_01CAC15A.29717800"
X-OriginalArrivalTime: 11 Mar 2010 20:33:51.0249 (UTC) FILETIME=[28FEE010:01CAC15A]
Content-class: urn:content-classes:message
Subject: battery backup
Date: Thu, 11 Mar 2010 13:33:43 -0700
Message-ID: <p06240809c7bf02f9624c@[128.114.22.203]>
X-MS-Has-Attach: 
X-MS-TNEF-Correlator: 
Thread-Topic: battery backup
Thread-Index: AcrBWimtulTrSvBdQ2CcfZ8lyQdxmQ==
From: "Jerry" <jerry@test.test>
To: "Hugh" <hugh@test.test>

This is a multi-part message in MIME format.

------_=_NextPart_003_01CAC15A.29717800
Content-Type: text/plain;
	charset="iso-8859-1"
Content-Transfer-Encoding: quoted-printable

Dear Hugh,
	A car batter has an energy capacity of ~ 500Wh.  A UPS=20
battery is worse than this.

if we need to provied 100kW for 30 minutes that will take 100 car=20
batteries.  This seems like an awful lot of batteries.

Of course I like your idea of making the time 1 minute, so we get to=20
a more modest number of batteries

Jerry


------_=_NextPart_003_01CAC15A.29717800
Content-Type: text/html;
	charset="iso-8859-1"
Content-Transfer-Encoding: quoted-printable

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<HTML>
<HEAD>
<META HTTP-EQUIV=3D"Content-Type" CONTENT=3D"text/html; =
charset=3Diso-8859-1">
<META NAME=3D"Generator" CONTENT=3D"MS Exchange Server version =
6.5.7654.12">
<TITLE>battery backup</TITLE>
</HEAD>
<BODY>
<!-- Converted from text/plain format -->

<P><FONT SIZE=3D2>Dear Hugh,</FONT>

<BR>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <FONT SIZE=3D2>A car =
batter has an energy capacity of ~ 500Wh.&nbsp; A UPS </FONT>

<BR><FONT SIZE=3D2>battery is worse than this.</FONT>
</P>

<P><FONT SIZE=3D2>if we need to provied 100kW for 30 minutes that will =
take 100 car </FONT>

<BR><FONT SIZE=3D2>batteries.&nbsp; This seems like an awful lot of =
batteries.</FONT>
</P>

<P><FONT SIZE=3D2>Of course I like your idea of making the time 1 =
minute, so we get to </FONT>

<BR><FONT SIZE=3D2>a more modest number of batteries</FONT>
</P>

<P><FONT SIZE=3D2>Jerry</FONT>
</P>

</BODY>
</HTML>
------_=_NextPart_003_01CAC15A.29717800--

------_=_NextPart_001_01CACA65.40A51CBC--
'''
        nodeid = self._handle_mail(message)
        assert not os.path.exists(SENDMAILDEBUG)
        msgid = self.db.issue.get(nodeid, 'messages')[0]
        self.assert_(self.db.msg.get(msgid, 'content').startswith('Hi Richard'))
        self.assertEqual(self.db.msg.get(msgid, 'files'), ['1', '2'])
        fileid = self.db.msg.get(msgid, 'files')[0]
        self.assertEqual(self.db.file.get(fileid, 'type'), 'text/html')
        fileid = self.db.msg.get(msgid, 'files')[1]
        self.assertEqual(self.db.file.get(fileid, 'type'), 'message/rfc822')

    def testForwardedMessageAttachment(self):
        message = '''Return-Path: <rgg@test.test>
Received: from localhost(127.0.0.1), claiming to be "[115.130.26.69]"
via SMTP by localhost, id smtpdAAApLaWrq; Tue Apr 13 23:10:05 2010
Message-ID: <4BC4F9C7.50409@test.test>
Date: Wed, 14 Apr 2010 09:09:59 +1000
From: Rupert Goldie <rgg@test.test>
User-Agent: Thunderbird 2.0.0.24 (Windows/20100228)
MIME-Version: 1.0
To: ekit issues <issues@test.test>
Subject: [Fwd: PHP ERROR (fb)] post limit reached
Content-Type: multipart/mixed; boundary="------------000807090608060304010403"

This is a multi-part message in MIME format.
--------------000807090608060304010403
Content-Type: text/plain; charset=ISO-8859-1; format=flowed
Content-Transfer-Encoding: 7bit

Catch this exception and log it without emailing.

--------------000807090608060304010403
Content-Type: message/rfc822; name="PHP ERROR (fb).eml"
Content-Transfer-Encoding: 7bit
Content-Disposition: inline; filename="PHP ERROR (fb).eml"

Return-Path: <ektravj@test.test>
X-Sieve: CMU Sieve 2.2
via SMTP by crown.off.ekorp.com, id smtpdAAA1JaW1o; Tue Apr 13 23:01:04 2010
X-Virus-Scanned: by amavisd-new at ekit.com
To: facebook-errors@test.test
From: ektravj@test.test
Subject: PHP ERROR (fb)
Message-Id: <20100413230100.D601D27E84@mail2.elax3.ekorp.com>
Date: Tue, 13 Apr 2010 23:01:00 +0000 (UTC)

[13-Apr-2010 22:49:02] PHP Fatal error:  Uncaught exception 'Exception' with message 'Facebook Error Message: Feed action request limit reached' in /app/01/www/virtual/fb.ekit.com/htdocs/includes/functions.php:280
Stack trace:
#0 /app/01/www/virtual/fb.ekit.com/htdocs/gateway/ekit/feed/index.php(178): fb_exceptions(Object(FacebookRestClientException))
#1 {main}
 thrown in /app/01/www/virtual/fb.ekit.com/htdocs/includes/functions.php on line 280


--------------000807090608060304010403--
'''
        nodeid = self._handle_mail(message)
        assert not os.path.exists(SENDMAILDEBUG)
        msgid = self.db.issue.get(nodeid, 'messages')[0]
        self.assertEqual(self.db.msg.get(msgid, 'content'),
            'Catch this exception and log it without emailing.')
        self.assertEqual(self.db.msg.get(msgid, 'files'), ['1'])
        fileid = self.db.msg.get(msgid, 'files')[0]
        self.assertEqual(self.db.file.get(fileid, 'type'), 'message/rfc822')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MailgwTestCase))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)

# vim: set filetype=python sts=4 sw=4 et si :




