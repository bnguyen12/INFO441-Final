from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from django.contrib.auth.models import User
from bs4 import BeautifulSoup

from .models import TreeType, Trees, Cart, InCart, UserPosts, Permissions, UserTrees
from auth.forms import PostForm, ProfileEdit
import json
import hashlib
import requests

@csrf_exempt
def loadoptions(request):
    if request.method == "GET":
            return render(request, "main/index.html")
    else:
            return HttpResponse("Method not allowed on /.", status=405)

@csrf_exempt
def exploreView(request): 
    """VIEW 1"""
    """EXPLORE view, GET request for news feed"""
    if request.method == "GET":
        if request.user.is_authenticated:
            allPosts = []
            posts = UserPosts.objects.all()
            for post in posts:
                description = post.description
                user_obj = post.user_id
                perm_type_obj = Permissions.objects.get(user_id=request.user.id)
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

@csrf_exempt
def exploreDeletePost(request, post_id):
    """VIEW 1"""
    """EXPLORE view, DELETE request to delete only your own posts"""
    if request.method == "GET":
        if request.user.is_authenticated:
            print(request.user.id)
            post_obj = UserPosts.objects.get(id=post_id)
            user = post_obj.user_id
            if user.id == request.user.id:
                UserPosts.objects.filter(id=post_id).delete()
                return HttpResponseRedirect("/main/explore")
            else:
                return HttpResponse("You are not authorized to delete another user's post.",
                status=401)
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)

@csrf_exempt
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
                newPost = UserPosts(user_id=request.user, 
                tree_name=form.cleaned_data["tree_name"], 
                description=form.cleaned_data["description"])
                newPost.save()
                return HttpResponseRedirect("/main/explore")
            else:
                return HttpResponse("Invalid registration request.", status=400)
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)

@csrf_exempt   
def userProfileView(request):
    """VIEW 2"""
    """PROFILE view, GET request to get all of one's details onto a page"""
    if request.method == "GET":
        if request.user.is_authenticated:
            curr_user = User.objects.get(id=request.user.id)
            trees_owned = []
            for tree in UserTrees.objects.all().filter(user_id=curr_user):
                tree_obj = tree.trees_id
                tree_type_obj = tree_obj.tree_type_id
                curr = {
                    "age" : tree_obj.age, "status" : tree_obj.status,
                    "breed" : tree_type_obj.breed, "description" : tree_type_obj.description
                }
                trees_owned.append(curr)
            permission = Permissions.objects.filter(user_id=curr_user).first()
            data = {
                "firstname": curr_user.first_name, "lastname" : curr_user.last_name,
                "email" : curr_user.email, "usertype" : permission.perm_type,
                "treesowned" : trees_owned
            }
            return render(request, "main/profile.html", {"data":data}, status=200)
        else:
            return HttpResponse("User unauthorized.", status=401)
    elif request.method == "DELETE":
        if request.user.is_authenticated:
            curr_user_perm_obj = Permissions.objects.get(user_id=request.user.id)
            
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)

@csrf_exempt
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

@csrf_exempt
def adminView(request):
    """VIEW 3"""
    """ADMIN view, GET request for admins to see all users and posts"""
    if request.user.is_authenticated:
        curr_user_permission = Permissions.objects.filter(user_id=request.user).first()
        if curr_user_permission.perm_type == "Admin":
            if request.method == "GET":
                allUsers = []
                allPosts = []
                for user in User.objects.all():
                    permission = Permissions.objects.filter(user_id=user).first()
                    curr = {
                        "firstname": user.first_name, "lastname" : user.last_name,
                        "email" : user.email, "type" : permission.perm_type, "userid": user.id
                    }
                    allUsers.append(curr)
                for post in UserPosts.objects.all():
                    user = post.user_id
                    permission = Permissions.objects.filter(user_id=user).first()

                    description = post.description
                    user_obj = post.user_id
                    perm_type = permission.perm_type
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

@csrf_exempt
def adminDeletePost(request, post_id):
    """VIEW 3"""
    """ADMIN view, DELETE request for spam posts"""
    if request.method == "GET":
        if request.user.is_authenticated:
            curr_user_permission = Permissions.objects.get(user_id=request.user)
            if curr_user_permission.perm_type == "Admin":
                post_obj = UserPosts.objects.get(id=post_id)
                user = post_obj.user_id
                UserPosts.objects.filter(id=post_id).delete()
                return HttpResponseRedirect("/main/adminview")
            else:
                return HttpResponse("You are not authorized to delete another user's post.",
                status=401)
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)

