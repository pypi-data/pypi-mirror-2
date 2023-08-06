# Copyright (C) 2001-2010 by the Free Software Foundation, Inc.
#
# This file is part of GNU Mailman.
#
# GNU Mailman is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# GNU Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# GNU Mailman.  If not, see <http://www.gnu.org/licenses/>.

"""Test the bounce detection modules."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'test_suite',
    ]


import os
import sys
import email
import unittest

from contextlib import closing
from pkg_resources import resource_stream

from mailman.app.finder import find_components
from mailman.bouncers.caiwireless import Caiwireless
from mailman.bouncers.microsoft import Microsoft
from mailman.bouncers.smtp32 import SMTP32
from mailman.interfaces.bounce import IBounceDetector, NonFatal



class BounceTest(unittest.TestCase):
    DATA = (
        # Postfix bounces
        ('Postfix', 'postfix_01.txt', ['xxxxx@local.ie']),
        ('Postfix', 'postfix_02.txt', ['yyyyy@digicool.com']),
        ('Postfix', 'postfix_03.txt', ['ttttt@ggggg.com']),
        ('Postfix', 'postfix_04.txt', ['davidlowie@mail1.keftamail.com']),
        ('Postfix', 'postfix_05.txt', ['bjelf@detectit.net']),
        # Exim bounces
        ('Exim', 'exim_01.txt', ['delangen@its.tudelft.nl']),
        # SimpleMatch bounces
        ('SimpleMatch', 'sendmail_01.txt', ['zzzzz@nfg.nl']),
        ('SimpleMatch', 'simple_01.txt', ['bbbsss@turbosport.com']),
        ('SimpleMatch', 'simple_02.txt', ['chris.ggggmmmm@usa.net']),
        ('SimpleMatch', 'simple_04.txt', ['claird@starbase.neosoft.com']),
        ('SimpleMatch', 'newmailru_01.txt', ['zzzzz@newmail.ru']),
        ('SimpleMatch', 'hotpop_01.txt', ['allensmithee@hotpop.com']),
        ('SimpleMatch', 'microsoft_03.txt', ['midica@banknbr.com']),
        ('SimpleMatch', 'simple_05.txt', ['rlosardo@sbcglobal.net']),
        ('SimpleMatch', 'simple_06.txt', ['dlyle@hamiltonpacific.com']),
        ('SimpleMatch', 'simple_07.txt', ['william.xxxx@sbcglobal.net']),
        ('SimpleMatch', 'simple_08.txt', ['severin.XXX@t-online.de']),
        ('SimpleMatch', 'simple_09.txt', ['RobotMail@auto-walther.de']),
        ('SimpleMatch', 'simple_10.txt', ['sais@thehartford.com']),
        ('SimpleMatch', 'simple_11.txt', ['carlosr73@hartfordlife.com']),
        ('SimpleMatch', 'simple_12.txt', ['charrogar@rhine1.andrew.ac.jp']),
        ('SimpleMatch', 'simple_13.txt', ['dycusibreix@ademe.fr']),
        ('SimpleMatch', 'simple_14.txt', ['dump@dachamp.com',
                                          'iqxwmmfauudpo@dachamp.com']),
        ('SimpleMatch', 'simple_15.txt', ['isam@kviv.be']),
        ('SimpleMatch', 'simple_16.txt', ['xvlogtfsei@the-messenger.com']),
        ('SimpleMatch', 'simple_17.txt', ['internetsailing@gmail.com']),
        ('SimpleMatch', 'simple_18.txt', ['powell@kesslersupply.com']),
        ('SimpleMatch', 'simple_19.txt', ['mcfall@cepi.com.ar']),
        ('SimpleMatch', 'simple_20.txt', ['duke@ald.socgen.com']),
        ('SimpleMatch', 'simple_23.txt', ['ketchuy@dadoservice.it']),
        ('SimpleMatch', 'simple_24.txt', ['liberty@gomaps.com']),
        ('SimpleMatch', 'simple_25.txt', ['mahau@cnbearing.com']),
        ('SimpleMatch', 'simple_26.txt', ['reilizavet@lar.ieo.it']),
        ('SimpleMatch', 'simple_27.txt', ['kulp@webmail.pla.net.py']),
        ('SimpleMatch', 'bounce_02.txt', ['acinsp1@midsouth.rr.com']),
        ('SimpleMatch', 'bounce_03.txt', ['james@jeborall.demon.co.uk']),
        # SimpleWarning
        ('SimpleWarning', 'simple_03.txt', NonFatal),
        ('SimpleWarning', 'simple_21.txt', NonFatal),
        ('SimpleWarning', 'simple_22.txt', NonFatal),
        # GroupWise
        ('GroupWise', 'groupwise_01.txt', ['thoff@MAINEX1.ASU.EDU']),
        # This one really sucks 'cause it's text/html.  Just make sure it
        # doesn't throw an exception, but we won't get any meaningful
        # addresses back from it.
        ('GroupWise', 'groupwise_02.txt', []),
        # Actually, it's from Exchange, and Exchange does recognize it
        ('Exchange', 'groupwise_02.txt', ['omarmo@thebas.com']),
        # Yale's own
        ('Yale', 'yale_01.txt', ['thomas.dtankengine@cs.yale.edu',
                                 'thomas.dtankengine@yale.edu']),
        # DSN, i.e. RFC 1894
        ('DSN', 'dsn_01.txt', ['JimmyMcEgypt@go.com']),
        ('DSN', 'dsn_02.txt', ['zzzzz@zeus.hud.ac.uk']),
        ('DSN', 'dsn_03.txt', ['ddd.kkk@advalvas.be']),
        ('DSN', 'dsn_04.txt', ['max.haas@unibas.ch']),
        ('DSN', 'dsn_05.txt', NonFatal),
        ('DSN', 'dsn_06.txt', NonFatal),
        ('DSN', 'dsn_07.txt', NonFatal),
        ('DSN', 'dsn_08.txt', NonFatal),
        ('DSN', 'dsn_09.txt', ['pr@allen-heath.com']),
        ('DSN', 'dsn_10.txt', ['anne.person@dom.ain']),
        ('DSN', 'dsn_11.txt', ['joem@example.com']),
        ('DSN', 'dsn_12.txt', ['auaauqdgrdz@jtc-con.co.jp']),
        ('DSN', 'dsn_13.txt', ['marcooherbst@cardinal.com']),
        ('DSN', 'dsn_14.txt', ['artboardregistration@home.dk']),
        ('DSN', 'dsn_15.txt', ['horu@ccc-ces.com']),
        # Microsoft Exchange
        ('Exchange', 'microsoft_01.txt', ['DJBENNETT@IKON.COM']),
        ('Exchange', 'microsoft_02.txt', ['MDMOORE@BALL.COM']),
        # SMTP32
        ('SMTP32', 'smtp32_01.txt', ['oliver@pcworld.com.ph']),
        ('SMTP32', 'smtp32_02.txt', ['lists@mail.spicynoodles.com']),
        ('SMTP32', 'smtp32_03.txt', ['borisk@gw.xraymedia.com']),
        ('SMTP32', 'smtp32_04.txt', ['after_another@pacbell.net',
                                     'one_bad_address@pacbell.net']),
        ('SMTP32', 'smtp32_05.txt', ['jmrpowersports@jmrpowersports.com']),
        ('SMTP32', 'smtp32_06.txt', ['Absolute_garbage_addr@pacbell.net']),
        ('SMTP32', 'smtp32_07.txt', ['info@husbyran.com']),
        # Qmail
        ('Qmail', 'qmail_01.txt', ['psadisc@wwwmail.n-h.de']),
        ('Qmail', 'qmail_02.txt', ['rauschlo@frontfin.com']),
        ('Qmail', 'qmail_03.txt', ['crown@hbc.co.jp']),
        ('Qmail', 'qmail_04.txt', ['merotiia@tennisnsw.com.au']),
        ('Qmail', 'qmail_05.txt', ['ivokggrrdvc@caixaforte.freeservers.com']),
        # LLNL's custom Sendmail
        ('LLNL', 'llnl_01.txt', ['trotts1@llnl.gov']),
        # Netscape's server...
        ('Netscape', 'netscape_01.txt', ['aaaaa@corel.com',
                                         'bbbbb@corel.com']),
        # Yahoo's proprietary format
        ('Yahoo', 'yahoo_01.txt', ['subscribe.motorcycles@listsociety.com']),
        ('Yahoo', 'yahoo_02.txt', ['agarciamartiartu@yahoo.es']),
        ('Yahoo', 'yahoo_03.txt', ['cresus22@yahoo.com']),
        ('Yahoo', 'yahoo_04.txt', ['agarciamartiartu@yahoo.es',
                                   'open00now@yahoo.co.uk']),
        ('Yahoo', 'yahoo_05.txt', ['cresus22@yahoo.com',
                                   'jjb700@yahoo.com']),
        ('Yahoo', 'yahoo_06.txt', ['andrew_polevoy@yahoo.com',
                                   'baruch_sterin@yahoo.com',
                                   'rjhoeks@yahoo.com',
                                   'tritonrugger91@yahoo.com']),
        ('Yahoo', 'yahoo_07.txt', ['mark1960_1998@yahoo.com',
                                   'ovchenkov@yahoo.com',
                                   'tsa412@yahoo.com',
                                   'vaxheadroom@yahoo.com']),
        ('Yahoo', 'yahoo_08.txt', ['chatrathis@yahoo.com',
                                   'crownjules01@yahoo.com',
                                   'cwl_999@yahoo.com',
                                   'eichaiwiu@yahoo.com',
                                   'rjhoeks@yahoo.com',
                                   'yuli_kolesnikov@yahoo.com']),
        ('Yahoo', 'yahoo_09.txt', ['hankel_o_fung@yahoo.com',
                                   'ultravirus2001@yahoo.com']),
        ('Yahoo', 'yahoo_10.txt', ['jajcchoo@yahoo.com',
                                   'lyons94706@yahoo.com',
                                   'turtle4jne@yahoo.com']),
        # sina.com appears to use their own weird SINAEMAIL MTA
        ('Sina', 'sina_01.txt', ['boboman76@sina.com', 'alan_t18@sina.com']),
        # No address can be detected in these...
        # dumbass_01.txt - We love Microsoft. :(
        # Done
        )

    def _getmsg(self, filename):
        with closing(resource_stream('mailman.tests.bounces', filename)) as fp:
            return email.message_from_file(fp)

    def test_bounce(self):
        detectors = {}
        for detector in find_components('mailman.bouncers', IBounceDetector):
            detectors[detector.__name__] = detector()
        for detector_name, filename, expected_addresses in self.DATA:
            msg = self._getmsg(filename)
            found_addresses = detectors[detector_name].process(msg)
            # Some modules return None instead of the empty sequence.
            if found_addresses is None:
                found_addresses = set()
            elif found_addresses is not NonFatal:
                found_addresses = set(found_addresses)
            if expected_addresses is not NonFatal:
                expected_addresses = set(expected_addresses)
            self.assertEqual(found_addresses, expected_addresses)

    def test_SMTP32_failure(self):
        # This file has no X-Mailer: header
        msg = self._getmsg('postfix_01.txt')
        self.failIf(msg['x-mailer'] is not None)
        self.failIf(SMTP32().process(msg))

    def test_caiwireless(self):
        # BAW: this is a mostly bogus test; I lost the samples. :(
        msg = email.message_from_string("""\
Content-Type: multipart/report; boundary=BOUNDARY

--BOUNDARY

--BOUNDARY--

""")
        self.assertEqual(None, Caiwireless().process(msg))

    def test_microsoft(self):
        # BAW: similarly as above, I lost the samples. :(
        msg = email.message_from_string("""\
Content-Type: multipart/report; boundary=BOUNDARY

--BOUNDARY

--BOUNDARY--

""")
        self.assertEqual(None, Microsoft().process(msg))



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BounceTest))
    return suite
