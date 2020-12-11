from .models import Profile
from json import loads
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from Pytreddit.redis_utils import get_redis_instance
from users.models import Profile
from rest_framework.response import Response


redis_manager = get_redis_instance()


def get_user_id(redis = redis_manager):
	return redis.Rget("PersonID")

def clear_from_cache(redis = redis_manager):
	return redis.Rdelete("PersonID")

def Unathorized_401():
	return HttpResponse("Login or password is wrong", status=401)


def authorize(user_query, body, redis = redis_manager):
	user = user_query.filter(password=body["password"])
	if len(user) < 1:
		return Unathorized_401()
	user = user[0]
	redis_manager.Rput('PersonID',user.id)
	return HttpResponse(f"Welcome {str(user)}", status=200)


def login(request, redis=redis_manager):
	if redis.Rget('PersonID'):
		return HttpResponse("You are still logged in.", status=400)

	body = loads(request.body)
	keys = body.keys()

	if "password" in keys:
		user = Profile.objects.all()
		if "login" in keys:
			user = user.filter(login=body["login"])
			return authorize(user, body)

		elif "username" in keys:
			user = user.filter(username=body["username"])
			return authorize(user, body)

		elif "phone" in keys:
			user = user.filter(phone=body["phone"])
			return authorize(user, body)

	return Unathorized_401()


def logout(request, redis=redis_manager):
	if redis.Rget('PersonID'):
		redis.Rdelete('PersonID')
		return HttpResponse("Logged out successfully", status=200)

	return HttpResponse("You are currently logged out.", status=401)