@csrf_exempt
def adminDeleteUser(request, user_id):
    """VIEW 3"""
    """ADMIN view, DELETE request for users"""
    if request.method == "GET":
        if request.user.is_authenticated:
            curr_user_permission = Permissions.objects.get(user_id=request.user)
            if curr_user_permission.perm_type == "Admin":
                user_obj = User.objects.get(id=user_id)
                user_obj.delete()
                return HttpResponseRedirect("/main/adminview")
            else:
                return HttpResponse("You are not authorized to delete another user.",
                status=401)
        else:
            return HttpResponse("User unauthorized.", status=401)
    else:
        return HttpResponse("Method not allowed.", status=405)

@csrf_exempt
def adopt(request):
    """Shows all trees for homepage"""
    if request.user.is_authenticated is False:
        return HttpResponse('User unauthorized.', status=401)

    if request.method == 'GET':
        trees = []
        for tree in Trees.objects.all():
            trees.append(tree)
        return render(request, 'main/trees.html', {'trees' : trees}, status=200)

@csrf_exempt
def specificTree(request, trees_id):
    """Shows, updates, or deletes a tree from the database"""
    if request.user.is_authenticated is False:
        return HttpResponse('User unauthorized.', status=401)
    
    if request.method == 'GET':
        tree = Trees.objects.get(id=trees_id)
        location = tree.location # TreeAddress.objects.get(trees_id=tree)
        return render(request, 'main/specificTree.html', {'tree' : tree, 'location': location}, status=200)
    elif request.method == 'POST': 
        # add tree to cart
        tree = Trees.objects.get(id=trees_id)
        tree.status = 'PENDING'
        tree.save()
        
        cart = Cart.objects.filter(user_id=request.user).first()
        if not cart: #cart doesn't exist for this user yet
            cart = Cart(user_id=request.user)
            cart.save()
        added_cart_item = InCart(cart_id=cart.id, trees_id=tree)
        added_cart_item.save()
        return HttpResponseRedirect('/adopt')
    elif request.method == 'PATCH':
        tree = Trees.object.get(id=trees_id)
        data = getJSON(request)
        tree.status = data['status']
        tree.age = data['age']
        tree_type = tree.tree_type_id
        tree_type.breed = data['breed']
        tree_type.description = data['description']
        tree.save()
        tree_type.save()

        json_tree = {
            'id': tree.id,
            'tree_type_id': tree_type.id,
            'status': tree.status,
            'age': tree.age,
            'tree_type': {
                'breed': tree_type.breed,
                'description': tree_type.description
            }
        }

        return JsonResponse(json_tree, safe=False, status=201)
    elif request.method == 'DELETE':
        tree = Trees.objects.get(id=trees_id)
        tree.delete()
        return HttpResponse('Tree successfully deleted', status=200)

@csrf_exempt
def cartOperations(request):
    """Shows, updates, or delete whole cart"""
    if request.user.is_authenticated is False:
        return HttpResponse('User unauthorized.', status=401)
    if request.method == 'GET': # Displays all cart items on a webpage
        cart = Cart.objects.filter(user_id=request.user).first()
        all_items = []
        if cart: # if there's an existing cart
            in_cart = InCart.objects.filter(cart_id=cart.id)
            if in_cart: # if there's item in cart
                for item in in_cart:
                    all_items.append(item)
        else: # make a cart for the user if not already made
            Cart(user_id=request.user).save()
        return render(request, 'main/cart.html', { 'all_items' : all_items }, status=200)
    elif request.method == 'DELETE':
        try:
            Cart.objects.filter(user_id=request.user).first().delete
        except Exception:
            return HttpResponse('Database error', status=400)
        return HttpResponse('Cart successfully emptied', status=200)
    elif request.method == 'POST': # Changes all items added to cart sold when checking out
        cart = Cart.objects.filter(user_id=request.user).first()
        in_cart = InCart.objects.filter(cart_id=cart.id)
        for item in in_cart:
            try:
                tree = item.trees_id
                tree.status = 'SOLD'
                tree.save()
                item.delete()

                user_tree = UserTrees(user_id=request.user, trees_id=tree)
                user_tree.save()
            except Exception:
                return HttpResponse('Database error', status=400)
        return HttpResponseRedirect('/cart')
    else:
        return HttpResponse('Method not allowed.', status=405)

@csrf_exempt
def inCartOperations(request, in_cart_id):
    """Shows, updates, or deletes items in cart"""
    if request.user.is_authenticated is False:
        return HttpResponse('User unauthorized.', status=401)
    
    if request.method == 'GET':
        in_cart_item = InCart.objects.get(id=in_cart_id)
        tree_in_cart = in_cart_item.trees_id
        json_cart = {
            'id': in_cart_id,
            'breed': tree_in_cart.tree_type_id.breed,
            'age': tree_in_cart.age
        }
        return JsonResponse(json_cart, safe=False, status=201)
    elif request.method == 'PATCH':
        in_cart_item = InCart.objects.get(id=in_cart_id)
        data = getJSON(request)
        new_tree_id = data['trees_id']
        new_tree = Trees.objects.get(id=new_tree_id)
        in_cart_item.trees_id = new_tree
        in_cart_item.save()

        in_cart_json = {
            'id': in_cart_id,
            'tree': {
                'breed': new_tree.tree_type_id.breed,
                'age': new_tree.age
            }
        }
        return JsonResponse(in_cart_json, safe=False, status=201)
    elif request.method == 'DELETE':
        in_cart_item = InCart.objects.get(id=in_cart_id)
        in_cart_item.delete()
        return HttpResponse('Successfully removed item from cart', status=200)

