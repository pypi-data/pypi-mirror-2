
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from mezzanine.utils import content_media_urls
from mezzanine.core.models import Orderable


class OrderWidget(forms.HiddenInput):
    """
    Add up and down arrows for ordering controls next to a hidden form field.
    """
    def render(self, *args, **kwargs):
        rendered = super(OrderWidget, self).render(*args, **kwargs)
        arrows = ["<img src='%simg/admin/arrow-%s.gif' />" %
            (settings.ADMIN_MEDIA_PREFIX, arrow) for arrow in ("up", "down")]
        arrows = "<span class='ordering'>%s</span>" % "".join(arrows)
        return rendered + mark_safe(arrows)


class DynamicInlineAdminForm(forms.ModelForm):
    """
    Form for ``DynamicInlineAdmin`` that can be collapsed and sorted with 
    drag and drop using ``OrderWidget``.
    """
    
    class Media:
        js = content_media_urls("js/jquery-1.4.2.min.js",
            "js/jquery-ui-1.8.1.custom.min.js", "js/dynamic_inline.js",)

    def __init__(self, *args, **kwargs):
        super(DynamicInlineAdminForm, self).__init__(*args, **kwargs)
        if issubclass(self._meta.model, Orderable):
            self.fields["_order"] = forms.CharField(label=_("Order"), 
                widget=OrderWidget, required=False)


def get_edit_form(obj, attr, data=None):
    """
    Returns the in-line editing form for editing a single model field.
    """

    class EditForm(forms.ModelForm):
        """
        In-line editing form for editing a single model field.
        """

        app = forms.CharField(widget=forms.HiddenInput)
        model = forms.CharField(widget=forms.HiddenInput)
        id = forms.CharField(widget=forms.HiddenInput)
        attr = forms.CharField(widget=forms.HiddenInput)

        class Meta:
            model = obj.__class__
            fields = (attr,)

    initial = {"app": obj._meta.app_label, "id": obj.id, "attr": attr,
        "model": obj._meta.object_name.lower()}
    return EditForm(instance=obj, initial=initial, data=data)
