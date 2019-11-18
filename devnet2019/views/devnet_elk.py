#!/usr/bin/env python3

from django.shortcuts import render


def devnet_elk(request):
    return render(request, 'elk.html')
