from django.urls import path, include
from mainapp.views import function_based_views,class_based_views,function_based_api_views,class_based_API_views

urlpatterns = [
    # Function based views URL
    
    # path("student_api/", function_based_views.student_api),
    # path("student_api_detail/<int:id>", function_based_views.student_api_detail)
    
    # class Based View
    #path("student_api/",class_based_views.StudentAPI.as_view()),1
    
    # """ Function based API views """
    #path("student_api/",function_based_api_views.StudentAPI)
    
    # """ class Based API View"""
    path("student_api/",class_based_API_views.StudentAPI.as_view())
    
    
    
    
    
]
