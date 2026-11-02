from django.shortcuts import render,redirect
from Cart.cart import Cart
from Course.models import Course,Profile
from django.contrib import messages
from Payment.forms import PaymentForm
from Payment.models import Order, OrderItem
from django.contrib.auth.models import User


def payment_success(request):
    return render(request, 'payment_success.html', {})


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_courses = cart.get_prods()
        total = cart.get_total()
        payment_form = PaymentForm(request.POST or None)

        if payment_form.is_valid():
            # Ensure user is authenticated to create an order
            if request.user.is_authenticated:
                user = request.user
                # Fetch all course IDs the user already owns to check against
                owned_courses = set(OrderItem.objects.filter(user=user).values_list('course_id', flat=True))
                
                # Check if there are any new courses in the cart
                new_courses = [course for course in cart_courses if course.id not in owned_courses]

                if not new_courses:
                    # If all courses are already owned, show a warning message and skip order creation
                    messages.warning(request, "شما قبلا این کالا هارا خریداری کرده اید.")
                    return redirect('home')
                
                # If there are new courses, proceed to create the Order and OrderItems
                full_name = payment_form.cleaned_data['card_name']
                email = payment_form.cleaned_data['email']
                amount_paid = total

                # Create the Order
                create_order = Order(user=user, full_name=full_name, email=email, amount_paid=amount_paid)
                create_order.save()
                order_id = create_order.pk

                # Create an OrderItem for each new course
                for course in new_courses:
                    course_id = course.id
                    price = course.sale_price if course.is_sale else course.price
                    create_order_item = OrderItem(order_id=order_id, course_id=course_id, user=user, price=price)
                    create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

                # Update user profile (optional step)
                Profile.objects.filter(user__id=user.id).update(oldCard="")

                messages.success(request, 'خرید با موفقیت انجام شد')
                return redirect('home')
            else:
                messages.warning(request, 'برای خرید ابتدا وارد حساب کاربری خود شوید')
                return redirect('login')
        else:
            messages.error(request, 'مشخصات را اشتباه وارد کرده اید')

        return redirect('home')
    else:
        messages.error(request, 'مشکلی پیش آمده است')
        return redirect('home')


def billing_info(request):
    cart =Cart(request)
    cart_course = cart.get_prods()
    total = cart.get_total()
    if request.user.is_authenticated:
        billing_form = PaymentForm
        return render(request, 'billing_info.html',{'cart_course': cart_course, 'total':total, 'billing_form':billing_form})
    else:
        billing_form = PaymentForm
        messages.success(request, 'برای پرداخت باید وارد حساب کاربری خود شوید')
        return redirect('home')

def checkout(request):
    cart =Cart(request)
    cart_course = cart.get_prods()
    total = cart.get_total()

    if request.user.is_authenticated:
        return render(request, 'checkout.html',{'cart_course': cart_course, 'total':total})
    else:
        return render(request, 'checkout.html',{'cart_course': cart_course, 'total':total})

def item_list(request):

    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.all()
        return render(request, 'item_list.html', {"orders":orders})

    else:
        messages.success(request, "شما اجازه دسترسی ندارید")
        return redirect('home')


def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # getting order
        order = Order.objects.get(id=pk)
        # get orderitem
        items = OrderItem.objects.filter(order=pk)
        return render(request, 'orders.html', {"order":order, "items":items})
    

def user_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = User.objects.all()
        return render(request, 'user_list.html', {"users":users})
    else:
        messages.success(request, "شما اجازه دسترسی ندارید")
        return redirect('home')


def users_courses(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # getting users
        user = User.objects.get(id=pk)
        # get courses
        courses = OrderItem.objects.filter(user=pk)
        print(courses)
        return render(request, 'users_courses.html', {"user":user, "courses":courses })
    
