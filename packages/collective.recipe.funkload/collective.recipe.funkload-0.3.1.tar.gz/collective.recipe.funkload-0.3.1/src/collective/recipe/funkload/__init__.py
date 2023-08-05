# -*- coding: utf-8 -*-
from zc.recipe.egg import Scripts
import os

class TestRunner(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        self.test_url = self.options.get('url')
        if not self.test_url:
            raise KeyError, "You must specify an address to test"

        default_location = os.path.join(self.buildout['buildout'].get('directory'),'var','funkload','data')
        default_report_destination = os.path.join(self.buildout['buildout'].get('directory'),'var','funkload','reports')
        default_record_output = os.path.join(self.buildout['buildout'].get('directory'),'var','funkload','records')
        
        self.location = self.options.get('location',default_location)
        self.report_destination = self.options.get('report_destination',default_report_destination)
        self.record_output = self.options.get('record_output',default_record_output)
        self.record_test_name = self.options.get('record_test_name', 'SimpleRecord')
        self.record_proxy_port = self.options.get('record_proxy_port', 8090)

        eggs = self.options.get('eggs', 'funkload\ncollective.funkload\ncollective.recipe.funkload' )
        required_eggs = ['funkload', 'collective.funkload', 'collective.recipe.funkload']
        for egg in required_eggs:
            if egg not in eggs:
                eggs = '\n'.join([eggs, egg])

        options_funkload = {'eggs': eggs,
                            'scripts':'funkload',
                            'arguments':'url="%s",buildout_dir="%s",report_destination="%s",data_destination="%s",record_output="%s",record_test_name="%s",record_proxy_port="%s"' \
                                % (self.test_url,
                                   self.buildout['buildout'].get('directory'),
                                   self.report_destination,
                                   self.location,
                                   self.record_output,
                                   self.record_test_name,
                                   self.record_proxy_port,
                                   )}

        if 'python' in options:
            options_funkload.update({'python':options['python']})
        
        self._recipe = Scripts(buildout,name,options_funkload)


    def install(self):
        """Installer"""
        
        if not os.path.exists(self.location):
            os.makedirs(self.location)
        
        return self._recipe.install()

