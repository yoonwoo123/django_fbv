from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

# class UserForm(forms.ModelForm): # ModelForm 과 그냥 form의 차이
#     class Meta:
#         model = get_user_model()
#         # fields = '__all__'
#         fields = ['username', 'password']

class UserCustomChangeForm(UserChangeForm): # UserChangeForm 을 받아서 만든 커스텀폼
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)