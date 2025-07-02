from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class signupForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)
    # email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter your Email'}))
    # first_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    # last_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email",'password1','password2']
    

    def __init__(self, *args, **kwargs):
        super(signupForm,self).__init__(*args, **kwargs)


        # self.fields['username'].widget.attrs['class']='form-control'
        # self.fields['username'].widget.attrs['placeholder']='Enter Username'
        # self.fields['username'].label=''



        # self.fields['password1'].widget.attrs['class']='form-control'
        # self.fields['password1'].widget.attrs['placeholder']='Enter Your Password'
        # self.fields['password1'].label=''


        # self.fields['password2'].widget.attrs['class']='form-control'
        # self.fields['password2'].widget.attrs['placeholder']='Cnfirm Your Password'
        # self.fields['password2'].label=''