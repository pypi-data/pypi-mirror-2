import optparse
from eximloganalyzer.parser import Parser
from eximloganalyzer.report import TextReport

def main():
    optparser = optparse.OptionParser()
    optparser.add_option('-l', '--logfile', dest='logFile', default='/var/log/exim_mainlog', action='store', help='Specify log file location. Default is /var/log/exim_mainlog')
    optparser.add_option('-c', '--config', dest='configFile', default='/etc/eximloganalyzer.cfg', action='store', help='Specify config file location. Default is /etc/eximloganalyzer.cfg')
    
    (opts, args) = optparser.parse_args()
    
    p = Parser(opts.logFile, opts.configFile)
    report = p.parseLog()
    r = TextReport(report)
    print r.generateReport()

if __name__ == '__main__':
    main()