from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product
from catalog.constants import BAD_WORDS


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    @staticmethod
    def _check_bad(value: str, field_label: str) -> str:
        text = (value or '').lower()
        for bad in BAD_WORDS:
            if bad in text:
                raise ValidationError(
                    f'Поле «{field_label}» содержит запрещённое слово: «{bad}».'
                )
        return value

    def clean_name(self):
        return self._check_bad(self.cleaned_data.get('name'),'Наименование')

    def clean_description(self):
        return self._check_bad(self.cleaned_data.get('description'), 'Описание')