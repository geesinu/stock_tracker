from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'name', 'sector']

class StockSelectionForm(forms.Form):
    stock = forms.ModelChoiceField(queryset=Stock.objects.all(), empty_label="Select a stock to edit")
