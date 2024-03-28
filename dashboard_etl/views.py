from django.core.cache import cache
from django.http import JsonResponse
from django.apps import apps
from django.shortcuts import render
from dashboard_etl.extract.extractor import run_indicators_etl, run_base_data_etl

from .extract.extract_premium_collected import run_etl as test_etl

base_data = apps.get_app_config("dashboard_etl").base_data
indicators = apps.get_app_config("dashboard_etl").indicators


def etl(request):
    if request.method == "POST":
        if "basedata" in request.POST:
            return extract_base_data(request)
        elif "indicators" in request.POST:
            return extract_indicators(request)
    else:
        progress_ind = {data: cache.get(f"{data}_progress", "Not Started")
                        for data in base_data}
        progress_base = {indicator_name: cache.get(f"{indicator_name}_progress", "Not Started")
                         for indicator_name in indicators}

        progress = {**progress_base, **progress_ind}

        return render(request, "etl.html", {"progress": progress})


def extract_base_data(request):
    if request.method == "POST":
        result = run_base_data_etl.apply_async()
        progress = {data: cache.get(f"{data}_progress", "Not Started")
                    for data in base_data}

        return render(request, "etl.html", {"progress": progress, "id": result})
    else:
        progress = {data: cache.get(f"{data}_progress", "Not Started")
                    for data in base_data}

        return render(request, "etl.html", {"progress": progress})


def extract_indicators(request):
    if request.method == "POST":
        result = test_etl()
        # result = run_indicators_etl.apply_async()
        progress = {indicator_name: cache.get(f"{indicator_name}_progress", "Not Started")
                    for indicator_name in indicators}

        return render(request, "etl.html", {"progress": progress, "id": result})

    else:
        progress = {indicator_name: cache.get(f"{indicator_name}_progress", "Not Started")
                    for indicator_name in indicators}

        return render(request, "etl.html", {"progress": progress})


def get_task_progress(request):
    progress = {indicator_name: cache.get(f"{indicator_name}_progress", "Not Started")
                for indicator_name in base_data + indicators}

    return JsonResponse({"progress": progress})
