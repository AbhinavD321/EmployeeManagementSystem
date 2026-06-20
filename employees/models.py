from django.db import models

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)

    employee_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    employee_name = models.CharField(max_length=150)

    father_husband_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    age = models.IntegerField(
        max_length=2,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=1,
        blank=True,
        null=True
    )

    permanent_address = models.TextField(
        blank=True,
        null=True
    )

    permanent_pin = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    present_address = models.TextField(
        blank=True,
        null=True
    )

    present_pin = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    marital_status = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    mobile_no = models.IntegerField(
        max_length=10,
        blank=True,
        null=True
    )

    aadhaar_no = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True
    )

    bank_account_no = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    bank_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    ifsc_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    uan_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    esi_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    department = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    designation = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    date_of_joining = models.DateField(
        blank=True,
        null=True
    )

    salary_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        blank=True,
        null=True
    )

    photo = models.ImageField(
        upload_to='employee_photos/',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.employee_code:
            last_employee = Employee.objects.order_by('-employee_id').first()

            if last_employee:
                next_id = last_employee.employee_id + 1
            else:
                next_id = 1

            self.employee_code = f"EMP{next_id:05d}"

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'employees'
        managed = False

    def __str__(self):
        return f"{self.employee_code} - {self.employee_name}"
    
class EmployeeFamily(models.Model):
    family_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')

    member_name = models.CharField(max_length=150, blank=True, null=True)
    relationship = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'employee_family'
        managed = False

    def __str__(self):
        return self.member_name or "Family Member"


class EmployeeEducation(models.Model):
    education_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')

    school_college = models.CharField(max_length=255, blank=True, null=True)
    course_name = models.CharField(max_length=255, blank=True, null=True)
    year_of_passing = models.IntegerField(blank=True, null=True)
    special_course = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'employee_education'
        managed = False

    def __str__(self):
        return self.course_name or "Education"


class EmployeeExperience(models.Model):
    experience_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')

    previous_concern = models.CharField(max_length=255, blank=True, null=True)
    nature_of_work = models.CharField(max_length=255, blank=True, null=True)
    period_of_work = models.CharField(max_length=100, blank=True, null=True)
    total_experience = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'employee_experience'
        managed = False

    def __str__(self):
        return self.previous_concern or "Experience"


class EmployeeLanguage(models.Model):
    language_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')

    language_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'employee_languages'
        managed = False

    def __str__(self):
        return self.language_name


class EmployeeDocument(models.Model):
    document_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')

    document_type = models.CharField(max_length=100, blank=True, null=True)
    document_number = models.CharField(max_length=100, blank=True, null=True)
    file_path = models.FileField(
        upload_to='employee_documents/',
        blank=True,
        null=True
        )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'employee_documents'
        managed = False

    def __str__(self):
        return self.document_type or "Document"
    
class AuditLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    employee_id = models.IntegerField(blank=True, null=True)
    action_type = models.CharField(max_length=50, blank=True, null=True)
    performed_by = models.CharField(max_length=100, blank=True, null=True)
    action_time = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'audit_logs'
        managed = False

    def __str__(self):
        return f"{self.action_type} - {self.performed_by}"
