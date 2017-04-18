# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from voucherapp.models import Person

import logging
  
import core

logger = logging.getLogger()

'''
class NullLogger:
    #log = []
    def error(self, msg):
        pass
        #self.log.append('ERROR: ' + msg)
    def warning(self, msg):
        pass
        #self.log.append('WARNING: ' + msg)
    def info(self, msg):
        pass
        #self.log.append('INFO: ' + msg
'''
         
class Command(BaseCommand):
    help = 'import'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            default = None,
            help = 'Path and filename of imported file.',            
        )                        
        
    def handle(self, *args, **options):
        fname = str(options['file'])
        #nl = NullLogger()
        #core.importFile(fname, nl)
        #Person.objects.all().update(rfid=None)
        core.importFile(fname)
        
