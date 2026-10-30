from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "phone", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Optional", "autocomplete": "tel"}),
            "message": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Your date, your city, and what you are imagining…"}
            ),
        }
