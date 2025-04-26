from django import forms

class BMICalculatorForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    height = forms.FloatField(label='Height (cm)', min_value=100, max_value=300)
    weight = forms.FloatField(label='Weight (kg)', min_value=20, max_value=500)