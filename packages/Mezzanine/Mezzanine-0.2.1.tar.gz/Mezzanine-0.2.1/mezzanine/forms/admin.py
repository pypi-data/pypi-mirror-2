
from copy import deepcopy

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from mezzanine.core.admin import OrderableAdmin
from mezzanine.forms.models import Form, Field
from mezzanine.pages.admin import PageAdmin


form_fieldsets = deepcopy(PageAdmin.fieldsets)
form_fieldsets[0][1]["fields"] += ("response", "send_email")
FormMedia = deepcopy(OrderableAdmin.Media)
FormMedia.js = PageAdmin.Media.js + [js for js in FormMedia.js if js not in 
    PageAdmin.Media.js]

class FieldAdmin(admin.TabularInline):
    model = Field
   
class FormAdmin(PageAdmin, OrderableAdmin):

    class Media(FormMedia):
        pass

    inlines = (FieldAdmin,)
    fieldsets = form_fieldsets
    
admin.site.register(Form, FormAdmin)
