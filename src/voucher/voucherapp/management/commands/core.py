# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils import timezone

from voucherapp.models import Person, Voucher

import serial
import time
import logging
import csv 
import os

from django.utils.translation import get_language, activate
import datetime
from django.template.defaultfilters import date

import cups
from django.utils import timezone

import RPi.GPIO as GPIO
BUZZER_PIN = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

activate('cs')
logger = logging.getLogger()

def beep(num):
    for i in range(0, num): 
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        if i + 1 < num:
            time.sleep(0.25)
    
def exportFile(fname, logger=logging.getLogger()):

    logger.info('Exporting file {} ...'.format(fname))
    now = timezone.localtime(timezone.now()) - datetime.timedelta(1)
    path, file = os.path.split(fname)
    #fname = os.path.join(path, now.strftime('%Y%m%d_') + file)
    fname = os.path.join(path, now.strftime('%Y%m_') + file)

    try:
        f = open(fname, 'w')
    except Exception as e:
        logger.error(str(e))
        return

    with f:
        writer = csv.writer(f, delimiter = ';')
        
        #vouchers = Voucher.objects.filter(datetime__year=now.strftime('%Y'),datetime__month=now.strftime('%m'),datetime__day=now.strftime('%d'))
        vouchers = Voucher.objects.filter(datetime__year=now.strftime('%Y'),datetime__month=now.strftime('%m'))
        #vouchers = Voucher.objects.filter(datetime__range=[now, now + datetime.timedelta(hours=23)])
        
        for v in vouchers:
            data = [str(v.person), str(v.person.center), timezone.localtime(v.datetime).strftime("%Y-%m-%d %H:%M")]
            writer.writerow(data)
    
    logger.info('Export done.')    
     
def importFile(fname, logger=logging.getLogger()):

    logger.info('Importing file {} ...'.format(fname))
    
    try:
        f = open(fname, 'r')
    except Exception as e:
        logger.error(str(e))
        return 0

    Person.objects.all().update(rfid=None)
    
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
                
                personal_number = row[0]
                rfid = row[1]
                center = row[2]
                last_name = row[3]
                first_name = row[4]
                #note = 
                quantity = row[5]
                if quantity == '':
                    quantity = '0'
                #released = 
                #last_released = 
            except Exception as e:
                logger.warning(str(e) + ' DATA: ' + str(row))
                next 
                
            try:
                person = Person.objects.get(personal_number = personal_number)
                #logger.debug('Update Person: ' + str(row))
                person.rfid = rfid
                person.center = center
                person.quantity = quantity
                person.last_name = last_name
                person.first_name = first_name
                person.save()
            except:
                try:
                    #logger.debug('New Person: ' + str(row))
                    Person.objects.create(rfid = rfid, personal_number = personal_number, center = center, quantity = quantity, last_name = last_name, first_name = first_name)
                except Exception as e:
                    logger.error(str(e) + ' DATA: ' + str(row))
                    
    logger.info('Import done.')
                    
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
                
        now = timezone.now()
        if person.last_released == None or (person.last_released.year == now.year and person.last_released.month == now.month):
            #same month
            if person.quantity > person.released:
                #OK
                person.released = person.released + 1
                person.last_released = timezone.now()
                hasCredit = True
            else:
                #NOK
                hasCredit = False
                message = 'Překročen nárok!'
        else:
            #new month
            if person.quantity > 0:
                #OK
                person.released = 1
                person.last_released = timezone.now()
                hasCredit = True
            else:
                #NOK
                hasCredit = False
                message = 'Překročen nárok!'
                    
    except Exception as e:
        return (False, None, str(e), )
        
    return (hasCredit, person, message)     

def printFile(fname):
    logger.debug('Printing...') 
    
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
            data = '''********** TOKOZ® **********
Kupón do prádelny
{} {}
Osobní č.: {}
Středisko: {}
Vydáno   : {} z {}
Platnost : {} {}'''.format(person.first_name.encode('utf-8'), person.last_name.encode('utf-8'), str(person.personal_number).encode('utf-8'), str(person.center).encode('utf-8'), str(person.released).encode('utf-8'), str(person.quantity).encode('utf-8'), month, person.last_released.strftime('%Y').encode('utf-8')) #person.last_released.strftime('%B') #date(person.last_released, 'F')
        else:
            if person is not None:
                beep(2)
                data = '''********** TOKOZ® **********
Kupón do prádelny
{} {}
Osobní č.: {}
Středisko: {}
Překročen nárok!'''.format(person.first_name.encode('utf-8'), person.last_name.encode('utf-8'), str(person.personal_number).encode('utf-8'), str(person.center).encode('utf-8'), str(person.released).encode('utf-8'))
            else:
                beep(3)
                data = '''*********** TOKOZ® **********
Kupón do prádelny
Neznámé ID!'''
           
        print(data)
        
        if result[0]:
            beep(1)
            
            fname = 'print.txt'
            f = open(fname, 'w')
            f.write(data)
            f.close()
        
            if printer:
                return printFile(fname)
            else:
                return True
                
        return True
    
    except Exception as e:
            logger.error(str(e)) 
            return False
 
