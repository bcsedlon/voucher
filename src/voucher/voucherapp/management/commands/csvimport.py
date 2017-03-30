# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

import logging
  
import core

logger = logging.getLogger()
 
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
        core.importFile(fname)
        
