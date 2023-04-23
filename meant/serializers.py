from datetime import date
from rest_framework import serializers
from .models import Contact
from rest_framework.validators import UniqueValidator
from django.conf import settings
import os
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email


"""
This just adds a class to django serializers rendered as forms 
Basically I wanted to use some framework to serve html files so
I thought if im using Django I can use serializer rendering but I didn't
liked how they looked so I added custom template instead of bootstrap ¯\_(ツ)_/¯

"""
TEMPLATE_PATH = os.path.join(
                settings.TEMPLATES[0]["DIRS"][0], "base", "custom_input_forms.html"
            )

class ContactSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    name = serializers.CharField(
        style={
            "template": TEMPLATE_PATH,
            "class": "custom_form_control",
            "input_type": "input"
        }
    )

    email = serializers.CharField(
        style={
            "template": TEMPLATE_PATH,
            "class": "custom_form_control",
            "input_type": "input"
        }
    )

    subject = serializers.CharField(
        style={
            "template": TEMPLATE_PATH,
            "class": "custom_form_control",
            "input_type": "select",
            "choice": Contact.SUBJECT
        }
    )

    message = serializers.CharField(
        style={
            "template": TEMPLATE_PATH,
            "input_type": "textarea",
        }
    )
    
    def get_status(self, obj):
        return obj.status

    def validate(self, data):
        name = data["name"]
        email = data["email"]
        if (5 > len(name)):
            raise serializers.ValidationError({"Invalid name": "Name is to short."})

        try:
            validate_email(email)
        except:
            raise serializers.ValidationError({"Invalid Email": "Email is invalid, please recheck."})

        return data

    class Meta:
        model = Contact
        fields = "__all__"
