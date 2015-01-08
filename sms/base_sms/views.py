from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login,logout
from django.core import serializers
import simplejson
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
from base_sms.models import DSms
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from base_sms.models import ContactForm
from datetime import date




def my_view(request):

	user = authenticate(username='root', password='123')
	print user
	return HttpResponse(user) 


def push(request):

	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponse(simplejson.dumps('Login')) 
		else:
			return HttpResponse(simplejson.dumps('Desactivado')) 
	else:
		return HttpResponse(simplejson.dumps('Usuario Incorrecto'))

#@login_required
def select(request):

	mes = request.POST['mes']
	print mes
	sms = DSms.objects.filter(fecha__month=mes)
	print sms
 	data = serializers.serialize("json",sms)
 	return HttpResponse(data)

def contact(request,ax,mx,dx,ay,my,dy):

	print 'post.....'
	form = ContactForm(request.POST) # A form bound to the POST dat

	if((dy==dx) and (mx==my)):
		dy=int(dx)+1


	fechax = str(ax)+"-"+str(mx)+"-"+str(dx)
	fechay = str(ay)+"-"+str(my)+"-"+str(dy)

	fecha_f = datetime.datetime.strptime(fechax,"%Y-%m-%d")
	fecha_fy = datetime.datetime.strptime(fechay,"%Y-%m-%d")



	print fecha_f
	print fecha_fy

	anio = str(fecha_f.strftime('%Y'))
	mes = str(fecha_f.strftime('%m'))
	dia = str(fecha_f.strftime('%d'))

	anioy = str(fecha_fy.strftime('%Y'))
	mesy = str(fecha_fy.strftime('%m'))
	diay = str(fecha_fy.strftime('%d'))


	contact_list = DSms.objects.filter(fecha__lte=fecha_fy,fecha__gte=fecha_f,cliente='OMMM')
#contact_list = DSms.objects.filter(fecha__year=anio,fecha__month=mes,fecha__day=dia,cliente='OMMM').order_by('-fecha')

#num_reg = DSms.objects.filter(fecha__year=anio,fecha__month=mes,fecha__day=dia,cliente='OMMM').count()
	num_reg = DSms.objects.filter(fecha__lte=fecha_fy,fecha__gte=fecha_f,cliente='OMMM').count()

	nfile="Reporte"+str(anio)+str(mes)+str(dia)+".csv"
	filex="/var/www/"+nfile
	text_file = open(filex, "w")

	text_file.write("id,fechadb,fecha,ip,dst,msg,status,detail,cliente"+str(chr(10)))

	for x in contact_list:

	#print x.msg
		msg = x.msg.encode("latin-1")

		msg =str(msg)

		msg= msg.replace(",", " ");
	
		text_file.write(str(x.id)+','+str(x.fechadb)+','+str(x.fecha)+','+ str(x.ip)+','+ str(x.dst)+','+msg+','+str(x.status)+','+str(x.detail)+','+str(x.cliente)+str(chr(10)))
	
	text_file.close()



	paginator = Paginator(contact_list, 200) # Show 25 contacts per page

	page = request.GET.get('page')

	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
    # If page is not an integer, deliver first page.
		contacts = paginator.page(1)
	except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
		contacts = paginator.page(paginator.num_pages)

	form = ContactForm()
#return render_to_response('contact.html', {"contacts": contacts,'form':form})
	

	fechax=str(fecha_f)
	fechax=fechax.split(' 00')
	fechax = fechax[0]

	fechay=str(fecha_fy)
	fechay=fechay.split(' 00')
	fechay = fechay[0]

	#contacts = [name.encode("latin-1") for name in DSms.objects.filter(fecha__month=mes,cliente='OMMM').values_list('msg', flat=True)]
	return render(request, 'contact.html', {'fechay':fechay,'fechax':fechax,'num_reg':num_reg,'nfile':nfile,'form': form,"contacts":contacts,})


	#return HttpResponse(contacts) 





	

def salir(request):

	logout(request)

	return render_to_response('logeate.html', context_instance=RequestContext(request))

def logeate(request):
 
	return render_to_response('logeate.html', context_instance=RequestContext(request))



#@login_required
def csv_x(request):
    # Create the HttpResponse object with the appropriate CSV header.



	
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="somefile.csv"'
	writer = csv.writer(response)
	writer.writerow(['id', 'fechadb', 'fecha', 'ip', 'dst','msg','status','detail','cliente'])
	
	for x in sms:
		writer.writerow([x.id, x.fechadb, x.fecha, x.ip, x.dst,x.msg,x.status,x.detail,x.cliente])
	return response

#@login_required
def reportes(request):
 
	sms = DSms.objects.all()

	#return render_to_response('reportes.html',{'sms':sms})
	
	return render_to_response('contact.html',context_instance=RequestContext(request))



def reportes_x(request):
	
    contact_list = DSms.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render_to_response('list.html', {"contacts": contacts})

