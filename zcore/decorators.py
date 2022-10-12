from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wraper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)
	return wraper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wraper_func(request, *args, **kwargs):
			print("working allowed roles", allowed_roles)
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
				print(group)
			# if group == "page1":
			# 	return redirect("page1")
			# if group == "page2":
			# 	return redirect("page2")
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			if group == "customer":
				return redirect("customer")
			if group == "manager":
				return redirect("manager")
			
			else:
				return HttpResponse('Unauthorized user! you do not have view access')
		return wraper_func
	return decorator


def admin_only(view_func):
	def wraper_func(request, *args, **kwargs):
		if not request.user.is_staff:
			return HttpResponse('Unauthorized user! you do not have view access')
		else:
			return view_func(request, *args, **kwargs)
	return wraper_func






