from rest_framework.decorators import api_view
from ..serializers import StudentModelSerializer
from ..models import Student
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET", "POST", "PUT","DELETE"]) # by default GET
def StudentAPI(request):
    if request.method == "GET":
        received_data = request.data
        id = received_data.get("id", None)
        if id is not None:
            student = Student.objects.get(id=id)
            serialized = StudentModelSerializer(student)
            return Response(serialized.data)
        student = Student.objects.all()
        serialized = StudentModelSerializer(student, many=True)
        return Response(serialized.data)
    
    elif request.method == "POST":
        serialized = StudentModelSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        else:
            return Response(serialized.errors)
        
    elif request.method == "PUT":
        received_data=request.data
        id=received_data.get('id',None)
        if id is not None:
            student = Student.objects.get(id=id)
            serialized=StudentModelSerializer(student, data=received_data,partial=True)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data)
            else:
                return Response(serialized.errors)
            
    elif request.method == "DELETE":
        id = request.data.get('id')
        try:
            student = Student.objects.get(id=id)
            student.delete()
            return Response("Your student data has been deleted", status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response("Student not found", status=status.HTTP_404_NOT_FOUND)
        