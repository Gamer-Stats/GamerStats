from core.models import Subscribe
from django import forms


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ("email",)
