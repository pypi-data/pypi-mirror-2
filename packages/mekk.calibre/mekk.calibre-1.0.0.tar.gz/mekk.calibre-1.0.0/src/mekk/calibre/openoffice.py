# -*- coding: utf-8 -*-

import ootools, uno

# Workaround for a bug in ootools
from com.sun.star.beans import PropertyValue
ootools.PropertyValue = PropertyValue

class Doc2RtfConverter(object):

    def __init__(self):
        self.runner = None
        self.desktop = None

    def convert(self, input_file, output_file):
        self._ensure_active()
        input_url = uno.systemPathToFileUrl(os.path.abspath(input_file))
        output_url = uno.systemPathToFileUrl(os.path.abspath(output_file))
        props = ootools.oo_properties(FilterName="Rich Text Format")
        #desktop = self.runner.connect()
        document = self.desktop.loadComponentFromURL(
            input_url, "_blank", 0, ootools.oo_properties())
        try:
            document.storeToURL(output_url, props)
        finally:
            document.close(True)

    def _ensure_active(self):
        if not self.runner:
            print "Starting up OpenOffice"
            self.runner = ootools.OORunner()
            self.runner.start()
            self.desktop = self.runner.connect()

    def __del__(self):
        if self.runner:
            print "Shutting down OpenOffice"
            self.runner.stop()

doc2rtf_converter = Doc2RtfConverter()


#where = "%s/tmp" % os.environ['HOME']
#doc2rtf_converter.convert(os.path.join(where, "test.doc"),
#                  os.path.join(where, "test.rtf"))

