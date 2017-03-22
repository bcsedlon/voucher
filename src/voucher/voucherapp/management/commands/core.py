# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils import timezone

from voucherapp.models import Person, Voucher

import serial
import time
import logging
import csv 

def printVoucher(person):
    print(person.personal_number)
    print(person.center)
    print(str(person.released) + ' / ' + str(person.quantity))
    return True
    return False

def importFile(fname, logger=logging.getLogger()):
    #logger = logging.getLogger()
    
    try:
        f = open(fname, 'r')
    except Exception as e:
        logger.error(str(e))
        #print(str(e))
        return 0

    with f:
        reader = csv.reader(f, delimiter = ';')
        for row in reader:
            #print(row)
            rfid = None
            personal_number = None
            center = None
            quantity  = None
                
            try:
                #0564-1-HPP;0800E807DD;601;1
                #rfid = int(row[1], 16)
                rfid = row[1]
                personal_number = row[0]
                center = row[2]
                #first_name = 
                #last_name = 
                #note = 
                quantity = row[3]
                #released = 
                #last_released = 
            except Exception as e:
                logger.warning(str(e) + ' DATA: ' + str(row))
                #print(str(e))
                next 
                
            try:
                person = Person.objects.get(personal_number = personal_number)
                person.rfid = rfid
                person.center = center
                person.quantity = quantity
                person.save()
            except:
                try:
                    Person.objects.create(rfid = rfid, personal_number = personal_number, center = center, quantity = quantity)
                except Exception as e:
                    logger.error(str(e) + ' DATA: ' + str(row))
                    #print(str(e))
                    
def saveVoucher(person):
    person.save()
    Voucher.objects.create(person=person, datetime=timezone.now())
        
def getPreparedPerson(rfid):
    try:
        hasCredit = False
        message = None
        person = Person.objects.get(rfid=rfid) 
                    
        #print(person)
        #print(person.last_released)
        #print(timezone.now().strftime("%Y-%m-%d %H:%M"))
                
        now = timezone.now()
        if person.last_released == None or (person.last_released.year == now.year and person.last_released.month == now.month):
            #same month
            if person.quantity > person.released:
                #OK
                person.released = person.released + 1
                person.last_released = timezone.now()
                    
                #person.save()
                #Voucher.objects.create(person=person, datetime=timezone.now())
                    
                hasCredit = True
                #issued = True
                #print('OK\t' + str(person.released) + '/' +  str(person.quantity))
            else:
                #NOK
                hasCredit = False
                message = 'Překročen nárok.'
                #print('NOK\t' + str(person.released) + '/' +  str(person.quantity))    
                    
        else:
            #new month
            if person.quantity > 0:
                #OK
                person.released = 1
                person.last_released = timezone.now()
                #person.save()
                #Voucher.objects.create(person=person, datetime=timezone.now())
                hasCredit = True
                #print('OK\t' + str(person.released) + '/' +  str(person.quantity))
            else:
                #NOK
                hasCredit = False
                message = 'Překročen nárok.'
                #print('NOK\t' + str(person.released) + '/' +  str(person.quantity))
                    
    except Exception as e:
        hasCredit = False
        #print(e)
        return (hasCredit, None, str(e), )
        
    return (hasCredit, person, message)      
        

class Command(BaseCommand):
    help = 'core'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            default = '',
            help = 'Path and filename of imported file.',            
        )  

    #logger = logging.getLogger()

        
    def handle(self, *args, **options):
        
        logger = logging.getLogger()
        
        port = 'COM2'
        baud = 9600
        #ser = serial.Serial(port, baud, timeout=0)
        
        try:
            ser = serial.Serial(port, baud, timeout=None)
        except Exception as e:
            logger.error(str(e))
            #return
        
        rfid_last = 0
        rfid_datetime = 0
        
        print('READY')
        
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
            rfid = '08004B6C2A'
            
            if rfid_datetime + 5 < int(time.time()):
                rfid_last = 0
        
            if rfid > 0 and rfid_last <> rfid:
                print('')
                
                rfid_last = rfid
                rfid_datetime = int(time.time())

                #rfid = 458
                #EA00022F7ABD 257285757565629
            
                try:
                    person = Person.objects.get(rfid=rfid) 
                
                    #issued = False
                
                    
                    print(person)
                    #print(person.last_released)
                    print(timezone.now().strftime("%Y-%m-%d %H:%M"))
                
                    now = timezone.now()
                
                    if person.last_released == None or (person.last_released.year == now.year and person.last_released.month == now.month):
                        #same month
                        if person.quantity > person.released:
                            #OK
                            person.released = person.released + 1
                            person.last_released = timezone.now()
                            person.save()
                            Voucher.objects.create(person=person, datetime=timezone.now())
                            #issued = True
                            print('OK\t' + str(person.released) + '/' +  str(person.quantity))
                        else:
                            #NOK
                            print('NOK\t' + str(person.released) + '/' +  str(person.quantity))    
                    
                    else:
                        #new month
                        if person.quantity > 0:
                            #OK
                            person.released = 1
                            person.last_released = timezone.now()
                            person.save()
                            Voucher.objects.create(person=person, datetime=timezone.now())
                            #issued = True
                            print('OK\t' + str(person.released) + '/' +  str(person.quantity))
                        else:
                            #NOK
                            print('NOK\t' + str(person.released) + '/' +  str(person.quantity))
                    
                            
                except Exception as e:
                    print(e)
                    
                print('')

        return 0