def getJSON(request):
    """Helper method that gets parsable json"""
    try: # try getting data from POST body
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError: # JSON failed to decode
        return HttpResponse('Failed to decode JSON', status=400)
    except Exception: # any other error
        return HttpResponse('Bad request.', status=405)
    return data

@csrf_exempt
def scrapeData(request):
    """Gets tree data from Wikipedia and puts it in TreeType and Trees"""
    if request.user.is_authenticated is False:
        return HttpResponse('User unauthorized.', status=401)
    
    if request.method == 'GET':
        if not TreeType.objects.filter(breed='Lost Tree').first(): # check if we've scraped before
            page_link = 'https://en.wikipedia.org/wiki/List_of_individual_trees'
            page_response = requests.get(page_link, timeout=10)
            page_content = BeautifulSoup(page_response.content, 'html.parser')
            tree_names = {}
            all_tables = page_content.findChildren('table', attrs={'class':'wikitable'})
            for table in all_tables:
                rows = table.findChildren(['tr'])
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) == 5:
                        name = cells[0].text.strip()
                        description = cells[4].text.strip().split('[')[0] # gets rid of citation at end of string
                        location = cells[2].text

                        try:
                            age = int(cells[3].text)
                        except:
                            age = 5 # if there isn't a default age found
                
                        if len(location) == 0:
                            location = "USA" # default value to USA is valid one isn't found
                        if len(description) == 0:
                            description = "No description available."
                        if len(name) > 0:
                            tree_names[name] = { 'description': description, 'age': age, 'location': location }

            for name in tree_names:
                desc = tree_names[name]['description']
                location = tree_names[name]['location']
                age = tree_names[name]['age']
                try:
                    new_tree_type = TreeType(breed=name, description=desc)
                    new_tree_type.save()
                    new_tree = Trees(
                        tree_type_id=new_tree_type,
                        age=age,
                        location=location,
                        status='AVAILABLE'
                    )
                    print(new_tree)
                    new_tree.save()
                except Exception:
                    return HttpResponse('Database error', status=400)

            return HttpResponseRedirect("/main/adopt")
        else:
            # Goes back to main page
            return HttpResponseRedirect("/main/adopt")
    else:
        return HttpResponse('Method not allowed.', status=405)

@csrf_exempt
def showTreeData(request):
    """Publicly available API endpoint"""
    if request.method == 'GET':
        page_link = 'https://en.wikipedia.org/wiki/List_of_individual_trees'
        page_response = requests.get(page_link, timeout=10)
        page_content = BeautifulSoup(page_response.content, 'html.parser')

        tree_names = {}
        all_tables = page_content.findChildren('table', attrs={'class':'wikitable'})
        for table in all_tables:
            rows = table.findChildren(['tr'])
            for row in rows:
                cells = row.find_all('td')
                if len(cells) == 5:
                    name = cells[0].text.strip()
                    description = cells[4].text.strip().split('[')[0] # gets rid of citation at end of string
                    location = cells[2].text
                    try:
                        age = int(cells[3].text)
                    except:
                        age = 0
                    if len(name) > 0:
                        tree_names[name] = { 'description': description, 'age': age, 'location': location }
        json_trees = []
        for name in tree_names:
            desc = tree_names[name]['description']
            location = tree_names[name]['location']
            age = tree_names[name]['age']
            try:
                json_trees.append({
                    'name': name,
                    'description': desc,
                    'location': location,
                    'age': age
                })
                
            except Exception:
                return HttpResponse('Parsing error', status=400)
        return JsonResponse(json_trees, safe=False, status=201)
    else:
        return HttpResponse('Method not allowed.', status=405)

@csrf_exempt
def displayPlantAPI(request):
    """Displays information on """
    if request.method == 'GET':
        page_link = 'https://plantsdb.xyz/search?limit=1000&fields=Common_Name'
        page_response = requests.get(page_link, timeout=10)
        json_response = json.loads(page_response.content)
        data = json_response['data']
        plant_names = []
        for plant in data:
            if plant['Common_Name'] != '':
                plant_names.append(plant['Common_Name'])
        return render(request, 'main/displayplants.html', {'plant_names': plant_names}, status=200)
    else:
        return HttpResponse('Method not allowed.', status=405)