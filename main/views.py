from django.http import JsonResponse
from .models import District, Region, Sector, State, Municipality



def get_filtered_districts(request, region_id):
    districts = District.objects.filter(region_id=region_id).order_by('name')
    districts_list = []
    for district in districts:
        districts_list.append({'id': district.id, 'name': district.name})
    return JsonResponse(districts_list, safe=False)


def get_filtered_sectors(request, district_id):
    sectors = Sector.objects.filter(district_id=district_id).order_by('name')
    sectors_list = []
    for sector in sectors:
        sectors_list.append({'id': sector.id, 'name': sector.name})
    return JsonResponse(sectors_list, safe=False)


def get_filtered_municipalities(request, state_id):
    municipalities = Municipality.objects.filter(state_id=state_id).order_by('name')
    municipalities_list = []
    for municipality in municipalities:
        municipalities_list.append({'id': municipality.id, 'name': municipality.name})
    return JsonResponse(municipalities_list, safe=False)