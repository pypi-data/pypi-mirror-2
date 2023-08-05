import os, re
from eximloganalyzer.config import Config

class Parser:
    """
    Parser class
    Handles the parsing of the log file.
    """
    def __init__(self, log='/var/log/exim_mainlog', config='/etc/eximlogparser.cfg'):
        """
        Requires the path to the exim log file and the path to the config file.
        Raises IOError if unable to open either one
        """
        if os.path.exists(log):
            self.log = log
        else:
            raise IOError('Unable to open log')
        
        if os.path.exists(config):
            self.config = Config(config)
        else:
            raise IOError('Unable to open config')
    
    def parseRules(self):
        """
        Gets the rules from the config module.
        Loops through the rules and builds each one
        """
        rules = {}
        for rule in self.config.getRules():
            r = self.buildRule(rule)
            rules[r[0]] = r[1]
        return rules
    
    def buildRule(self, rule):
        """
        Builds individual rules.
        Tries to parse the format from the config file, compile the regular expression
        and eval the tuple.
        """
        try:
            ruleTitle = rule[0]
            (ruleRegex, ruleMatch) = eval(rule[1])
            ruleRegex = re.compile(ruleRegex)
            return (ruleTitle, (ruleRegex, ruleMatch))
        except:
            raise Exception('Unable to parse rule: %s' % ruleTitle)
    
    def parseLog(self):
        """
        Loops through the exim log file.
        It compares each line against each rule.
        If a match is found, it tallies the score
        """
        rules = self.parseRules()
        report = {}
        try:
            log = open(self.log)
        except:
            raise Exception('Unable to open log file')
        for line in log:
            for ruleTitle in rules.keys():
                if not ruleTitle in report:
                    report[ruleTitle] = {}
                match = rules[ruleTitle][0].match(line)
                if match:
                    m = match.expand(rules[ruleTitle][1])
                    if m in report[ruleTitle]:
                        report[ruleTitle][m] += 1
                    else:
                        report[ruleTitle][m] = 1
        return report