import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render 
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse
from .forms import PostForm
from .models import User, Post, Follower


def index(request):
    myPostForm=  PostForm()
    post_list=Post.objects.all().order_by('-date')
    # paginator = Paginator( post_list, 10)  
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)    
    if request.method =='POST':
          myPostForm=PostForm(request.POST)
          if myPostForm.is_valid():
             obj = myPostForm.save(commit=False)
             obj.user = request.user
             obj.save()
    post_list_paginator=retPaginatorList(request,post_list)
    return render(request, "network/index.html",{'PostForm':myPostForm, 'post_list':post_list_paginator,})


def Find_no_of_follower(profile_user):
    follow=Follower.objects.all().filter(user=profile_user)
    fList=[]
    no_follower = 0
    for item in follow:
         fList.append((item.user_follower))

    for us in fList:
        if Follower.objects.all().filter(user=us,user_follower=profile_user):
            no_follower += 1

    return no_follower


@login_required
def follow(request,pro_id):

        prof_user=User.objects.all().get(id=pro_id)
        delete_follower = Follower.objects.filter(user=request.user,user_follower=prof_user)
        if delete_follower:
            delete_follower.delete()
            return HttpResponseRedirect(reverse('profile', args=(pro_id,)))

        else:
            new_follower = Follower.objects.create(user=request.user,user_follower=prof_user)
            new_follower.save()
            return HttpResponseRedirect(reverse('profile', args=(pro_id,)))
 
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def profile(request,id):
    fol_unfol='follow' 
    no_follower = 0 
    profile_user=User.objects.all().get(id=id)
    post_list=Post.objects.all().filter(user=profile_user)
    countFollowing = Follower.objects.filter(user=profile_user).count()
    no_follower = Find_no_of_follower(profile_user)
    
    if profile_user== request.user:
        disp='none'
    else:
        disp='block'
        test_follow = Follower.objects.all().filter(user=request.user, user_follower=profile_user)
        if test_follow:
            fol_unfol = 'unfollow'
        else:
            fol_unfol = 'follow'
    post_list_paginator=retPaginatorList(request,post_list)
    return render(request,'network/profile.html', {'profile_user':profile_user, 'post_list':post_list_paginator, 'no_following':countFollowing, 'no_follower':no_follower,'disp_follow':disp,
         'fol_unfol':fol_unfol,})


   
@login_required 
def following_posts(request):
    f_posts=Post.objects.all().filter(user=None)
    following_list=Follower.objects.all().filter(user=request.user)
    
    for item in following_list:
        f_posts=Post.objects.all().filter(user=item.user_follower)
        f_posts=f_posts.order_by('-date')
        post_list_paginator=retPaginatorList(request,f_posts)

    return render (request,'network/following_posts.html', {'post_list':post_list_paginator,})

@csrf_exempt
@login_required
def like(request):
    data = json.loads(request.body)
    post = Post.objects.get(id = data.get('id'))
    liked = False
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        post.likes_count -= 1
    else:
        post.likes.add(request.user)
        post.likes_count += 1
        liked = True
    post.save()

    return JsonResponse({
            "likes_count": post.likes_count,
            "liked": liked,
    })



@csrf_exempt
@login_required
def edit_post(request, id):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    else:

     data = json.loads(request.body)
     body = data.get("body", "")
     print('post body is', body)
    try:
        post = Post.objects.all().get(id=id, user=request.user)
        post.content = body
        post.date = datetime.now()
        post.save()
        return JsonResponse({"message": "Email sent successfully."}, status=201)
    except Post.DoesNotExist:
        return JsonResponse({
            "error": f"post with id {id} does not exist."
        }, status=400)



def retPaginatorList(request, queryList):
    page = request.GET.get('page')
    mypge = Paginator(queryList, 10)
    try:
        resultList = mypge.page(page)
    except PageNotAnInteger:
        resultList = mypge.page(1)
    except EmptyPage:
        resultList = mypge.page(mypge.num_pages)

    return  resultList