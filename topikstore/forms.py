from django import forms
from .models import *

class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['author_name', 'email', 'question']
        widgets = {
            'author_name': forms.TextInput(),
            'email': forms.TextInput(),
            'question': forms.Textarea()
        }

class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Feedback
        fields = ['author_name', 'feedback']
        widgets = {
            'author_name': forms.TextInput(),
            'feedback': forms.Textarea()
        }