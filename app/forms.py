from django import forms

class UserForm(forms.Form):
    website = forms.CharField(label='Your Website', max_length=100)
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email', max_length=100)
    password = forms.CharField(label='Your Password', max_length=100, widget=forms.PasswordInput)

class widgetCustomizationForm(forms.Form):
    widget_color = forms.CharField(max_length=100)
    widget_background = forms.CharField(max_length=100)
    widget_outer_ring_color = forms.CharField(max_length=100)