import ConfigParser, os

class Config:
    """
    Config class
    Handles the config file and returns the rule section
    """
    def __init__(self, configFile):
        """
        Takes the path to a config file as an argument.
        Raises IOError if the file does not exist
        """
        self.config = ConfigParser.RawConfigParser()
        self.config.optionxform = str
        if os.path.exists(configFile):
            self.config.read(configFile)
        else:
            raise IOError('Unable to open config file')
    
    def getRules(self):
        """
        Tries to return the [rules] section of the config file
        """
        try:
            return self.config.items('rules')
        except ConfigParser.NoSectionError:
            return False
            