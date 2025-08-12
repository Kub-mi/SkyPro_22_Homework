from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput, NumberInput, Textarea, Select, ClearableFileInput, CheckboxInput

from catalog.models import Product
from catalog.constants import BAD_WORDS


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        help_texts = {
            'name': 'Короткое, понятное название (без запрещённых слов).',
            'description': 'Ключевые характеристики товара (без запрещённых слов).',
            'image': 'PNG или JPEG (см. доп. задание).',
            'category': 'Выберите подходящую категорию.',
            'price': 'Неотрицательное число, например 1999.00.',
        }

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

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is None:
            return price
        if price < 0:
            # Сообщение попадёт под поле «Цена» в шаблоне
            raise ValidationError('Цена не может быть отрицательной.')
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widget_class_map = {
            TextInput: 'form-control',
            NumberInput: 'form-control',
            Textarea: 'form-control',
            Select: 'form-select',
            ClearableFileInput: 'form-control',
            CheckboxInput: 'form-check-input',  # на будущее (если добавишь BooleanField)
        }
        placeholders = {
            'name': 'например, «Апельсин»',
            'description': 'краткое описание товара…',
            'price': 'например, 1999.00',
        }

        for name, field in self.fields.items():
            widget = field.widget
            for widget_type, css in widget_class_map.items():
                if isinstance(widget, widget_type):
                    existing = widget.attrs.get('class', '')
                    widget.attrs['class'] = (existing + ' ' + css).strip()
                    break

            if name in placeholders:
                widget.attrs.setdefault('placeholder', placeholders[name])

            if name == 'name':
                widget.attrs.setdefault('autofocus', 'autofocus')

        for name, field in self.fields.items():
            if self.errors.get(name):
                existing = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = (existing + ' is-invalid').strip()
