from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course
from .models import Category
from .models import Profile
from Payment.models import Order, OrderItem
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from Course.forms import SignUpForms, UpdateUserForm, UpdatePasswordForm, UpdateUserInfo,AddCoursetForm,AddCategoryForm, ProfilePicForm
from django.db.models import Q
from Cart.cart import Cart
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group


# Create your views here.
def home(request):
    all_course = Course.objects.all()
    return render(request, 'home.html', {'courses': all_course})
# list of courses in general
def courses(request):
    all_course = Course.objects.all()
    return render(request, 'courses.html', {'courses': all_course})
# about page
def about(request):
    return render(request, "about.html")
# user courses
def my_course(request):
    
    purchased_courses  = Course.objects.filter(orderitem__order__user = request.user).distinct()
    
    return render(request, 'my_course.html', {"purchased_courses":purchased_courses})
# each course page
def course(request,ck):
    course = Course.objects.get(id=ck)
    similar_courses = Course.objects.filter(category=course.category).exclude(id=ck)
    return render(request, 'course.html', {'course':course, 'similar_courses': similar_courses})
# each category page
def category(request,cat):
    cat = cat.replace("-", " ")
    try: 
        category = Category.objects.get(name=cat)
        courses = Course.objects.filter(category=category)
        return render(request, 'category.html', { "courses": courses, "category": category})
    except:
        messages.error(request,("دسته بندی وجود ندارد!"))
        return redirect("home")
# list of categories
def category_summary(request):
    all_cat = Category.objects.all()
    return render(request, 'category_summary.html',{'category': all_cat})
# search based on name and description
def search(request):
    if request.method == 'POST':
        search_box = request.POST['search_box']
        search_box = Course.objects.filter(
            Q(name__icontains=search_box) | 
            Q(description__icontains=search_box)
            )

        if not search_box:
            messages.error(request, 'چنین دوره ای وجود ندارد!')
            return render(request, 'search.html')
        else:
              return render(request, 'search.html', {'search_box':search_box})

      
    return render(request, 'search.html')
# Login
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید")
            return redirect("home")
        else:
            messages.error(request, "کاربری با این مشخصات وجود ندارد!!")
            return redirect("login")
    return render(request, 'login.html')
# Logout
def logout_user(request):
    logout(request)
    messages.error(request, "با موفقیت خارج شدید")
    return redirect("home")
# signup
def signup_user(request):
    form = SignUpForms()
    if request.method == "POST":
        form = SignUpForms(request.POST)
        if form.is_valid:
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(request, username=username, password= password1)
            login(request, user)
            messages.success(request, 'اکانت شما ساخته شد')
            return redirect("home")
        else:
            messages.error(request, 'مشکلی در ثبت نام شما وجود دارد')
            return redirect("signup")
    else: 
        return render(request, 'signup.html', {'form': form})




# update profile
def update_user(request):
    if request.user.is_authenticated:
        profile = Profile()
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        user_form = UpdateUserForm(request.POST or None, request.FILES or None, instance = current_user)

        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance = profile_user)

        if user_form.is_valid() and  profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, 'پروفایل شما با موفقیت ویرایش شد')
            return redirect('update_user')
        return render(request, 'update_user.html',{'user_form': user_form , 'profile_form': profile_form, 'profile': profile})
    else:
        messages.error('ابتدا باید وارد حساب خود شوید!')   
        return redirect('home')
# update information
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UpdateUserInfo(request.POST or None, instance = current_user)

        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات کاربری شما با موفقیت ویرایش شد')
            return redirect('home')
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.success('ابتدا باید وارد حساب خود شوید!')   
        return redirect('home')


    return render(request, 'update_info.html')
# update password
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = UpdatePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'رمز با موفقیت ویرایش شد')
                login(request,current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = UpdatePasswordForm(current_user)
            return render(request,  'update_password.html', {'form':form})
        
    else: 
        messages.success(request, 'برای تغییر رمز باید وارد حساب خود شوید')
        return redirect('home')
    
# admin access
def is_admin(user):
    return user.is_authenticated and user.is_superuser

# add course by admin
@user_passes_test(is_admin)
def add_course(request):
    if request.method == "POST":
        form = AddCoursetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'دوره با موفقیت افزوده شد')
            return redirect('courses')
    else:
        form = AddCoursetForm()
    return render(request, 'add_course.html', {'form': form})

# update course by admin
@user_passes_test(is_admin)
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)  # Fetch the product by primary key
    
    # If the form is submitted (POST request)
    if request.method == 'POST':
        form = AddCoursetForm(request.POST, request.FILES, instance=course)  # Bind form with existing product data
        if form.is_valid():
            form.save()  # Save the updated product data
            messages.success(request, 'دوره با موفقیت ویرایش شد')
            return redirect('courses')  # Redirect to the product list after saving
    else:
        form = AddCoursetForm(instance=course)  # Load the form with existing product data
    
    return render(request, 'edit_course.html', {'form': form, 'course': course})


# delete course by admin
@user_passes_test(is_admin)
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()  # Delete the product
    messages.success(request, 'دوره حذف شد')
    return redirect('courses')  # Redirect to the product list after deletion









# add category by admin
@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ' دستبه بندی با موققیت افزوده شد')
            return redirect('category_summary')  
    else:
        form = AddCategoryForm()
    return render(request, 'add_category.html', {'form': form})

# update category page by admin
@user_passes_test(is_admin)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, ' دستبه بندی با موققیت ویرایش شد')
            return redirect('category_summary') 
    else:
        form = AddCategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category': category})

# delete category by admin
@user_passes_test(is_admin)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    # Handle the confirmation page on GET request
    if request.method == 'GET':
        return render(request, 'confirm_delete_category.html', {'category': category})
    
    # Handle the actual deletion on POST request
    if request.method == 'POST':
        category.delete()
        messages.success(request, ' دستبه بندی با موققیت حذف شد')
        return redirect('category_summary')  # or 'category_summary'

    # For safety, if we get any other method, just redirect (though unlikely)
    return redirect('category_summary')

