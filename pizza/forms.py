from django import forms


class OrderForm(forms.Form):
    email = forms.EmailField(label='Ваш e-mail, обязателен к заполнению')
    phone = forms.RegexField(regex=r'^\+?\d{9,15}$',
                             label='Ваш номер телефона',
                             error_messages={'wrong_phone': "Введите номер в формате '+1234567890', до 15 цифр"})
    name = forms.CharField(max_length=50, label='Ваше имя')
