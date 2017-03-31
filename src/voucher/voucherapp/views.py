# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

import os
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

#from management.commands.rfid import Machine
#from management.commands.importFile import ImportMachine

from .forms import RFIDForm

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import management.commands.core

class StrLogger:
    log = []
    def error(self, msg):
        self.log.append('ERROR: ' + msg)
    def warning(self, msg):
        self.log.append('WARNING: ' + msg)
 
@login_required(login_url='/accounts/login/')      
def upload(request):
    
    if request.method == 'POST':
        filepath = request.FILES.get('filepath', False) 
        if filepath:
            fs = FileSystemStorage()
            filename = fs.save(filepath.name, filepath)
            uploaded_file_url = fs.url(filename)
                
            strLogger = StrLogger()
            strLogger.log = []
                    
            #importMachine = ImportMachine()
            #importMachine.importFile(uploaded_file_url, strLogger)
            management.commands.core.importFile(uploaded_file_url, strLogger)

            fs.delete(filename)
                
            return render(request, 'voucherapp/upload.html', {
                'uploaded_file_url': uploaded_file_url,
                'error_messages': strLogger.log,
            })
    
    return render(request, 'voucherapp/upload.html')
     
@login_required(login_url='/accounts/login/')
def simulate(request, rfid = 0):
   
    if request.method == 'POST': # and 'submit' in request.POST:
        form = RFIDForm(request.POST)
    else:
        form  = RFIDForm()
    
    if not form.is_valid():
        rfid = 0
    else:
        person = form.cleaned_data['person']
        if person == None:
            rfid = 0
        else:
            rfid = person.rfid
   
    #machine = Machine()     
    #result = machine.getPreparedPerson(rfid)
    result = management.commands.core.getPreparedPerson(rfid)
 
    '''
    if result[0]:
        #print('PRINT') 
        #machine.saveVoucher(result[1])
        #logger.debug('PRINT')
        
        #if(management.commands.core.printVoucher(result[1])):
        if management.commands.core.printResult(result):
            management.commands.core.saveVoucher(result[1])
        else:
            result = (False, person, 'Chyba tiskárny.')
    '''
    if rfid <> 0:
        if management.commands.core.printResult(result):
            if result[0]:
                management.commands.core.saveVoucher(result[1])
        else:
            result = (False, result[1], 'Chyba tiskárny!')
    else:
        result = (False, result[1], 'Neznáme ID!')
            
    context = {
        'result': result[0],
        'person': result[1],
        'form' : form,
        'message' : result[2],
    }
            
    return render(request, 'voucherapp/simulate.html', context)
 
#@user_passes_test(lambda u: u.is_superuser, login_url='archaapp:login')
#@login_required(login_url='auth_views:login')
@login_required(login_url='/accounts/login/')
def logfile(request):
    filename = 'logfile'
    SITE_ROOT = os.path.abspath(os.path.dirname(__name__))
    
    filefullpath = os.path.join(SITE_ROOT, filename)

    try:  
        import tempfile
        with open(tempfile.mktemp(), 'w') as tf:
            try:
                with open(filefullpath + '.1') as flog:
                    tf.write(flog.read())
            except:
                pass
            with open(filefullpath) as flog:
                tf.write(flog.read())
      
        wrapper = FileWrapper(open(tf.name, 'rb'))
       
        response = HttpResponse(wrapper, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = 'inline; filename={0}'.format(filename + '.txt')
        response['Content-Length'] = os.path.getsize(tf.name)
        
        os.remove(tf.name)
        return response

    except Exception as e:
        response = 'Log neni dostupny!<br>Zkontrolujete logfile<br>tail -f logfile<br>Chyba: {0} {1}'.format(str(e), filefullpath)
        return HttpResponse(response)
