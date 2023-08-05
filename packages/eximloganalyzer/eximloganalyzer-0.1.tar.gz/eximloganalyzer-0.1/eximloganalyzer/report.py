import datetime
import StringIO

class TextReport:
    """
    TextReport class
    Returns a report in plain-text
    """
    def __init__(self, report):
        if not report:
            raise Exception('Report is required')
        else:
            self.report = report
    
    def generateReport(self):
        """
        Loops through a result and generates a report
        """
        output = StringIO.StringIO()
        output.write("Exim Log Analyzer")
        print >>output, ("Generated on %s" % datetime.datetime.now()).rjust(63)
        print >>output,'-' * 80
        print >>output, ''
        
        for report in self.report.keys():
            print >>output, report
            print >>output, '-' * len(report)
            sortedResult = sorted([(value,key) for (key, value) in self.report[report].items()], reverse=True)
            for (times, result) in sortedResult[0:50]:
                output.write(result)
                print >>output, ("%s" % times).rjust(80 - len(result))
            print >>output, ''
        
        return output.getvalue()