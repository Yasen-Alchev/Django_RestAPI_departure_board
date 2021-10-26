from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from departure_board.serializers import BoardSerializer
from departure_board.models import Board
import requests

def departure(response):
    return HttpResponse("Hello Departure Board")

def index(request):
    link = "https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=10&sort=departure_time&include=vehicle%2Cschedule%2Ctrip&filter%5Bdirection_id%5D=0&filter%5Bstop%5D=place-north"
    content = requests.get(link).json()

    data = content['data']
    included = content['included']

    formated_data = []

    for entry in data:
        entry_data = {}

        for i in included:
            if i['id'] == entry['relationships']['schedule']['data']['id']:
                entry_data['time'] = i['attributes']['departure_time']
                break

        if entry['relationships']['vehicle']['data'] is not None:
            train_id = entry['relationships']['vehicle']['data']['id']
        else:
            train_id = None

        for i in included:
            if i['id'] == entry['relationships']['trip']['data']['id']:
                entry_data['destination'] = i['attributes']['headsign']
                break

        entry_data['train'] = None
        for i in included:
            if i['id'] == train_id:
                entry_data['train'] = i['attributes']['label']
                break

        entry_data['track'] = "TBD"
        entry_data['status'] = entry['attributes']['status']

        formated_data.append(entry_data)

    return render(request, 'homework.html', {"data" : formated_data})




def home(request):
    boards = Board.objects.all()
    return render(request, 'index.html', {"boards" : boards})

def boards_json(request):
    boards = Board.objects.all()
    serializer = BoardSerializer(boards, many = True)
    return JsonResponse({'data': serializer.data }, safe=False)
