from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.models import User
from .models import Classroom, Student
from .forms import ClassroomForm, StudentForm, SigninForm, SignupForm

from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):

	classroom = Classroom.objects.get(id=classroom_id)
	students = Student.objects.filter(classroom=classroom).order_by('name', '-exam_grade')

	context = {
		"classroom": classroom,
		"students": students,
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	if request.user.is_anonymous:
		return redirect('signin')
		
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST)
		if form.is_valid():
			
			classr = form.save(commit=False)
			classr.teacher = request.user
			classr.save()

			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)

	context = {
	"form": form,
	}

	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)

	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	Classroom.objects.get(id=classroom_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')


def signup(request):
	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)

			user.set_password(user.password)
			user.save()

			login(request, user)
			return redirect("classroom-list")
	
	context = {
		"form":form,
	}

	return render(request, 'signup.html', context)

def signout(request):
	logout(request)
	return redirect("signin")


def signin(request):
	form = SigninForm()
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('classroom-list')
	
	context = {
		"form":form,
	}
	return render(request, 'signin.html', context)


def student_create(request, classroom_id):

	if request.user.is_anonymous:
		return redirect('signin')
		
	form = StudentForm()
	classroom = Classroom.objects.get(id = classroom_id)

	if not (request.user.is_staff or request.user == classroom.teacher):
        # return redirect('no-access')
		return HttpResponse("<h1> You shall not pass!!</h1>")

	if request.method == "POST":
		form = StudentForm(request.POST)

		if form.is_valid():

			student = form.save(commit=False)

			student.classroom = classroom
			student.save()

			messages.success(request, "Successfully Created!")
			return redirect(classroom)
		print ("form.errors: ", form.errors)

	context = {
	"form": form,
	"classroom": classroom,
	}

	return render(request, 'create_student.html', context)


def student_update(request, classroom_id, student_id):
	
	student = Student.objects.get(id=student_id)
	classroom = Classroom.objects.get(id=classroom_id)

	# form = StudentForm(instance=student)

	# if request.method == "POST":
	# 	form = StudentForm(request.POST, instance=student)
	# 	if form.is_valid():
	# 		form.save()
	# 		messages.success(request, "Successfully Edited!")
	# 		return redirect(classroom.get_absolute_url())

	if request.user == classroom.teacher:
		form = StudentForm(instance=student)

	if request.method == "POST":
		form = StudentForm(request.POST, instance=student)
		if form.is_valid():
			form.save()
			messages.success(request, "Student Successfully Edited!")
			return redirect(classroom)

	context = {
	"form": form,
	"classroom": classroom,
	"student": student,
	}
	return render(request, 'update_student.html', context)


def student_delete(request, classroom_id, student_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if request.user == classroom.teacher:
		Student.objects.get(id=student_id).delete()
		messages.success(request, "Student Successfully Deleted!")
		return redirect(classroom.get_absolute_url())