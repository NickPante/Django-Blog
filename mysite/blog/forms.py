from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)  # ΟΝΟΜΑ
    email = forms.EmailField()  # EMAIL ΑΠΟΣΤΟΛΕΑ
    to = forms.EmailField()  # EMAIL ΠΑΡΑΛΗΠΤΕΙ
    comments = forms.CharField(required=False, widget=forms.Textarea)  # ΚΟΥΤΙ ΚΕΙΜΕΝΟΥ


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]  # ΤΑ ΠΑΙΔΙΑ ΠΟΥ ΘΑ ΕΜΦΑΝΙΖΟΝΤΑΙ
