# -*- coding: utf-8 -*-

import ConfigParser
import os.path

class Config(object):
    """
    Wrapper for configuration settings
    """

    # Command names
    calibredb = "calibredb"
    pdftotext = "pdftotext"
    catdoc = "catdoc"
    djvutxt = "djvutxt"
    archmage = "archmage"

    # Extra params
    guess_lead_pages = 10  # Pages where we look for ISBN (in page-oriented docs)
    guess_lead_lines = 10000 # Lines where we look for ISBN (in not-page oriented docs)

    # Reporting
    progress_report_every = 50 # Every that many files progress note is sent

    def __init__(self, inifile = "~/.calibre-utils"):
        """
        Ładuje parametry z zadanego pliku konfiguracyjnego, zarazem uzupełnia lub tworzy
        go jeśli go brakowało.
        """

        COMMANDS_SECTION = "commands"
        ISBN_SECTION = "isbn-search"

        config = ConfigParser.SafeConfigParser({})

        ini = os.path.abspath(os.path.expanduser(inifile))
        if os.path.exists(ini):
            config.read(ini)

        for section in [COMMANDS_SECTION, ISBN_SECTION]:
            if not config.has_section(section):
                config.add_section(section)

        config_changed = False

        for cmdopt in ["calibredb", "pdftotext", "catdoc", "djvutxt", "archmage"]:
            if config.has_option(COMMANDS_SECTION, cmdopt):
                setattr(self, cmdopt, config.get(COMMANDS_SECTION, cmdopt))
            else:
                config_changed = True
                config.set(COMMANDS_SECTION, cmdopt, getattr(self, cmdopt))

        for cmdopt in ["guess_lead_pages", "guess_lead_lines"]:
            if config.has_option(ISBN_SECTION, cmdopt):
                setattr(self, cmdopt, config.getint(ISBN_SECTION, cmdopt))
            else:
                config_changed = True
                config.set(ISBN_SECTION, cmdopt, str(getattr(self, cmdopt)))
        
        if config_changed:
            config.write(open(ini, 'w'))


_config = None
def standard_config():
    global _config
    if not _config:
        _config = Config()
    return _config

# TODO: report missing tools and suggest how to install them
