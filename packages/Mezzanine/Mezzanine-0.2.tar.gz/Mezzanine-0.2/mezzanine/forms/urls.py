

from django.conf.urls.defaults import patterns, url
from mezzanine.forms.views import built_form_detail, built_form_sent

urlpatterns = patterns("",
    url(r'(?P<slug>.*)/sent/$', built_form_sent, name="form_sent"),
    url(r'(?P<slug>.*)/$', built_form_detail, name="form_detail"),
)


