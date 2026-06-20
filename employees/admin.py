from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (
    Employee,
    EmployeeFamily,
    EmployeeEducation,
    EmployeeExperience,
    EmployeeLanguage,
    EmployeeDocument,
    AuditLog
)


class EmployeeFamilyInline(admin.TabularInline):
    model = EmployeeFamily
    extra = 1


class EmployeeEducationInline(admin.TabularInline):
    model = EmployeeEducation
    extra = 1


class EmployeeExperienceInline(admin.TabularInline):
    model = EmployeeExperience
    extra = 1


class EmployeeLanguageInline(admin.TabularInline):
    model = EmployeeLanguage
    extra = 1


class EmployeeDocumentInline(admin.TabularInline):
    model = EmployeeDocument
    extra = 1

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        import_id_fields = ('employee_code',)

        fields = (
            'employee_code',
            'employee_name',
            'father_husband_name',
            'date_of_birth',
            'age',
            'gender',
            'permanent_address',
            'permanent_pin',
            'present_address',
            'present_pin',
            'marital_status',
            'mobile_no',
            'aadhaar_no',
            'bank_account_no',
            'bank_name',
            'ifsc_code',
            'uan_number',
            'esi_number',
            'department',
            'designation',
            'date_of_joining',
            'salary_per_day',
        )

        exclude = (
            'created_at',
        )

        export_order = fields


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    
    list_display = (
        'employee_code',
        'employee_name',
        'mobile_no',
        'department',
        'designation',
        'date_of_joining',
        'salary_per_day'
    )



    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        AuditLog.objects.create(
            employee_id=obj.employee_id,
            action_type='UPDATE' if change else 'CREATE',
            performed_by=request.user.username,
            remarks=f"{obj.employee_code} - {obj.employee_name}"
        )
    

    search_fields = (
        'employee_code',
        'employee_name',
        'mobile_no',
        'aadhaar_no',
        'uan_number',
        'esi_number',
        'bank_account_no'
    )

    list_filter = (
        'department',
        'designation',
        'gender',
        'marital_status',
        'date_of_joining'
    )

    ordering = (
        'employee_code',
    )

    fieldsets = (
        ('1. Personal Details', {
            'fields': (
                'employee_code',
                'employee_name',
                'father_husband_name',
                'date_of_birth',
                'age',
                'photo',
                'gender',
                'marital_status',
                'mobile_no'
            )
        }),

        ('2. Address Details', {
            'fields': (
                'permanent_address',
                'permanent_pin',
                'present_address',
                'present_pin'
            )
        }),

        ('3. Identity Details', {
            'fields': (
                'aadhaar_no',
                'uan_number',
                'esi_number'
            )
        }),

        ('4. Bank Details', {
            'fields': (
                'bank_account_no',
                'bank_name',
                'ifsc_code'
            )
        }),

        ('5. Company Details', {
            'fields': (
                'department',
                'designation',
                'date_of_joining',
                'salary_per_day'
            )
        }),

    )

    inlines = [
        EmployeeFamilyInline,
        EmployeeEducationInline,
        EmployeeExperienceInline,
        EmployeeLanguageInline,
        EmployeeDocumentInline
    ]
admin.site.register(AuditLog)
