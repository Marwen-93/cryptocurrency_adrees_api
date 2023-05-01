from rest_framework.response import Response
from .models import ValidAddress
from .serializers import ValidAddressSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from .addresses_generator import *

PRIVKEY_HEX = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"


# 1. Create
@api_view(['POST'])
def generate_address(request):
    if request.method == 'POST':
        private_key = bytes.fromhex(PRIVKEY_HEX)
        public_key = generate_public_key(private_key, ValidAddress)
        address = generate_address_for_currency(public_key, request.data.get('name'))

        data = {
            'currency': request.data.get('name'),
            'address': address,
            'public_key': str(public_key)

        }
        serializer = ValidAddressSerializer(data=data)

        if address and serializer.is_valid():
            serializer.save()
            return Response({
                'address': address,

            }, status=status.HTTP_201_CREATED)
        elif not address:
            return Response({
                "message": "unsupported currency"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2.list
@api_view(['GET'])
def list_address(request):
    if request.method == 'GET':
        data = ValidAddress.objects.all()
        serializer = ValidAddressSerializer(data, many=True)
        data = serializer.data
        new_data = []
        for item in data:
            new_item = {}
            new_item['id'] = item['id']
            new_item['address'] = item['address']
            new_data.append(new_item)
        return Response(new_data, status=200)


# 3.retrive
@api_view(['GET'])
def retrieve_address(request, pk):
    try:
        address = ValidAddress.objects.get(pk=pk)
    except ValidAddress.DoesNotExist:
        return Response({"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ValidAddressSerializer(address)
    data = serializer.data
    return Response({"id": data["id"], "address": data["address"]}, status=status.HTTP_200_OK)
