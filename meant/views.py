from django.shortcuts import render, redirect
from .models import Contact
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ContactSerializer
from rest_framework import status, viewsets
from .permissions import AdminOnly
from .filters import ContactMessageFilter


"""
Just to be cohesive we can do that like we are doing contact form
but this is 6 lines of code and we can do that in two

In production this is the thing we can discuss what the team prefers 
"""
# class LandingAPIView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'meant/index.html'  

#     def get(self, request):

#         serializer = ContactSerializer()
#         return Response(template_name = 'meant/index.html')

def index(request):

    return render(request, 'meant/index.html')


def login(request):

   return render(request, 'meant/login.html')


"""
I've used serializers as forms here 
We can do this in other ways.

First.
    Django forms 
Second.
    Custom forms in some frontend framework. 
    This is the most typicall solution, where you only posting data to
    an endpoint. This works here two I just have rendering form done by Django
    If you wanna test this out just go into postman or /swagger/

"""

def contact_form(request):

    serializer = ContactSerializer()
    context = {
        'serializer': serializer
    }

    return render(request, 'meant/contact.html', context)

"""
In other situation I would create file/app for api functions
"""

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOnly,)
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filterset_class  = ContactMessageFilter

    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)