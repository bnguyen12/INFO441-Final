from django import forms

class RegistrationForm(forms.Form):
    first_name = forms.CharField(label="FirstName", max_length=30, required=True)
    last_name = forms.CharField(label="LastName", max_length=30, required=True)
    email = forms.EmailField(label="Email", max_length=30, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, max_length=30, required=True)
    passwordconf = forms.CharField(label="PasswordConf", widget=forms.PasswordInput, max_length=30, required=True)

    MY_CHOICES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
        ('Seller', 'Seller'),
    )

    permission_type = forms.ChoiceField(widget=forms.RadioSelect, choices=MY_CHOICES, required=True)

class SigninForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=30, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, max_length=30, required=True)

class PostForm(forms.Form):
    description = forms.CharField(label="Description", max_length=1000)
    tree_name = forms.CharField(label="Tree", widget=forms.TextInput, max_length=300, required=True)


class ProfileEdit(forms.Form):
    first_name = forms.CharField(label="FirstName", max_length=30, required=True)
    last_name = forms.CharField(label="LastName", max_length=30, required=True)

    MY_CHOICES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
        ('Seller', 'Seller'),
    )

    permission_type = forms.ChoiceField(widget=forms.RadioSelect, choices=MY_CHOICES, required=True)
