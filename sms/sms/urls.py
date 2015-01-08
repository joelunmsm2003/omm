from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^reportes/', 'base_sms.views.reportes', name='reporte'),
	url(r'^reportes_x/', 'base_sms.views.reportes_x', name='reporte'),
 	url(r'^logeate/', 'base_sms.views.logeate', name='reporte'),
	url(r'^push$', 'base_sms.views.push'),
	url(r'^seleccionar$', 'base_sms.views.select'),
	url(r'^csv/$', 'base_sms.views.csv_x'),
	url(r'^salir/', 'base_sms.views.salir'),
	url(r'^contact/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/$', 'base_sms.views.contact'),

)
