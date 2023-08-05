exim log analyzer
=================

This is a set of modules as well as a cli-frontend that can be used to
gather statistics from an exim_mainlog file.

Statistics are collected via rules made in a config file. The config 
file uses the format:

    [rules]
    Rule Name: ('regex (.+) here', 'String \\1 to return')

Where \\1 is the captured regex (.+). There are several examples of
rules in the tests/eximloganalyzer.cfg file.

Once configured, you can either use the cli.py file directly or the
eximloganalyzer file created by setuptools:

    eximloganalyzer --logfile=/path/to/exim_mainlog --config=file.cfg

Defaults for file locations are:

  * Logfile: /var/log/exim_mainlog
  * Config: /etc/eximloganalyzer.cfg
