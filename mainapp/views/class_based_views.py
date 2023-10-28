from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import io
from rest_framework.parsers import JSONParser
from ..models import Student
from ..serializers import StudentModelSerializer
from rest_framework.renderers import JSONRenderer


@method_decorator(csrf_exempt,name='dispatch')
class StudentAPI(View):
    def get(self, request, *args, **kwargs):
        # body probably like binary
        json_data = request.body
        stream = io.BytesIO(json_data)  # binary data converted
        Data = JSONParser().parse(stream)  # json
        id = Data.get("id", None)

        if id is not None:
            student = Student.objects.get(id=id)
            serializer = StudentModelSerializer(student)
            response = JSONRenderer().render(serializer.data)
            return HttpResponse(response, content_type="application/json")

        student = Student.objects.all()
        serializer = StudentModelSerializer(student, many=True)  # many=True bcz get method
        response = JSONRenderer().render(serializer.data)
        return HttpResponse(response, content_type="application/json")

    def post(self, request, *args, **kwargs):
        received_data = request.body
        stream = io.BytesIO(received_data)
        parsed_data = JSONParser().parse(stream)

        serializer = StudentModelSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            response = JSONRenderer().render(serializer.data)
        else:
            response = JSONRenderer().render(serializer.errors)
        
        return HttpResponse(response, content_type="application/json")
    
    
    def put(self, request, *args, **kwargs):
        received_data = request.body
        stream = io.BytesIO(received_data)
        parsed_data = JSONParser().parse(stream)
        id=parsed_data.get('id', None)
        student= Student.objects.get(id=id)
        serializer=StudentModelSerializer(student,data=parsed_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            response=JSONRenderer().render(serializer.data)
        else:
            response = JSONRenderer().render(serializer.errors)
        return HttpResponse(response,content_type='application/json')
        
    def delete(self, request, *args, **kwargs):
        received_data = request.body
        stream = io.BytesIO(received_data)
        parsed_data = JSONParser().parse(stream)
        id=parsed_data.get('id', None)
        Student.objects.get(id=id).delete()
        response=JSONRenderer().render({"message": "Student deleted"})
        return HttpResponse(response,content_type='application/json')
