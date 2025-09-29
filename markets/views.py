from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from django.views import View
from .models import Product, Like