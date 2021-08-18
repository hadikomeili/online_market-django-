from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import MessageForm
from .models import *
# Create your views here.


# class CreateMessageView(generic.FormView):
#
#     template_name = 'landing/contact_us.html'
#     form_class = MessageForm
#     # fields = ['subject', 'customer_name', 'phone_number', 'email', 'message_text']
#
#     success_url = reverse_lazy('landing:contact_us')
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

def contact_us(request):
    # if request.method == 'POST':

    if request.POST.get('action') == 'create-message':
        subject = request.POST.get('subject')
        customer_name = request.POST.get('customer_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message_text = request.POST.get('message_text')

        message = Message.objects.create(
            subject=subject, customer_name=customer_name, email=email,
            phone_number=phone_number, message_text=message_text
        )
        if isinstance(message, Message):
            # return render(request, 'landing/contact_us.html')
            return redirect('landing:contact_us')
        else:
            return HttpResponse('invalid inputs')

    # return render(request, 'create-post.html')
    else:

        return render(request, 'landing/contact_us.html')


