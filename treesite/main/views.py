from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
import hashlib
from urllib.parse import urlencode
from .models import user_posts, trees, tree_type, permissions, user_trees
from .forms import PostForm, ProfileEdit
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def exploreView(request): 
    """VIEW 1"""
    """EXPLORE view, GET request for news feed"""
    if request.method == "GET":
        if request.user.is_authenticated:
            allPosts = []
            posts = user_posts.objects.all()
            for post in posts:
                description = post.description
                user_obj = post.user_id
                perm_type_obj = permissions.objects.get(user_id=request.user.id)
                tree_name = post.tree_name
                curr = {
                    "firstname": user_obj.first_name, "lastname": user_obj.last_name,
                    "description": post.description, "treename": tree_name,
                    "postid" : post.id, "permtype" : perm_type_obj.perm_type
                }
                allPosts.append(curr)
            return render(request, "main/explore.html", {'posts':allPosts}, status=200)
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)

def exploreDeletePost(request, post_id):
    """VIEW 1"""
    """EXPLORE view, DELETE request to delete only your own posts"""
    if request.method == "DELETE":
        if request.user.is_authenticated:
            post_obj = user_posts.objects.get(id=post_id)
            user = post_obj.user_id
            if user.id == request.user.id:
                user_posts.objects.filter(id=post_id).delete()
                return HttpResponseRedirect("main/explore.html")
            else:
                return HttpResponse("You are not authorized to delete another user's post.",
                status=401)
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)

def exploreMakeAPost(request):
    """VIEW 1"""
    """EXPLORE view, GET request to get a form to make a new post"""
    """EXPLORE view, POST request to post the newly created post onto the news feed"""
    if request.method == "GET":
        if request.user.is_authenticated:
            form = PostForm()
            return render(request, "main/makeapost.html", {"form":form}, status=200)
        else:
            return HttpResponse("User unauthorized.", status=401)
    elif request.method == "POST":
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                newPost = user_posts(user_id=request.user.id, 
                tree_name=form.cleaned_data["tree_name"], 
                description=form.cleaned_data["description"])
                newPost.save()
                return HttpResponseRedirect("main/explore.html")
            else:
                return HttpResponse("Invalid registration request.", status=400)
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)
        
def userProfileView(request):
    """VIEW 2"""
    """PROFILE view, GET request to get all of one's details onto a page"""
    if request.method == "GET":
        if request.user.is_authenticated:
            curr_user = User.objects.get(id=request.user.id)
            trees_owned = []
            for tree in user_trees.objects.all().filter(user_id=request.user.id):
                tree_obj = trees.objects.get(id=tree.trees_id)
                tree_type_obj = tree_type.objects.get(id=tree_obj.tree_type_id)
                curr = {
                    "age" : tree_obj.age, "status" : tree_obj.status,
                    "breed" : tree_type_obj.breed, "description" : tree_type_obj.description
                }
                trees_owned.append(curr)
            data = {
                "firstname": curr_user.first_name, "lastname" : curr_user.last_name,
                "email" : curr_user.email, "usertype" : curr_user.perm_type,
                "treesowned" : trees_owned
            }
            return render(request, "main/profile.html", {"data":data}, status=200)
        else:
            return HttpResponse("User unauthorized.", status=401)
    elif request.method == "DELETE":
        if request.user.is_authenticated:
            curr_user_perm_obj = permissions.objects.get(user_id=request.user.id)
            
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)

def userProfileEdit(request):
    """VIEW 2"""
    """PROFILE view, GET request to create a form to edit one's profile"""
    """PROFILE view, POST request to UPDATE one's new details onto database"""
    if request.method == "GET":
        if request.user.is_authenticated:
            form = ProfileEdit()
            return render(request, "main/editprofile.html", {'form':form}, status=200)
    elif request.method == "POST":
        if request.user.is_authenticated:
            form = ProfileEdit(request.POST)
            if form.is_valid():
                curr_user = User.objects.get(id=request.user.id)
                curr_user.first_name = form.cleaned_data["first_name"]
                curr_user.last_name = form.cleaned_data["last_name"]
                curr_user.perm_type = form.cleaned_data["perm_type"]
                curr_user.save()
                return HttpResponseRedirect("main/profile.html")
            else:
                return HttpResponse("Invalid registration request.", status=400)
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)

def adminView(request):
    """VIEW 3"""
    """ADMIN view, GET request for admins to see all users and posts"""
     if request.user.is_authenticated:
        curr_user_permission = permissions.objects.get(user_id=request.user)
        if curr_user_permission.perm_type == "Admin":
            if request.method == "GET":
                allUsers = []
                allPosts = []
                for user in User.objects.all():
                    curr = {
                        "firstname": user.first_name, "lastname" : user.last_name,
                        "email" : user.email, "type" : user.perm_type, "userid": user.id
                    }
                    allUsers.append(curr)
                for post in user_posts.objects.all():
                    description = post.description
                    user_obj = post.user_id
                    perm_type = user_obj.perm_type
                    tree_name = post.tree_name
                    curr = {
                        "firstname": user_obj.first_name, "lastname": user_obj.last_name,
                        "description": post.description, "treename": tree_name,
                        "postid" : post.id, "permtype" : perm_type
                    }
                    allPosts.append(curr)
                return render(request, "main/adminhome.html", 
                    {"users":allUsers, "posts":allPosts}, status=200)
            else:
                return HttpResponse("Method not allowed.", status=405)
        else:
            return HttpResponse("You are not authorized to delete.", status=401)
    else:
        return HttpResponse("User unauthorized.", status=401)

def adminDeletePost(request, post_id):
    """VIEW 3"""
    """ADMIN view, DELETE request for spam posts"""
    if request.method == "DELETE":
        if request.user.is_authenticated:
            curr_user_permission = permissions.objects.get(user_id=request.user)
            if curr_user_permission.perm_type == "Admin":
                post_obj = user_posts.objects.get(id=post_id)
                user = post_obj.user_id
                user_posts.objects.filter(id=post_id).delete()
                return HttpResponseRedirect("main/adminhome.html")
            else:
                return HttpResponse("You are not authorized to delete another user's post.",
                status=401)
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)

def adminDeleteUser(request, user_id):
    """VIEW 3"""
    """ADMIN view, DELETE request for users"""
    if request.method == "DELETE":
        if request.user.is_authenticated:
            curr_user_permission = permissions.objects.get(user_id=request.user)
            if curr_user_permission.perm_type == "Admin":
                user_obj = User.objects.get(id=post_id)
                user_obj.delete()
                return HttpResponseRedirect("main/adminhome.html")
            else:
                return HttpResponse("You are not authorized to delete another user.",
                status=401)
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)
