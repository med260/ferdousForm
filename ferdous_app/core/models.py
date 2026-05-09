from django.db import models
from django.core.validators import RegexValidator ,MaxValueValidator
from datetime import date
 
class Teacher(models.Model):
    name = models.CharField(max_length=255)
    # Auto-generated ID: TCH-001
    teacher_id = models.CharField(max_length=20, unique=True, editable=False)
    date_of_birth = models.DateField()
    # National ID: Required 14 digits
    national_id = models.CharField(
        max_length=14,
        unique=True,
        default="00000000000000",
        validators=[
            RegexValidator(
                regex=r'^\d{14}$',
                message='National ID must be exactly 14 digits.'
            )
        ]
    )
    # Cleaned Phone Field: No default, allows null for existing records
    phone_number = models.CharField(
        max_length=11, 
        unique=True, 
        null=True, 
        blank=True,
        validators=[RegexValidator(r'^\d{11}$', 'Must be 11 digits')]
    )

    gmail = models.EmailField(max_length=255, blank=True, null=True)
    # student_count can be kept as a manual field, 
    # but usually, we calculate this from the relationship
    student_count = models.PositiveIntegerField(default=0, verbose_name="Number of Students")
    class_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            count = Teacher.objects.count() + 1
            self.teacher_id = f"TCH-{count:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.teacher_id} - {self.name}"


class Student(models.Model):
    name = models.CharField(max_length=255)
    # Link to Teacher
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.CASCADE, 
        related_name='students'
    )
    
    # Auto-generated ID: STU-001 (Unique per teacher)
    student_id = models.CharField(max_length=20, editable=False)

    memorized_juz = models.IntegerField(
        choices=[(i, str(i)) for i in range(31)],
        default=0
    )
    
    parent_phone = models.CharField(
        max_length=20
    )

    age = models.PositiveIntegerField(
        validators=[MaxValueValidator(20)]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures STU-001 is only unique for that specific teacher
        unique_together = ('teacher', 'student_id')

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Count how many students this specific teacher already has
            current_count = Student.objects.filter(teacher=self.teacher).count() + 1
            self.student_id = f"STU-{current_count:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_id} - {self.name} (Tutor: {self.teacher.name})"