# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from voucherapp.models import Person, Voucher

import logging
import serial
import time
  
import core

logger = logging.getLogger()
 
class Command(BaseCommand):
    help = 'run'

    def add_arguments(self, parser):
        parser.add_argument(
            '--port',
            default = '/dev/ttyUSB0',
            help = 'RFID reader port.',            
        )                        
    
    def handle(self, *args, **options):
                
        port = str(options['port'])
        baud = 4800

        try:
            ser = serial.Serial(port, baud, timeout=None)
        except Exception as e:
            logger.error(str(e))
            return
        
        rfid_last = 0
        rfid_datetime = 0
        
        logger.debug(port)

        
        while True:
            '''
            #time.sleep(0.1)
            #print('COM2')
            #data = ser.read()
            #data = ser.readline()#.decode()
            #print(data)
            ID = ''
            rfid = 0
            read_byte = ser.read()
            if read_byte == '\x02':
                for counter in range(12):
                    read_byte = ser.read()
                    ID = ID + str(read_byte)
                    #rfid = rfid + ord(read_byte) > 2 ^ counter
                    #print hex(ord( read_byte))
                print(ID)
                #print(int(ID, 16))
                
                rfid = int(ID, 16)
                print(rfid)
            
            #print(rfid_datetime)
            #print(int(time.time()))
            #print('')
            '''
            #EA00022F7ABD 257285757565629
            #rfid = '08004B6C2A'
            #rfid = '08006D29AB'
            
            data = ser.readline().decode()
            rfid = data.replace('\n', '').replace('\r', '')
            
            if rfid_datetime + 5 < int(time.time()):
                rfid_last = 0
        
            if rfid > 0 and rfid_last <> rfid:
                
                logger.debug('RFID: ' + rfid)
                rfid_last = rfid
                rfid_datetime = int(time.time())

                #result = core.getPreparedPerson(rfid)
                try:
                    try:
                        person = Person.objects.get(rfid__iendswith=rfid[2:]) 
                        result = core.getPreparedPerson2(person)
                    except Exception as e:
                        result =  (False, None, str(e), )
                    logger.debug('{}, {}, {}'.format(result[0], result[1], result[2] ))
                
                    #if result[0]:
                        #if core.printVoucher(result[1]):
                    if core.printResult(result):
                        if result[0]:
                            core.saveVoucher(result[1])
                
                except Exception as e:
                    logger.error(str(e))    
            
            ser.flushInput()
            time.sleep(0.1)

        return
        
