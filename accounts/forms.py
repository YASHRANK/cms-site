from django import forms
from accounts.models import Order, Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for each_field in self.fields:
            self.fields[each_field].widget.attrs.update({'class': 'form-control'})
       

    class Meta(object):
        model = Order
        fields = '__all__'
        

class CustomerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for each_field in self.fields:
            if each_field == "profile_pic":
                continue

            self.fields[each_field].widget.attrs.update({'class': 'form-control'})

    class Meta(object):
        model = Customer
        fields = '__all__'
        exclude = ['user']

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'})
        self.fields['email'].widget.attrs.update({'class':'form-control', 'placeholder':'Email'})
        self.fields['password1'].widget.attrs.update({'class':'form-control','placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'class':'form-control','placeholder':'Confirm Password'})
            
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
