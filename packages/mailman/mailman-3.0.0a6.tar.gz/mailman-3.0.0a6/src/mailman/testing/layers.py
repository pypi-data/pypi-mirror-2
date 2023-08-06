# Copyright (C) 2008-2010 by the Free Software Foundation, Inc.
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

"""Mailman test layers."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'ConfigLayer',
    'MockAndMonkeyLayer',
    'RESTLayer',
    'SMTPLayer',
    ]


import os
import sys
import shutil
import logging
import datetime
import tempfile

from pkg_resources import resource_string
from textwrap import dedent
from urllib2 import urlopen, URLError
from zope.component import getUtility

from mailman.config import config
from mailman.core import initialize
from mailman.core.initialize import INHIBIT_CONFIG_FILE
from mailman.core.i18n import _
from mailman.core.logging import get_handler
from mailman.interfaces.domain import IDomainManager
from mailman.interfaces.messages import IMessageStore
from mailman.testing.helpers import TestableMaster
from mailman.testing.mta import ConnectionCountingController
from mailman.utilities.datetime import factory
from mailman.utilities.string import expand


TEST_TIMEOUT = datetime.timedelta(seconds=5)
NL = '\n'



class MockAndMonkeyLayer:
    """Layer for mocking and monkey patching for testing."""

    @classmethod
    def setUp(cls):
        factory.testing_mode = True

    @classmethod
    def tearDown(cls):
        factory.testing_mode = False

    @classmethod
    def testTearDown(cls):
        factory.reset()



class ConfigLayer(MockAndMonkeyLayer):
    """Layer for pushing and popping test configurations."""

    var_dir = None
    styles = None

    @classmethod
    def setUp(cls):
        # Set up the basic configuration stuff.  Turn off path creation until
        # we've pushed the testing config.
        config.create_paths = False
        initialize.initialize_1(INHIBIT_CONFIG_FILE)
        assert cls.var_dir is None, 'Layer already set up'
        # Calculate a temporary VAR_DIR directory so that run-time artifacts
        # of the tests won't tread on the installation's data.  This also
        # makes it easier to clean up after the tests are done, and insures
        # isolation of test suite runs.
        cls.var_dir = tempfile.mkdtemp()
        # We need a test configuration both for the foreground process and any
        # child processes that get spawned.  lazr.config would allow us to do
        # it all in a string that gets pushed, and we'll do that for the
        # foreground, but because we may be spawning processes (such as queue
        # runners) we'll need a file that we can specify to the with the -C
        # option.  Craft the full test configuration string here, push it, and
        # also write it out to a temp file for -C.
        test_config = dedent("""
        [mailman]
        layout: testing
        [paths.testing]
        var_dir: %s
        """ % cls.var_dir)
        # Read the testing config and push it.
        test_config += resource_string('mailman.testing', 'testing.cfg')
        config.create_paths = True
        config.push('test config', test_config)
        # Initialize everything else.
        initialize.initialize_2()
        initialize.initialize_3()
        # When stderr debugging is enabled, subprocess root loggers should
        # also be more verbose.
        if cls.stderr:
            test_config += dedent("""
            [logging.root]
            propagate: yes
            level: debug
            """)
        # Enable log message propagation and reset the log paths so that the
        # doctests can check the output.
        for logger_config in config.logger_configs:
            sub_name = logger_config.name.split('.')[-1]
            if sub_name == 'root':
                continue
            logger_name = 'mailman.' + sub_name
            log = logging.getLogger(logger_name)
            log.propagate = True
            # Reopen the file to a new path that tests can get at.  Instead of
            # using the configuration file path though, use a path that's
            # specific to the logger so that tests can find expected output
            # more easily.
            path = os.path.join(config.LOG_DIR, sub_name)
            get_handler(sub_name).reopen(path)
            log.setLevel(logging.DEBUG)
            # If stderr debugging is enabled, make sure subprocesses are also
            # more verbose.
            if cls.stderr:
                test_config += expand(dedent("""
                [logging.$name]
                propagate: yes
                level: debug
                """), dict(name=sub_name, path=path))
        # zope.testing sets up logging before we get to our own initialization
        # function.  This messes with the root logger, so explicitly set it to
        # go to stderr.
        if cls.stderr:
            console = logging.StreamHandler(sys.stderr)
            formatter = logging.Formatter(config.logging.root.format,
                                          config.logging.root.datefmt)
            console.setFormatter(formatter)
            logging.getLogger().addHandler(console)
        # Write the configuration file for subprocesses and set up the config
        # object to pass that properly on the -C option.
        config_file = os.path.join(cls.var_dir, 'test.cfg')
        with open(config_file, 'w') as fp:
            fp.write(test_config)
            print >> fp
        config.filename = config_file

    @classmethod
    def tearDown(cls):
        assert cls.var_dir is not None, 'Layer not set up'
        config.pop('test config')
        shutil.rmtree(cls.var_dir)
        cls.var_dir = None

    @classmethod
    def testSetUp(cls):
        # Add an example domain.
        getUtility(IDomainManager).add(
            'example.com', 'An example domain.',
            'http://lists.example.com', 'postmaster@example.com')
        config.db.commit()

    @classmethod
    def testTearDown(cls):
        # Reset the database between tests.
        config.db._reset()
        # Remove all residual queue files.
        for dirpath, dirnames, filenames in os.walk(config.QUEUE_DIR):
            for filename in filenames:
                os.remove(os.path.join(dirpath, filename))
        # Clear out messages in the message store.
        message_store = getUtility(IMessageStore)
        for message in message_store.messages:
            message_store.delete_message(message['message-id'])
        config.db.commit()
        # Reset the global style manager.
        config.style_manager.populate()

    # Flag to indicate that loggers should propagate to the console.
    stderr = False

    @classmethod
    def enable_stderr(cls):
        """Enable stderr logging if -e/--stderr is given.

        We used to hack our way into the zc.testing framework, but that was
        undocumented and way too fragile.  Well, this probably is too, but now
        we just scan sys.argv for -e/--stderr and enable logging if found.
        Then we remove the option from sys.argv.  This works because this
        method is called before zope.testrunner sees the options.

        As a bonus, we'll check an environment variable too.
        """
        if '-e' in sys.argv:
            cls.stderr = True
            sys.argv.remove('-e')
        if '--stderr' in sys.argv:
            cls.stderr = True
            sys.argv.remove('--stderr')
        if len(os.environ.get('MM_VERBOSE_TESTLOG', '').strip()) > 0:
            cls.stderr = True

    # The top of our source tree, for tests that care (e.g. hooks.txt).
    root_directory = None

    @classmethod
    def set_root_directory(cls, directory):
        """Set the directory at the root of our source tree.

        zc.recipe.testrunner runs from parts/test/working-directory, but
        that's actually changed over the life of the package.  Some tests
        care, e.g. because they need to find our built-out bin directory.
        Fortunately, buildout can give us this information.  See the
        `buildout.cfg` file for where this method is called.
        """
        cls.root_directory = directory



class SMTPLayer(ConfigLayer):
    """Layer for starting, stopping, and accessing a test SMTP server."""

    smtpd = None

    @classmethod
    def setUp(cls):
        assert cls.smtpd is None, 'Layer already set up'
        host = config.mta.smtp_host
        port = int(config.mta.smtp_port)
        cls.smtpd = ConnectionCountingController(host, port)
        cls.smtpd.start()

    @classmethod
    def tearDown(cls):
        assert cls.smtpd is not None, 'Layer not set up'
        cls.smtpd.clear()
        cls.smtpd.stop()

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        cls.smtpd.clear()



class RESTLayer(SMTPLayer):
    """Layer for starting, stopping, and accessing the test REST layer."""

    server = None

    @staticmethod
    def _wait_for_rest_server():
        until = datetime.datetime.now() + TEST_TIMEOUT
        while datetime.datetime.now() < until:
            try:
                fp = urlopen('http://localhost:8001/3.0/system')
            except URLError:
                pass
            else:
                fp.close()
                break
        else:
            raise RuntimeError('REST server did not start up')

    @classmethod
    def setUp(cls):
        assert cls.server is None, 'Layer already set up'
        cls.server = TestableMaster(cls._wait_for_rest_server)
        cls.server.start('rest')

    @classmethod
    def tearDown(cls):
        assert cls.server is not None, 'Layer not set up'
        cls.server.stop()
        cls.server = None
