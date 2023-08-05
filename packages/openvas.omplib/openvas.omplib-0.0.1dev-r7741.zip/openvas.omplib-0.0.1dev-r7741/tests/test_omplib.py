# -*- coding: utf-8 -*-
"""
Testsuite for openvas.oaplib
"""
#
# Copyright 2010 by Hartmut Goebel <h.goebel@goebel-consult.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

__author__ = "Hartmut Goebel <h.goebel@goebel-consult.de>"
__copyright__ = "Copyright 2010 by Hartmut Goebel <h.goebel@goebel-consult.de>"
__licence__ = "GNU General Public License version 3 (GPL v3)"

import unittest
import os
import inspect

import openvas.omplib
from openvas.omplib import etree

# uuids of samples delivered by gsa, see gsa/src/html/src/help.xsl
SAMPLE_TASK_ID = '343435d6-91b0-11de-9478-ffd71f4c6f29'
SAMPLE_REPORT_ID = '343435d6-91b0-11de-9478-ffd71f4c6f30'


def tests_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

class OMPTestBase(unittest.TestCase):
    _OMP_HOST = None
    _OMP_PORT = None
    _OMP_USER = None
    _OMP_PASSWD = None

    def setUp(self):
        self.client = openvas.omplib.OMPClient(self._OMP_HOST, self._OMP_PORT,
                                               self._OMP_USER, self._OMP_PASSWD)
        self.client.open()

    def tearDown(self):
        self.client.close()


class TestOMP(OMPTestBase):

    def test_help(self):
        self.client.help()

    def test_xml_0(self):
        text = self.client.xml('<help/>')
        self.assert_(isinstance(text, basestring))
        self.assert_(text != '')

    def test_xml_1(self):
        xml = self.client.xml('<help/>', xml_result=True)
        self.assert_(etree.iselement(xml))

    #--- agent ---

    def test_agent(self):
        installerdata = "#!/bin sh\necho 'agent'"
        name = "omp_test_agent"
        try:
            self.client.create_agent(name, installerdata, 'Some Agent')
            agents = self.client.get_agents()
            self.assert_(inspect.isgenerator(agents))
            for agent in agents:
                self.assert_(isinstance(agent, dict))
                pass
            agent = self.client.get_agents(name)
            self.assert_(isinstance(agent, dict))
            self.assert_(agent['name'] == name)
        finally:
            self.client.delete_agent(name)

    #--- config ---

    def test_config_get_all(self):
        configs = self.client.get_configs()
        self.assert_(inspect.isgenerator(configs))
        for cfg in configs:
            self.assert_(isinstance(cfg, dict))

    def test_config_get_one(self):
        cfg = self.client.get_configs('empty')
        self.assert_(isinstance(cfg, dict))
        self.assert_(cfg['name'] == 'empty')

    def _test_config(self):
        rcdata = open(tests_path('new_task_empty_rc.xml')).read()
        name = "omp_test_config"
        try:
            self.client.create_config(name, rcdata)
        finally:
            self.client.delete_config(name)

    #--- lsc_credentials ---

    def _test_lsc_credentials(self):
        name = "omp_test_lsc_credential"
        #self.client.create_lsc_credential(name, 'LoGinInOut', 'Kommentar')
        #self.client.create_lsc_credential(name+'2', 'LoGinInOutx', 'Kommentarx')
        creds = self.client.get_lsc_credentials()
        self.assert_(inspect.isgenerator(creds))
        creds = list(self.client.get_lsc_credentials(name))
        self.assert_(len(creds) == 1)
        #self.client.delete_lsc_credential(name)
        #self.client.delete_lsc_credential(name+'2')

    #--- targets ---

    def test_targets(self):
        name = "omp_test_targets"
        hosts = '10.10.10.10\nwww.example.com'
        try:
            self.client.create_target(name, hosts, 'Kommentar on Targets')

            targets = self.client.get_targets()
            self.assert_(inspect.isgenerator(targets))
            for target in targets:
                self.assert_(isinstance(target, dict))

            target = self.client.get_targets(name)
            self.assert_(isinstance(target, dict))
            self.assert_(target['name'] == name)
        finally:
            self.client.delete_target(name)

    #--- escalators ---

    def test_escalator(self):
        # can't test since creating escalators is not yet implemented
        name = "omp_test_escalators"
        # until creating escalators is not yet implemented simply create
        # using_xml()
        xml = """
        <create_escalator>
        <name>%s</name>
        <comment>hjhjklh</comment>
        <condition>Threat level at least<data><name>level</name>Medium</data></condition>
        <event>Task run status changed<data><name>status</name>Done</data></event>
        <method>Email<data><name>to_address</name>aaaa@example.com</data><data><name>from_address</name>vaaa@example.com</data><data><name>notice</name>1</data></method>
        </create_escalator>
        """ % name.encode('utf-8')
        try:
            self.client.xml(xml)
            escalators = self.client.get_escalators()
            self.assert_(inspect.isgenerator(escalators))
            for escalator in escalators:
                self.assert_(isinstance(escalator, dict))

            escalator = self.client.get_escalators(name)
            self.assert_(isinstance(escalator, dict))
            self.assert_(escalator['name'] == name)
        finally:
            self.client.delete_escalator(name)
            pass

    #--- misc ---

    def test_get_preferences(self):
        prefs = self.client.get_preferences()
        self.assert_(isinstance(prefs, dict))

    def _test_get_certificates(self):
        certs = self.client.get_certificates()
        print certs

    def test_get_report(self):
        report = self.client.get_report(SAMPLE_REPORT_ID)
        #print etree.tostring(report[3])
        #print etree.tostring(report)


