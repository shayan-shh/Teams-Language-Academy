from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from Course.models import Profile,Course,Category

# add profile picture
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'id': 'id_profile_picture', 'class': 'form-control'})
    ),

    class Meta:
        model = Profile
        fields = ['profile_image']
# update user info form
class UpdateUserInfo(forms.ModelForm):
    phone = forms.CharField(
        label="شماره تماس ",
        max_length=11,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'شماره تماس خود را وارد کنید'
            }
        )
    )
    address1 = forms.CharField(
        label="آدرس منزل",
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'آدرس منزل را وارد کنید',
            }
        )
    )
    address2 = forms.CharField(
        label="آدرس محل کار ",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'آدرس محل کار را وارد کنید'
            }
        ),
        required=False
    )
    city = forms.CharField(
        label="شهر ",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'شهر'
            }
        ),
        required=False
    )
    state = forms.CharField(
        label=" استان",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'استان'
            }
        ),
        required=False
    )
    zipcode = forms.CharField(
        label="کد پستی ",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'کد پستی'
            }
        ),
        required=False
    )
    country = forms.CharField(
        label=" کشور",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'کشور'
            }
        ),
        required=False
    )

    class Meta:
        model = Profile
        fields = {'phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country'}

# update password form
class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="رمزعبور ",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type': 'password',
                'placeholder': 'رمز عبور بالای 8 کاراکتر را وارد کنید'
            }
        )
    )
    new_password2 = forms.CharField(
        label="تایید رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type': 'password',
                'placeholder': 'دوباره رمز را وارد کنید'
            }
        )
    )

    class Meta:
        model = User
        fields = {'new_password1', 'new_password2'}

# update profile form
class UpdateUserForm(UserChangeForm):

    password = None
    first_name = forms.CharField(
        label="نام ",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'نام خود را وارد کنید'
            }
        )
    )
    last_name = forms.CharField(
        label="نام خانوادگی",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'نام  خانوادگی خود را وارد کنید'
            }
        )
    )
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'ایمیل خود را وارد کنید'
            }
        )
    )
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'نام کاربری خود را وارد کنید'
            }
        )
    )

    class Meta:
        model = User
        fields =['first_name','last_name', 'email', 'username' ]
# sign up form
from django.core.exceptions import ValidationError

class SignUpForms(UserCreationForm):
    first_name = forms.CharField(
        label="نام ",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    last_name = forms.CharField(
        label="نام خانوادگی",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password1 = forms.CharField(
        label="رمزعبور ",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password2 = forms.CharField(
        label="تایید رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")
        return username


# add course to page by admin
class AddCoursetForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'price', 'category', 'picture', 'is_sale', 'sale_price', 'length', 'days', 'teacher_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'is_sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'length': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'teacher_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }


    def clean(self):
        cleaned_data = super().clean()
        is_sale = cleaned_data.get('is_sale')
        sale_price = cleaned_data.get('sale_price')
        
        # If 'is_sale' is True but 'sale_price' is empty, raise validation error
        if is_sale and not sale_price:
            self.add_error('sale_price', 'باید قیمت بعد از تخفیف وارد شود ')
        
        # If 'is_sale' is False, set 'sale_price' to None
        if not is_sale:
            cleaned_data['sale_price'] = None
        
        return cleaned_data
#  add category by admin
class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }