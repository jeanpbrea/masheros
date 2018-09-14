from django.conf.urls import url
from . import views

urlpatterns = [
    # admin page url
    url(r'^admin$', views.admin),
    # user urls
    url(r'^$', views.home),
    url(r'^log$', views.log),
    url(r'^signup$', views.signup),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logoff$', views.logoff),
    url(r'^dashboard/(?P<u_id>\d+)$', views.dashboard),
    url(r'^reviewcreate$', views.reviewcreate),
    url(r'^review$', views.review),
    url(r'^update/(?P<r_id>\d+)$', views.update),
    url(r'^reviewedit/(?P<r_id>\d+)$', views.reviewedit),
    url(r'^deletereview/(?P<r_id>\d+)$', views.deletereview),
    url(r'^deleteuser/(?P<u_id>\d+)$', views.deleteuser),
    url(r'^showreview/(?P<r_id>\d+)$', views.showreview),
    url(r'^create_comment/(?P<r_id>\d+)$', views.create_comment)
]
