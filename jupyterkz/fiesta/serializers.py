from rest_framework import serializers
from fiesta.models import Author
from fiesta.models import Html
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'path')

class HtmlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Html
        fields = ('id', 'name', 'path')
