from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import (
    Employee,
    EmployeeFamily,
    EmployeeEducation,
    EmployeeExperience,
    EmployeeLanguage
)

def dashboard(request):
    total_employees = Employee.objects.count()

    context = {
        "total_employees": total_employees
    }

    return render(
        request,
        "employees/dashboard.html",
        context
    )


def employee_list(request):

    search = request.GET.get('search', '')

    employees = Employee.objects.all()

    if search:
        employees = employees.filter(
            employee_name__icontains=search
        )

    return render(
        request,
        "employees/employee_list.html",
        {
            "employees": employees,
            "search": search
        }
    )

def print_biodata(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)

    context = {
        'employee': employee,
        'family_details': EmployeeFamily.objects.filter(employee=employee),
        'education_details': EmployeeEducation.objects.filter(employee=employee),
        'experience_details': EmployeeExperience.objects.filter(employee=employee),
        'languages': EmployeeLanguage.objects.filter(employee=employee),
    }

    return render(
        request,
        'employees/print_biodata.html',
        context
    )

def download_biodata_pdf(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)

    context = {
        'employee': employee,
        'family_details': EmployeeFamily.objects.filter(employee=employee),
        'education_details': EmployeeEducation.objects.filter(employee=employee),
        'experience_details': EmployeeExperience.objects.filter(employee=employee),
        'languages': EmployeeLanguage.objects.filter(employee=employee),
    }

    template = get_template('employees/print_biodata.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{employee.employee_code}_biodata.pdf"'

    pisa_status = pisa.CreatePDF(
        html,
        dest=response
    )

    if pisa_status.err:
        return HttpResponse('PDF generation failed')

    return response
