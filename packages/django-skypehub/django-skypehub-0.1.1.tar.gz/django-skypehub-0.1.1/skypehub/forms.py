from django import forms

class PostMessageForm(forms.Form):
    message = forms.CharField()
    chat = forms.CharField()
