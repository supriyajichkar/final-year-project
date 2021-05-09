from django.contrib import admin
from . import models
from django.shortcuts import redirect
from django import forms
from django.urls import path
import os
from django.contrib import messages
import io
# from .views import CsvUploader
from .models import TestQuestionAnswer
from django.db.utils import IntegrityError
from django.core.exceptions import FieldDoesNotExist
from django.db import transaction
# Register your models here.
admin.site.register(models.Test)
admin.site.register(TestQuestionAnswer)
# admin.site.register(models.TestQuestionAnswer)


# class CsvUploadForm(forms.Form):
#     csv_file = forms.FileField()


# class CsvUploadAdmin(admin.ModelAdmin):

#     change_list_template = "csv_form.html"

#     def get_urls(self):
#         urls = super().get_urls()
#         additional_urls = [
#             path("upload-csv/", self.upload_csv),
#         ]
#         return additional_urls + urls

#     def changelist_view(self, request, extra_context=None):
#         extra = extra_context or {}
#         extra["csv_upload_form"] = CsvUploadForm()
#         return super(CsvUploadAdmin, self).changelist_view(request, extra_context=extra)

#     def upload_csv(self, request):
#         if request.method == "POST":
#             pass
#             # Here we will process the csv file



#         return redirect("..")


# @admin.register(TestQuestionAnswer)
# class TestQuestionAnswerAdmin(CsvUploadAdmin):
#     pass


# l1 = set(l1)
# l2 = set(l2)

# print(l1.intersection(l2))
# l1.difference(l2)

# def upload_csv(self, request):
#     if request.method == "POST":
#         form = CsvUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             if request.FILES['csv_file'].name.endswith('csv'):

#                 try:
#                     decoded_file = request.FILES['csv_file'].read().decode(
#                         'utf-8')
#                 except UnicodeDecodeError as e:
#                     self.message_user(
#                         request,
#                         "There was an error decoding the file:{}".format(e),
#                         level=messages.ERROR
#                     )
#                     return redirect("..")

# 				# Here we will call our class method
#                 io_string = io.StringIO(decoded_file)
#                 uploader = CsvUploader(io_string, self.model)
#                 result = uploader.create_records()

#             else:
#                self.message_user(
#                request,
#                "Incorrect file type: {}".format(
#                    request.FILES['csv_file'].name.split(".")[1]
#                    ),
#                level=messages.ERROR
#                )

#     else:
#         self.message_user(
#             request,
#             "There was an error in the form {}".format(form.errors),
#             level=messages.ERROR
#         )

#     return redirect("..")


# def read_chunk(self):
#     chunk = []
#     for i in range(1000):
#         try:
#             chunk.append(self.model(**self.reader[self.csv_pos]))
#         except IndexError as e:
#             print(e)
#             break
#         self.csv_pos += 1
#     return chunk


# def create_records(self):

#     if not self.valid:
#         return "Invalid csv file"

#     while True:
#         chunk = self.read_chunk()

#         if not chunk:
#             break

#         try:
#             with transaction.atomic():
#                 self.model.objects.bulk_create(chunk)
#         except IntegrityError as e:
#             for i in chunk:
#                 try:
#                     i.save()
#                 except IntegrityError:
#                     continue
#             print("Exeption: {}".format(e))

#     return "records succesfully saved!"