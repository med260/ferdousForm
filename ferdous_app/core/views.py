from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher, Student


# Home Page
def home(request):
    return render(request, "home.html")


# Teacher Form Page
def teacher_form(request):

    if request.method == "POST":

        name = request.POST.get("name")
        dob = request.POST.get("dob")
        national_id = request.POST.get("national_id")
        class_name = request.POST.get("class_name")
        phone_number = request.POST.get("phone_number")

        num_students = request.POST.get("num_students")

        if not num_students:
            return redirect("teacher_form")

        num_students = int(num_students)

        teacher = Teacher.objects.create(
            name=name,
            date_of_birth=dob,
            national_id=national_id,
            phone_number=phone_number,
            class_name=class_name,
            student_count=num_students
        )

        request.session["teacher_id"] = teacher.id

        return redirect(
            "students_form",
            count=num_students
        )

    return render(request, "teacher_form.html")


# Students Form Page
def students_form(request, count):

    if request.method == "POST":

        teacher_id = request.session.get("teacher_id")
        teacher = Teacher.objects.get(id=teacher_id)

        names = request.POST.getlist("student_name")
        ages = request.POST.getlist("student_age")
        phones = request.POST.getlist("parent_phone")
        juzs = request.POST.getlist("memorized_juz")

        for n, a, p, j in zip(names, ages, phones, juzs):

            if n:

                Student.objects.create(
                    teacher=teacher,
                    name=n,
                    age=a,
                    parent_phone=p,
                    memorized_juz=j
                )

        return redirect(
            'success_view',
            t_id=teacher.teacher_id
        )

    return render(
        request,
        "students_form.html",
        {"count": range(count)}
    )


# Success Page
def success_view(request, t_id):

    teacher = get_object_or_404(
        Teacher,
        teacher_id=t_id
    )

    return render(
        request,
        'success.html',
        {'teacher': teacher}
    )