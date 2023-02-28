from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .seializers import ApiSerializers
from .models import ApiModel
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.views.decorators.csrf import csrf_protect, csrf_exempt

# Create your views here.

class ApiTestView(APIView):
    def get(self, request):
        queryset = ApiModel.objects.all()

        serializer = ApiSerializers(queryset, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        serializer = ApiSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def test(request):

    return render(request, 'test.html')


@csrf_exempt
def newtest(request):

    if request.method == "GET":
        queryset = ApiModel.objects.all()
        print(queryset)
        serializer = ApiSerializers(queryset, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ApiSerializers(data=data)
        print(serializer.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



class ApiModelView(viewsets.ModelViewSet):
    serializer_class = ApiSerializers
    queryset = ApiModel.objects.all()
