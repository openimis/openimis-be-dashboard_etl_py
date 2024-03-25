from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from django.shortcuts import render
from dashboard_etl.extract.base_data_extract import BaseExtractor
from dashboard_etl.extract.indicators_extract import run_etl

indicators = apps.get_app_config("dashboard_etl").indicators


async def extract_base_data(request):
    extractor = BaseExtractor()
    extractor.extract_base_data()
    return HttpResponse("Base data extracted!")


def extract_indicators(request):
    if request.method == "POST":
        result = run_etl.apply_async()
        progress = {indicator_name: cache.get(f"{indicator_name}_progress", "Not Started")
                    for indicator_name in indicators}

        print(result)
        # return JsonResponse({"task_id": result.id}, status=202)
        return render(request, "etl.html", {"progress": progress, "id": result})

    else:
        progress = {indicator_name: cache.get(f"{indicator_name}_progress", "Not Started")
                    for indicator_name in indicators}

        return render(request, "etl.html", {"progress": progress})


def get_task_progress(request):
    progress = {indicator_name: cache.get(f"{indicator_name}_progress", "Not Started")
                for indicator_name in indicators}

    return JsonResponse({"progress": progress})




# celery -A openIMIS.celery worker -E --loglevel=info
