from django import forms
from .models import Review, Movie
from django.core.validators import MinValueValidator, MaxValueValidator

class ReviewForm(forms.ModelForm):


    class Meta:
        model = Review
        fields = ('score', 'content')
        widgets = {
            'score': forms.NumberInput(attrs={'min': 0, 'max':10, 'placeholder': '0~10점 사이로 입력해주세요.'})
        }
        labels={
            'score' : "평점",
            'content' : "내용",
        }

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'