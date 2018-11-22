#!usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework import status, permissions, views

from fiesta.models import Attachment
from fiesta.models import Author
from fiesta.models import Html


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, pk):
        try:
            author = Author()
            author.save()
            user = request.user
            # if user is None:
            #    return Response({"detail": "Необходима авторизация"})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)



        f = request.data['file']
        instance = Attachment(
            parent_id=str(author.id),
            file_name=filename,
            attachment=f,
            # user_id = user.id,
        )
        instance.save()

        html = Html()
        html.author = author
        html.attachment = instance
        html.name=filename
        html.size = 0 # <----
        html.save()

        #with open(instance.attachment.url) as csvfile:

        return Response(status=204)


class FileUploadViewOriginal(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, pk):
        try:
            author = Author.objects.get(pk=pk)
            # user = request.user
            # if user is None:
            #    return Response({"detail": "Необходима авторизация"})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        f = request.data['file']
        instance = Attachment(
            parent_id=str(author.id),
            file_name=filename,
            attachment=f,
            # user_id = user.id,
        )
        instance.save()

        return Response(status=204)