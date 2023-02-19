from .models import Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        # Т.к в модели group стоит blank=True,следовательно оно
        # по умолчанию необязательное для заполнения в фоме
        fields = ('text', 'group')
