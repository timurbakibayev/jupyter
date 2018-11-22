#!usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework import status, permissions, views

from plot.models import Patient
from plot.models import Reading
from plot.models import Attachment

import dateutil
import csv
import time
import sys
import pytz

tz = pytz.timezone('Asia/Almaty')

class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            user = request.user
            # if user is None:
            #    return Response({"detail": "Необходима авторизация"})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        f = request.data['file']
        instance = Attachment(
            parent_id=str(patient.id),
            file_name=filename,
            attachment=f,
            # user_id = user.id,
        )
        instance.save()
        print("Loading", instance.attachment.url)
        readings = Reading.objects.filter(patient=patient)
        with open(instance.attachment.url) as csvfile:
            print("File is open now")
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            print("spamreader is ready")
            i = 0
            cumulative = 0
            for row in spamreader:
                #print("line",i)
                i += 1
                if i > 1:
                    try:
                        device, counter, timestamp, timezone, value, quality = row
                        value = float(value)
                        quality = float(quality)
                        if quality > -1 or "_activity_" in filename or 2+2 == 4:
                            timestamp = int(timestamp)+6*60*60
                            timestamp_iso = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(timestamp))
                            time_dt = tz.localize(dateutil.parser.parse(timestamp_iso))
                            if timestamp_iso[-2:] == "00":
                                try:
                                    reading = readings.get(time_iso=timestamp_iso)
                                except:
                                    reading = Reading()
                                reading.patient_id = patient.id
                                reading.time_iso = timestamp_iso
                                reading.time_epoch = timestamp
                                reading.time = time_dt
                                if "_hr_" in filename:
                                    reading.value_hr = int(value)
                                if "_spo2_" in filename:
                                    reading.value_spo2 = int(value)
                                if "_rr_" in filename:
                                    reading.value_rr = int(value)
                                if "_hrv_" in filename:
                                    reading.value_hrv = int(value)
                                if "_bperf_" in filename:
                                    reading.value_bperf = value
                                if "_activity_" in filename:
                                    reading.value_activity = value + cumulative
                                if "_steps_" in filename:
                                    reading.value_steps = int(value + cumulative)
                                cumulative = 0
                                try:
                                    reading.save()
                                except Exception as e:
                                    print("failed to save")
                                    print(e)
                            else:
                                cumulative += value
                    except Exception as e:
                        print("general fail to")
                        print(e)

        return Response(status=204)


class FileUploadViewOriginal(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            # user = request.user
            # if user is None:
            #    return Response({"detail": "Необходима авторизация"})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        f = request.data['file']
        instance = Attachment(
            parent_id=str(patient.id),
            file_name=filename,
            attachment=f,
            # user_id = user.id,
        )
        instance.save()
        # action = Action()
        # action.order_id = order.id
        # action.action = "Файл " + filename
        # action.user_id = user.id
        # action.save()
        # order.save()

        return Response(status=204)