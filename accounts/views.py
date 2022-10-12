from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from zcore.decorators import unauthenticated_user

@unauthenticated_user
def register(request):
	if request.method == "POST":
		username = request.POST['username'].lower()
		# group_name = request.POST['group'].lower()
		first_name = request.POST['first_name'].lower()
		last_name = request.POST['last_name'].lower()
		password = request.POST['password']
		password2 = request.POST['password2']

		if not User.objects.filter(username=username).exists():
			if not User.objects.filter(email=username).exists():
				if password != password2:
					messages.error(request, "Passwords do not match!")
					return render(request, 'register.html', status=409)
				if len(password) < 4:
					messages.error(request, "Passwords must have minimum length of 4")
					return render(request, 'register.html', status=409)
				else:
					user = User.objects.create_user(username=username, password=password, first_name=first_name , last_name=last_name)
					user.is_active = False
					# group = Group.objects.get(name="default")
					# user.groups.add(group)
					user.save()
					messages.success(request, "Successfully registered! wait for an admin to approve your account")
					user.save()
					return redirect('login')
		messages.error(request, "something went wrong")

		if User.objects.filter(username=username).exists():
			messages.error(request, 'Email already taken')
			return render(request, 'register.html', status=409)
		
		elif password != password2:
			messages.error(request, 'Passwords do not match')
			return redirect('register')
		
		else:
			user = User.objects.create_user(username=username, password=password, first_name=first_name , last_name=last_name)
			user.is_active = False
			# group = Group.objects.get(name=group_name)
			# user.groups.add(group)
			user.save()
			messages.success(request, 'Account created')
			user.save()
			return redirect('login')

	context = {

	}
	return render(request, 'register.html', context)

@unauthenticated_user
def login_view(request):
	if request.method == "POST":
		username = request.POST['username'].lower()
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request, user)
			messages.success(request, 'Successfully logged in')
			# if user.is_superuser:
			# 	return redirect('home')
			return redirect('dashboard')
		else:
			print("invalid credentials")
			messages.error(request, 'Invalid credentials')
			return redirect('login')
	context = {
	
	}
	return render(request, 'login.html', context)

def dashboard(request):
	current_user = request.user
	# print(current_user)
	if current_user.is_superuser:
		user_groups = Group.objects.exclude(name="admin").all()
	else:
		user_groups = current_user.groups.exclude(name="admin").all()
		
	# user_groups = current_user.groups.all()
	# user = User.objects.get(id=current_user)
	
	# usergroups = user.groups.all()
	context = {
		"groups": user_groups ,
		"firstname": "People",
		"admin": current_user.is_superuser
	}
	return render(request, "dashboard.html" , context)

def adminregister(request):
	return render(request, 'adminregister.html')

def adminlogin(request):
	return render(request, 'adminlogin.html')


@login_required(login_url="login")
def logout_view(request):
	logout(request)
	messages.success(request, 'You have been logged out')
	return redirect('login')