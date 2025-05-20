# serializers.py
# Os serializers vão transformar os dados recebidos da API em objetos de modelo do Django para serem salvos no banco.
from rest_framework import serializers
from .models import AtaRegistroPreco, ItemDaAta

class ItemDaAtaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDaAta
        fields = '__all__'

class AtaRegistroPrecoSerializer(serializers.ModelSerializer):
    itens = ItemDaAtaSerializer(many=True)

    class Meta:
        model = AtaRegistroPreco
        fields = '__all__'

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        ata = AtaRegistroPreco.objects.create(**validated_data)
        for item_data in itens_data:
            ItemDaAta.objects.create(ata=ata, **item_data)
        return ata
