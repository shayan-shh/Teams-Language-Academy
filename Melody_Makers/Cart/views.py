from django.shortcuts import render,get_object_or_404
from .cart import Cart
from Course.models import Course
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    cart =Cart(request)
    cart_course = cart.get_prods()
    total = cart.get_total()
    return render(request, 'cart_summary.html',{'cart_course': cart_course, 'total':total})

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        course_id = int(request.POST.get('course_id'))
        course = get_object_or_404(Course, id=course_id)

        if cart.add(course):
            messages.success(request, f'دوره "{course.name}" با موفقیت به سبد خرید اضافه شد.')
        else:
            messages.info(request, f'دوره "{course.name}" قبلاً در سبد خرید موجود است.')

        response = JsonResponse({'qty': len(cart)})
        return response

def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        course_id = int(request.POST.get('course_id'))

        cart.delete(course=course_id)

        response = JsonResponse({'course': course_id})
        messages.error(request, ' دوره از سبد خرید حذف شد')
        return response

