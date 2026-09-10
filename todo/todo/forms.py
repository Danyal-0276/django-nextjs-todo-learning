from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title"]
        error_messages = {
            "title": {
                "required": "Todo title is required.",
                "max_length": "Todo titles must be 120 characters or fewer.",
            }
        }

    def clean_title(self):
        title = self.cleaned_data.get(
            "title",
            "",
        ).strip()

        if not title:
            raise forms.ValidationError(
                "Todo title is required."
            )

        return title
