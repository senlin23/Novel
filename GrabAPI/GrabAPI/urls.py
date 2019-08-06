"""
Definition of urls for GrabAPI.
"""

from django.conf.urls import include, url
import GrabAPI
import QD.views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', GrabAPI.views.home, name='home'),
    # url(r'^GrabAPI/', include('GrabAPI.GrabAPI.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^GetAllInfo',QD.views.GetAllInfo,name='GetAllInfo'),
    url(r'^GetInfoDetail/',QD.views.GetInfoDetail,name='GetInfoDetail'),
    url(r'^GetChapterList/',QD.views.GetChapterList,name='GetChapterList'),
    url(r'^GetContent/',QD.views.GetContent,name='GetContent')
]
