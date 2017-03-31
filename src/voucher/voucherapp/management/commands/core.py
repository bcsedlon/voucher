# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils import timezone

from voucherapp.models import Person, Voucher

import serial
import time
import logging
import csv 

from django.utils.translation import get_language, activate
import datetime
from django.template.defaultfilters import date

import cups
from django.utils import timezone

activate('cs')
logger = logging.getLogger()


    
'''
def printVoucher(person):
    print(person.personal_number)
    print(person.center)
    print(str(person.released) + ' / ' + str(person.quantity))
    return True
    return False
'''
def exportFile(fname, logger=logging.getLogger()):
    #logger = logging.getLogger()
    '''
    with open(fname, 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=';')
    data = [['Me', 'You'],
            ['293', '219'],
            ['54', '13']]
    a.writerows(data)
    return
    '''
    try:
        f = open(fname, 'w')
    except Exception as e:
        logger.error(str(e))
        return

    with f:
        writer = csv.writer(f, delimiter = ';')
        
        vouchers = Voucher.objects.filter()
        
        
        for v in vouchers:
            #now = timezone.localtime(timezone.now())
            #print(now.strftime("%Y-%m-%d %H:%M"))
            data = [str(v.person), str(v.person.center), timezone.localtime(v.datetime).strftime("%Y-%m-%d %H:%M")]
            #print(data)
        
            writer.writerow(data)
        
        
        '''
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
        '''
                    
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
        return getPreparedPerson2(person)
    except Exception as e:
        logger.error(str(e)) 
        return (False, None, str(e), )
        
def getPreparedPerson2(person):
    try:
        hasCredit = False
        message = None
        #person = Person.objects.get(rfid=rfid) 
                    
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
                message = 'Překročen nárok!'
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
                message = 'Překročen nárok!'
                #print('NOK\t' + str(person.released) + '/' +  str(person.quantity))
                    
    except Exception as e:
        #print(e)
        return (False, None, str(e), )
        
    return (hasCredit, person, message)     

def printFile(fname):
    logger.debug('Printing...') 
    #print('PRINTER')
    #return True
    
    try:
        conn = cups.Connection ()
        printers = conn.getPrinters ()
            
        for printer in printers:
            #logger.debug('{0} {1}'.format(printer, printers[printer]['device-uri']))
            pass
            
        printid =conn.printFile(printer, fname, 'voucher', {})

        while conn.getJobs().get(printid, None) is not None:
            time.sleep(1)
     
        
    
    except Exception as e:
            logger.error(str(e)) 
            return False
    
    logger.debug('Printing done.')
    return True
 
def printResult(result, printer=True):
    activate('cs')
    try:
        person = result[1]
        if result[0]:
            month = date(person.last_released, 'F').encode('utf-8')
            data = '''Osobní č.: {}
Středisko: {}
Vydáno   : {} z {}
Měsíc    : {} {}'''.format(str(person.personal_number), person.center, str(person.released), str(person.quantity), month, person.last_released.strftime('%Y')) #person.last_released.strftime('%B') #date(person.last_released, 'F')
        else:
            if person is not None:
                data = '''Osobní č.: {}
Středisko: {}
Překročen nárok!'''.format(str(person.personal_number), person.center, str(person.released))
            else:
                data = '''Neznáme ID!'''
    
        print(data)
        
        fname = 'print.txt'
        f = open(fname, 'w')
        f.write(data)
        f.close()
        
        if printer:
            return printFile(fname)
        else:
            return True
    
    except Exception as e:
            logger.error(str(e)) 
            return False
    
   
def printVoucherXXX(person): #conn, printer, person):
    try:
        conn = cups.Connection ()
        printers = conn.getPrinters ()
            
        for printer in printers:
            #logger.debug('{0} {1}'.format(printer, printers[printer]['device-uri']))
            pass
            
    #except Exception as e:
    #logger.error(str(e)) 
    #return   
    #try:
        month = date(person.last_released, 'F').encode('utf-8')
        #print(month)
        #data = '{0}\n{1}\n{2}/{3}\n{4}'.format(str(person.personal_number), person.center, str(person.released), str(person.quantity), 'f')
        data = '''Osobní č.: {}
Středisko: {}
Vydáno   : {} z {}
Měsíc    : {} {}'''.format(str(person.personal_number), person.center, str(person.released), str(person.quantity), month, person.last_released.strftime('%Y')) #person.last_released.strftime('%B') #date(person.last_released, 'F')
        print(data)
        
        return True
        
        f = open('print.txt', 'w')
        f.write(data)
        f.close()
        printid =conn.printFile(printer, 'print.txt', 'voucher', {})

        while conn.getJobs().get(printid, None) is not None:
            time.sleep(1)
                
    except Exception as e:
            logger.error(str(e)) 
            return False
    
    return True
        
