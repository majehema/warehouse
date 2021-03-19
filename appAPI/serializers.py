from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from appAPI.models import Article, Shelf, Warehouse
from django.db.models import F, Sum


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ('id',
                  'name',
                  'description')


class ArticleListSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ('id',
                  'name')


class ShelfSerializer(ModelSerializer):
    class Meta:
        model = Shelf
        fields = ('row',
                  'bay',
                  'height',
                  'width',
                  'depth')


class ShelfRowBaySerializer(ModelSerializer):
    class Meta:
        model = Shelf
        fields = ('height',
                  'width',
                  'depth')


class ShelfListSerializer(ModelSerializer):
    class Meta:
        model = Shelf
        fields = ('row',
                  'bay')


class WarehouseSerializer(ModelSerializer):
    #article = ArticleListSerializer(many=False)
    #shelf = ShelfSerializer(many=False)
    total_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Warehouse
        fields = ('article',
                  'shelf',
                  'amount',
                  'total_amount')

        #user=self.context['request'].user

    def get_total_amount(self, task):
        return Warehouse.objects.filter(article=task.article, shelf=task.shelf).aggregate(total=Sum('amount'))


class WarehouseDetailSerializer(ModelSerializer):
    article = ArticleListSerializer(many=False)
    #shelf = ShelfSerializer(many=False)
    total_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Warehouse
        fields = ('article',
                  'shelf',
                  'total_amount')

    def get_total_amount(self, data):
        return Warehouse.objects.filter(article=data.article, shelf=data.shelf).aggregate(total=Sum('amount'))
