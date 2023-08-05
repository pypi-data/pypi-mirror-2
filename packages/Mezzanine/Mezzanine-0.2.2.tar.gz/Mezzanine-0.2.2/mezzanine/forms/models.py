
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import Orderable
from mezzanine.pages.models import Page


FIELD_MAPPING = (
    (1, "Check-box", "BooleanField"),
    (2, "Text", "CharField"),
    (3, "Email", "EmailField"),
    (4, "Date", "DateField"),
    (5, "Date/time", "DateTimeField"),
    (6, "Drop-down", "ChoiceField"),
    (7, "Multi-select", "MultipleChoiceField"),
)

FIELD_CHOICES = [f[:2] for f in FIELD_MAPPING]

class Form(Page):
    """
    A user-built form
    """

    response = models.TextField(_("Response"), max_length=2000)
    send_email = models.BooleanField(_("Send email"), default=True)

    class Meta:
        verbose_name = _("Form")
        verbose_name_plural = _("Forms")
        
    @models.permalink
    def get_absolute_url(self):
        return ("form_detail", (), {"slug": self.slug})

class Field(Orderable):
    
    form = models.ForeignKey("Form")
    label = models.CharField(_("Label"), max_length=20)
    type = models.IntegerField(_("Type"), choices=FIELD_CHOICES)
    mandatory = models.BooleanField(_("Mandatory"))
    choices = models.CharField(_("Choices"), max_length=1000, blank=True)

    class Meta:
        verbose_name = _("Field")
        verbose_name_plural = _("Fields")
        order_with_respect_to = "form"
    
    def __unicode__(self):
        return self.label
    
#class FormSubmission(models.Model):
#    """
#    a website submission to a user-built form
#    """
#    
#    class Meta:
#        verbose_name = "Form entry"
#        verbose_name_plural = "Form entries"
#    
#    built_form = models.ForeignKey(BuiltForm)
#    submission_date = models.DateTimeField()

#    # mandatory form fields for every form
#    first_name = models.CharField(max_length=50)
#    last_name = models.CharField(max_length=50)
#    email = models.EmailField(max_length=50)
#    
#    # extra fields for a form that can be user-specified as mandatory or option
#    # identified by blank=True
#    dob = models.DateField(blank=True, null=True)
#    phone = models.CharField(blank=True, max_length=20)
#    message = models.TextField(blank=True, max_length=2000)
#    image = models.ImageField(blank=True, upload_to=UPLOAD_TO, max_length=50)
#    
#    def __unicode__(self):
#        return "%s Submission: %s %s" % (self.built_form, self.first_name, 
#            self.last_name)

#class FieldSubmission(models.Model):

#    
