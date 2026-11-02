from Course.models import Course,Profile
from django.contrib import messages
from django.contrib.auth.models import User

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request

        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] ={}

        self.cart = cart



    def add(self,course):
        course_id = str(course.id)
        if course_id in self.cart:
            return False  # Item already exists
        else:
            self.cart[course_id] = {'price': str(course.price)}
            self.session.modified = True
            return True  # Item successfully added


# tool sabade kharid ra barmigardand
    def __len__(self):
        return len(self.cart)
    
# gereftan dore ha braye namayesh dar sabad kharid
    def get_prods(self):
        course_ids = self.cart.keys()
        course = Course.objects.filter(id__in= course_ids)

        return course
    
    def delete(self,course):
        course_id = str(course)
        
        if course_id in self.cart:
            del self.cart[course_id]

        self.session.modified = True

    def get_total(self):
        course_ids = self.cart.keys()
        courses = Course.objects.filter(id__in=course_ids)
        total = 0
        for key,value in self.cart.items():
            key = int(key)
            for course in courses:
                if course.id == key:
                    if course.is_sale:
                        total = total + (course.sale_price)
                    else:
                        total = total + (course.price)

        return total