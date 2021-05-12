from django import forms

class TodoForm(forms.Form):
    file_title = forms.CharField(max_length=255)
    file = forms.FileField()
    