from rest_framework.views import APIView
from ..serializers import StudentModelSerializer
from ..models import Student
from rest_framework.response import Response
from rest_framework import status


class StudentAPI(APIView):
    def get(self, request, *args, **kwargs):
        received_data = request.data
        id = received_data.get('id',None)
        if id is not None:
            student=Student.objects.get(id=id)
            serialized=StudentModelSerializer(student)
            return Response(serialized.data)
        student=Student.objects.all()
        serialized=StudentModelSerializer(student,many=True)
        return Response(serialized.data)
    
    def post(self, request, *args, **kwargs):
        received_data= request.data
        serialized= StudentModelSerializer(data=received_data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        else:
            return Response(serialized.errors)
        
    def put(self, request, *args, **kwargs):
        received_data=request.data
        id = received_data.get('id',None)
        student= Student.objects.get(id=id)
        serialized= StudentModelSerializer(instance=student,data=received_data,partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        else:
            return Response(serialized.errors)
        
        
    def delete(self, request, *args, **kwargs): 
        try:
            id=request.data.get('id',None)
            student=Student.objects.get(id=id)
            student.delete()
            return Response("Data deleted successfully")
        except Student.DoesNotExist as e:
            print(e)
            return Response(str(e).upper()+f' with ID :{id}'.upper())
