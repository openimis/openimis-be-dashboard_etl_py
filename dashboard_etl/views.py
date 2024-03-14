from django.http import HttpResponse
from django.shortcuts import render
from dashboard_etl.extract.base_data_extract import BaseExtractor


def extract_base_data(request):
    extractor = BaseExtractor()
    extractor.extract_base_data()
    return HttpResponse("Hello!")