class Command25(BaseCommand):
    help = 'core'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            default = '',
            help = 'Path and filename of imported file.',            
        )  

    #logger = logging.getLogger()
        
    def handle(self, *args, **options):
        
        activate('cs')
            
        #logger = logging.getLogger()
        
        '''
        printer = None
        conn = None
        try:
            conn = cups.Connection ()
            printers = conn.getPrinters ()
            
            for printer in printers:
                logger.debug('{0} {1}'.format(printer, printers[printer]['device-uri']))
            #printer = printers[0]
            
        except Exception as e:
            logger.error(str(e)) 
            return
        '''
            
        #port = 'COM2'
        #baud = 9600
        port = '/dev/ttyUSB0'
        baud = 4800
        
        try:
            ser = serial.Serial(port, baud, timeout=None)
        except Exception as e:
            logger.error(str(e))
            return
        logger.debug(ser)
        
        rfid_last = 0
        rfid_datetime = 0
        
        logger.debug('READY')
        
        while True:
            
            #time.sleep(0.1)
            #print('COM2')
            #data = ser.read()
            data = ser.readline().decode()
            #print(data)
            '''
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
            #rfid = '08004B6C2A'
            rfid = data.replace('\n', '').replace('\r', '')
            
            if rfid_datetime + 5 < int(time.time()):
                rfid_last = 0
        
            if rfid <> '' and rfid_last <> rfid:
                logger.debug('RFID: ' + rfid)
                #print('X')
                
                rfid_last = rfid
                rfid_datetime = int(time.time())

                #rfid = 458
                #EA00022F7ABD 257285757565629
                #rfid = 'CF0073D02C'
                #print('RFID: ' + rfid)
            
                try:
                

                        
                    #person = Person.objects.get(rfid=rfid) 
                    #person = Person.objects.get(rfid__contains=rfid[2:])
                    person = Person.objects.get(rfid__iendswith=rfid[2:]) 

                    result = getPreparedPerson2(person)
                    logger.debug(person)
                    if result[0]:
                        if(printVoucher(result[1])):
                            saveVoucher(result[1])
                        #else:
                        #    result = (False, person, 'Chyba tiskárny.')                    

                    '''
                    logger.debug(person)
                    now = timezone.localtime(timezone.now())
                    #print(now.strftime("%Y-%m-%d %H:%M"))
                    logger.debug(now)
                    
                    if person.last_released == None or (person.last_released.year == now.year and person.last_released.month == now.month):
                        #same month
                        if person.quantity > person.released:
                            #OK
                            logger.debug('OK\t' + str(person.released) + '/' +  str(person.quantity))
                            #if printVoucher(conn, printer, person):
                            if printVoucher(person):
                                person.released = person.released + 1
                                person.last_released = timezone.now()
                                person.save()
                                Voucher.objects.create(person=person, datetime=timezone.now())
                        else:
                            #NOK
                            logger.debug('NOK\t' + str(person.released) + '/' +  str(person.quantity))    
                    
                    else:
                        #new month
                        if person.quantity > 0:
                            #OK
                            logger.debug('OK\t' + str(person.released) + '/' +  str(person.quantity))
                            #if printVoucher(conn, printer, person):
                            if printVoucher(person):
                                person.released = 1
                                person.last_released = timezone.now()
                                person.save()
                                Voucher.objects.create(person=person, datetime=timezone.now())
                        else:
                            #NOK
                            logger.debug('NOK\t' + str(person.released) + '/' +  str(person.quantity))
                    '''
                    
                except Exception as e:
                    #print(str(e))
                    logger.error(str(e)) 

        return 
