from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StoreValue
from .serializers import StoreValueSerializer


class StoreView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'key',
                openapi.IN_QUERY,
                description="The key to filter by (optional). If not provided, returns all keys.",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description="Success",
                examples={
                    "application/json": {
                        "single_key_example": {"key": "example_key", "value": "example_value"},
                        "all_keys_example": [
                            {"key": "example_key1", "value": "example_value1"},
                            {"key": "example_key2", "value": "example_value2"}
                        ]
                    }
                }
            ),
            404: "Not Found"
        }
    )
    def get(self, request):
        data = request.data
        if 'key' in data:
            store_value_query_set = StoreValue.objects.filter(key=data.get('key'))
            if store_value_query_set.count() == 0:
                return Response({'error': 'Key not found'}, status=404)
            data = StoreValueSerializer(store_value_query_set.get(), many=False).data
            return Response(data)
        store_value_query_set = StoreValue.objects.all()
        if store_value_query_set.count() == 0:
            return Response({'error': 'No keys set'}, status=404)
        data = StoreValueSerializer(store_value_query_set, many=True).data
        return Response(data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['key'],
            properties={
                'key': openapi.Schema(type=openapi.TYPE_STRING, description='Key to store'),
                'value': openapi.Schema(type=openapi.TYPE_STRING, description='Value associated with the key'),
            }
        ),
        responses={
            200: "Success",
            400: "Bad Request"
        }
    )
    def post(self, request):
        data = request.data
        if 'key' not in data:
            return Response('key is required')
        value = data.get('value', None)
        key = data.get('key')
        store_value_object, _ = StoreValue.objects.get_or_create(key=key)
        store_value_object.value = value
        store_value_object.save(update_fields=["value"])
        data = StoreValueSerializer(store_value_object, many=False).data
        return Response(data)