class main(unittest.main):
    def parseArgs(self, argv):
        """

Examples:
  %prog                            - run default set of tests
  %prog MyTestSuite                - run suite 'MyTestSuite'
  %prog MyTestCase.testSomething   - run MyTestCase.testSomething
  %prog MyTestCase                 - run all 'test*' test methods
                                               in MyTestCase
        """
        import getpass
        import optparse
        parser = optparse.OptionParser('usage: %prog [options] [test] [...]' +
                                       self.parseArgs.__doc__.rstrip(),
                                       add_help_option=False)
        parser.add_option("--help", action="help",
                          help="show this help message and exit")
        parser.set_defaults(verbosity=1)
        parser.add_option('-v', '--verbose', dest='verbosity',
                          action='store_const', const=2)
        parser.add_option('-q', '--quiet', dest='verbosity',
                          action='store_const', const=0)

        group = parser.add_option_group('Options for connecting to the manager')
        group.add_option('-h', '--host',
                          default=openvas.omplib.MANAGER_ADDRESS,
                          help="Connect to manager on host HOST (default: %default)")
        group.add_option('-p', '--port', type=int,
                          default=openvas.omplib.MANAGER_PORT,
                          help="Use port number PORT (default: %default)")
        group.add_option('-u', '--username', default=getpass.getuser(),
                          help="OMP username (default: current user's name)")
        group.add_option('-w', '--password',
                          help="OMP password (use '-' to be prompted, default: same as username)")

        opts, args = parser.parse_args(argv[1:])

        if not (0 < opts.port < 65536):
            parser.error('Manager port must be a number between 1 and 65535.')
        if opts.password is None:
            opts.password = opts.username
        elif opts.password == '-':
            opts.password = getpass.getpass('Enter password for openvas-manager: ')

        self.verbosity = int(opts.verbosity)
        OMPTestBase._OMP_HOST = opts.host
        OMPTestBase._OMP_PORT = opts.port
        OMPTestBase._OMP_USER = opts.username
        OMPTestBase._OMP_PASSWD = opts.password
        
        if len(args) == 0 and self.defaultTest is None:
            self.test = self.testLoader.loadTestsFromModule(self.module)
            return
        if len(args) > 0:
            self.testNames = args
        else:
            self.testNames = (self.defaultTest,)
        self.createTests()

if __name__ == '__main__':
    main()
