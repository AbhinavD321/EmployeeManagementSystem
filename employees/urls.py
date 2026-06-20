from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('print-biodata/<int:employee_id>/',
         views.print_biodata,
         name='print_biodata'),
    path(
        'download-biodata-pdf/<int:employee_id>/',
        views.download_biodata_pdf,
        name='download_biodata_pdf'),
]
