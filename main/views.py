from django.http import JsonResponse
from .models import District

def get_filtered_districts(request):
    region_id = request.GET.get('region_id')
    if region_id:
        districts = District.objects.filter(region_id=region_id)
        data = [{'id': district.id, 'name': district.name} for district in districts]
        return JsonResponse({'districts': data})
    else:
        return JsonResponse({'districts': []})
