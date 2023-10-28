from ..serializers import StudentSerializer
from django.views.decorators.csrf import csrf_exempt
from ..models import Student
from rest_framework.parsers import JSONParser
import io
from django.shortcuts import HttpResponse
from rest_framework.renderers import JSONRenderer


@csrf_exempt
def student_api(request):
    if request.method == 'GET':
        student = Student.objects.all()
        student_serializer = StudentSerializer(student, many=True)
        json_byte_data = JSONRenderer().render(student_serializer.data)
        return HttpResponse(json_byte_data, content_type='application/json')

    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = StudentSerializer(data=pythondata)

        if serializer.is_valid():
            serializer.save()
            json_data = JSONRenderer().render(serializer.data)
        else:
            json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type="application/json")


@csrf_exempt
def student_api_detail(request, id):
    if request.method == 'GET':
        student = Student.objects.get(id=id)
        student_serializer = StudentSerializer(student)
        json_byte_data = JSONRenderer().render(student_serializer.data)
        return HttpResponse(json_byte_data, content_type='application/json')
    
    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        student=Student.objects.get(id=id)
        serializer = StudentSerializer(student,data=pythondata,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            json_data=JSONRenderer().render(serializer.data)
        else:
            json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type="application/json")
    if request.method =="DELETE" :
        student= Student.objects.get(id=id)
        student.delete()
        response={
            "message": "Student deleted"
        }
        json_data=JSONRenderer().render(response)
        return HttpResponse(json_data,content_type="application/json")
        

        
