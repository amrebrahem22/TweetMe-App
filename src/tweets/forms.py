from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
	content = forms.CharField(label="", widget=forms.Textarea(attrs={
		'class': 'form-control tweet-form',
		'rows': 4,
		'placeholder': "What's Happening?"
	}))

	class Meta:
		model = Tweet
		fields = ['content']

	def clean_content(self):
		content = self.cleaned_data['content']

		if len(content) >= 140:
			raise forms.ValidationError("Status Should be less than 140.")

		return content

