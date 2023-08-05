import unittest
from eximloganalyzer.parser import Parser

class ParserTestsBasic(unittest.TestCase):
    """Tests basic init of the Parser"""
    
    def setUp(self):
        self.configFile = 'tests/eximloganalyzer.cfg'
        self.logFile = 'tests/exim_mainlog.txt'
    
    def testParserLogOpenPass(self):
        """Tests if Parser can open the log file"""
        self.failUnless(Parser(log=self.logFile, config=self.configFile))
    
    def testParserLogOpenFail(self):
        """Tests if Parser can fail when log is not found"""
        self.assertRaises(IOError, Parser, 'Idontexist.txt', self.configFile)
    
    def testParserConfigOpenFail(self):
        """Tests if Parser can fail when config is not found"""
        self.assertRaises(IOError, Parser, self.logFile, 'Idontexist.txt')

class ParserParsing(unittest.TestCase):
    """Tests parsing capabilities of the Parser"""
    
    def setUp(self):
        self.configFile = 'tests/eximloganalyzer.cfg'
        self.logFile = 'tests/exim_mainlog.txt'
    
    def testParserParseRules(self):
        """Tests if Parser can parse the rules"""
        p = Parser(self.logFile, self.configFile)
        rules = p.parseRules()
        self.assertEqual('tuple', rules['Outgoing via Cron'].__class__.__name__)
    
    def testParserParseRulesFail(self):
        """Tests if Parser can fail when bad rule is found"""
        p = Parser(self.logFile, self.configFile)
        badRule = 'Outgoing via Cron: (\'<= (.+?) U=(.+?) P=local S=(.+?) T="Cron\', $2)'
        self.assertRaises(Exception, p.buildRule, badRule)

    def testParserParseLog(self):
        """Tests if Parser can parse the log file"""
        p = Parser(self.logFile, self.configFile)
        report = p.parseLog()
        self.assertEqual(report['Outgoing via Cron']['user1'], 1)
        self.assertEqual(report['Outgoing via Cron']['user2'], 1)