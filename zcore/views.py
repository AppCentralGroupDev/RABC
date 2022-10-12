from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import admin_only, allowed_users, unauthenticated_user
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import Group
from zcore.models import Description

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def home(request):
	users = User.objects.all().exclude(username=request.user.username)
	context = {
		"users": users,
	}
	return render(request, "index.html", context)

# @unauthenticated_user
@allowed_users(allowed_roles=["customer"])
def customer_page(request):
    
	context = {
		"message": "I am customer"
	}
	return render(request, "customer_page.html", context)

# @allowed_users(allowed_roles=["pages"])
login_required(login_url="login")
def pages(request , page_name):
    current_user = request.user 
    # user_groups = current_user.groups.all()
    # user_groups = current_user.groups.all()
    # user_groups = current_user.groups.all()
	# context = {
	# 	"message": current_user.groups.all()
	# }
	

    if current_user.is_superuser:
        context = {
			"group": Group.objects.filter(name=page_name)[0], 
			"model_name": page_name,
			"Access": True,
			"admin": True
		}
        return render(request, "streamlit.html", context)
	
    if current_user.groups.filter(name=page_name).exists():
        context = {
			"group": current_user.groups.filter(name=page_name)[0], 
			"model_name": page_name,
			"Access": True,
			"admin": False
		}
        # return render(request, "streamlit.html", context)
    else:
        context = {
			"message": "No Access",
			"model_name": page_name,
			"Access": False, 
			"admin": False
		}
    return render(request, "streamlit.html", context)

# def dashboard(request):
# 	# current_user = request.user
# 	# print(current_user)
# 	# # user_groups = current_user.groups.all()
# 	# user = User.objects.get(id=current_user)
	
# 	# usergroups = user.groups.all()
# 	context = {
# 		# "groups": usergroups ,
# 		"groups": "hello" ,
# 		"firstname": "People",
# 		# "group_count": len(user_groups)
# 	}
# 	return render(request, "customer_page.html" , {"firstname": "kilo",})

@allowed_users(allowed_roles=["page1"])
def page1(request):
	context = {
		"message": "You can only view page1"
	}
	return render(request, "page1.html", context)

@allowed_users(allowed_roles=["page2"])
def page2(request):
	context = {
		"message": "You can only view page2"
	}
	return render(request, "page2.html", context)





@allowed_users(allowed_roles=["manager"])
def manager_page(request):
	context = {
		"message": "I am manager"
	}
	return render(request, "manager.html", context)


@allowed_users(allowed_roles=["admin"])
def admin_page(request):
	context = {
		"message": "I am admin"
	}
	return render(request, "admin.html", context)

@admin_only
def add_new_group(request):
	if request.method == "POST":
		name = request.POST.get('name')
		Group.objects.create(name=name)
		messages.success(request, "group added successfully")
		return redirect('home')
	return render(request, "add_group.html")

###################################

@admin_only
def add_model(request):
	if request.method == "POST":
		name = request.POST.get('name')
		try:
			print('hello')
		except Exception as e :
			pass
			
		current_stage = request.POST.get('current_stage')
		version = request.POST.get('version')
		model_author = request.POST.get('model_author')
		model_url = request.POST.get('model_url')
		# status = request.POST.get("status")
		# last_updated = 
  		
		desc = request.POST.get("description")
		new_group = Group.objects.create(name=name)
		new_group.save()
		new_desc = Description(
			group=new_group,
			current_stage=current_stage,
			version=version,
			model_author=model_author,
			model_url=model_url,
			description=desc,
		)
		new_desc.save()
		
		messages.success(request, "model added successfully")
		return redirect('home')
	return render(request, "add_group.html")

#####################################


@admin_only
def assign_user(request,user_id):
	if request.method == "POST":
		pass
	user = User.objects.get(id=user_id)
	Allgroups = Group.objects.exclude(user=user)
	
	usergroups = user.groups.all()
	username = user.username
	context={
		"groups" : Allgroups,
		"usergroups" : usergroups, 
		"username": username,
		"user_id": user.id
	}
	return render(request, "assign_user.html" ,context)

@admin_only 
def add_user_group(request,group_name,user_id):
	if request.method == "GET":
		user = User.objects.get(id=user_id)
		my_group = Group.objects.get(name=group_name)
		my_group.user_set.add(user)
	return redirect('assign_user', user_id=user_id)

@admin_only 
def remove_user_group(request,group_name,user_id):
	if request.method == "GET":
		user = User.objects.get(id=user_id)
		my_group = Group.objects.get(name=group_name)
		my_group.user_set.remove(user)
	return redirect('assign_user', user_id=user_id)


@admin_only
@require_http_methods(['GET'])
def approve_user_account(request, user_id):
	user = User.objects.get(id=user_id)
	user.is_active = True
	user.save()
	messages.success(request, "User approved")
	return redirect('home')