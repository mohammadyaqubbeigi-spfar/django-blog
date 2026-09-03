from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title" , "content"]

    def clean_title(self):
        title = self.cleaned_data["title"]

        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters.")

        return title

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        if title and content:
            if "python" in title.lower() and "django" not in content.lower():
                self.add_error(
                    "content",
                    "Posts about Python must mention Django in the content."
                )

        return cleaned_data