from .models import Article, Shelf, Warehouse
from django.http.response import JsonResponse
from django.db.models import F, Sum
from rest_framework.parsers import JSONParser
from rest_framework import status
from appAPI.serializers import ArticleSerializer, ShelfSerializer, WarehouseSerializer, ShelfRowBaySerializer, \
    WarehouseDetailSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def articles_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        return JsonResponse(list(articles.values('id', 'name')), safe=False)

    elif request.method == 'POST':
        article_data = JSONParser().parse(request)
        article_serializer = ArticleSerializer(data=article_data)
        if article_serializer.is_valid():
            article_serializer.save()
            return JsonResponse(article_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def articles_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return JsonResponse({'message': 'The article does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        article_serializer = ArticleSerializer(article)
        return JsonResponse(article_serializer.data)

    elif request.method == 'PATCH':
        article_data = JSONParser().parse(request)
        article_serializer = ArticleSerializer(article, data=article_data,
                                               partial=True)  # set partial=True to update a data partially
        if article_serializer.is_valid():
            article_serializer.save()
            return JsonResponse(article_serializer.data)
        return JsonResponse(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return JsonResponse({'message': 'Article was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def shelves_list(request):
    if request.method == 'GET':
        shelves = Shelf.objects.all()

        return JsonResponse(list(shelves.values('row', 'bay')), safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        shelf_data = JSONParser().parse(request)
        shelf_serializer = ShelfSerializer(data=shelf_data)
        if shelf_serializer.is_valid():

            # Validate that the shelf noes not exist
            try:
                shelf = Shelf.objects.get(row=shelf_data['row'], bay=shelf_data['bay'])
                return JsonResponse({'message': 'The shelf already exists'}, status=status.HTTP_302_FOUND)
            except Shelf.DoesNotExist:
                pass

            shelf_serializer.save()
            return JsonResponse(shelf_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(shelf_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def shelves_by_row(request, row):
    shelves = Shelf.objects.filter(row=row)
    if not shelves:
        return JsonResponse({'message': 'The shelf does not exist'}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse(list(shelves.values('bay')), safe=False)


@api_view(['GET', 'PATCH', 'DELETE'])
def shelves_detail(request, row, bay):
    try:
        shelf = Shelf.objects.get(row=row, bay=bay)
    except Shelf.DoesNotExist:
        return JsonResponse({'message': 'The shelf does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        shelf_serializer = ShelfRowBaySerializer(shelf)
        return JsonResponse(shelf_serializer.data)

    elif request.method == 'PATCH':
        shelf_serializer = ShelfSerializer(shelf, data=request.data,
                                           partial=True)  # set partial=True to update a data partially
        if shelf_serializer.is_valid():
            shelf_serializer.save()
            return JsonResponse(shelf_serializer.data)
        return JsonResponse(shelf_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        shelf.delete()
        return JsonResponse({'message': 'Shelf was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT'])
def warehouse_list(request):
    if request.method == 'GET':

        if 'row' in request.GET or 'bay' in request.GET or 'id' in request.GET:

            try:
                shelf = Shelf.objects.get(row=request.GET['row'], bay=request.GET['bay'])
            except Shelf.DoesNotExist:
                return JsonResponse({'message': 'The shelf does not exist'}, status=status.HTTP_404_NOT_FOUND)

            try:
                article = Article.objects.get(pk=request.GET['id'])
            except Article.DoesNotExist:
                return JsonResponse({'message': 'The article does not exist'}, status=status.HTTP_404_NOT_FOUND)

            w_list = Warehouse.objects.filter(shelf=shelf, article=article).annotate(total=Sum('amount'))

            warehouse_serializer = WarehouseDetailSerializer(w_list, many=True)
            return JsonResponse(warehouse_serializer.data, safe=False)

        warehouse = Warehouse.objects.all()
        warehouse_serializer = WarehouseSerializer(warehouse, many=True)
        return JsonResponse(warehouse_serializer.data, safe=False)

    elif request.method == 'POST':
        warehouse_data = JSONParser().parse(request)

        # Validate that the article noes not exist
        try:
            article = Article.objects.get(id=warehouse_data['id'])
        except Article.DoesNotExist:
            return JsonResponse({'message': 'The article does not exists'}, status=status.HTTP_302_FOUND)
        except KeyError:
            return JsonResponse({'id': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            shelf = Shelf.objects.get(row=warehouse_data['row'], bay=warehouse_data['bay'])
        except Shelf.DoesNotExist:
            return JsonResponse({'message': 'The shelf does not exists'}, status=status.HTTP_302_FOUND)
        except KeyError as exc:
            return JsonResponse({exc.args[0]: ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        warehouse_data['article'] = article.id
        warehouse_data['shelf'] = shelf.id
        warehouse_serializer = WarehouseSerializer(data=warehouse_data)

        if warehouse_serializer.is_valid():
            warehouse_serializer.save()
            return JsonResponse(warehouse_serializer.data)
        return JsonResponse(warehouse_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        warehouse_data = JSONParser().parse(request)

        try:
            shelf = Shelf.objects.get(row=warehouse_data['row'], bay=warehouse_data['bay'])
        except Shelf.DoesNotExist:
            return JsonResponse({'message': 'The shelf does not exist'}, status=status.HTTP_404_NOT_FOUND)

        warehouse_serializer = ShelfSerializer(shelf, data=request.data,
                                               partial=True)  # set partial=True to update a data partially
        if warehouse_serializer.is_valid():
            warehouse_serializer.save()
            return JsonResponse(warehouse_serializer.data)
        return JsonResponse(warehouse_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
