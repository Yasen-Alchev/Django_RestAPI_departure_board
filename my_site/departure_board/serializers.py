from rest_framework import fields, serializers
from departure_board.models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        #fields = ['name']
        fields = '__all__'