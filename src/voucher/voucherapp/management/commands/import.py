# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

import logging
  
import core
 
class Command(BaseCommand):
    help = 'import'

    
    def add_arguments(self, parser):
        #parser.add_argument('--file', nargs='+', type=str)
        
        parser.add_argument(
            '--file',
            default = None,
            help = 'Path and filename of imported file.',            
        )                        
    
        
    def handle(self, *args, **options):
        #logger = logging.getLogger()
        
        fname = str(options['file'])
        core.importFile(fname)
        
