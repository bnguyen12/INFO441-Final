from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import TreeType, Trees, TreeAddress, Cart, InCart
import json

def adopt(request):
    """Shows all trees for homepage"""
    if request.user.is_authenticated is False:
        return HttpResponse('User unauthorized.', status=401)

    if request.method == 'GET':
        trees = []
        for tree in Trees.objects.all():
            trees.append(tree)
        return render(request, 'main/trees.html', {'trees' : trees}, status=200)

def specificTree(request, trees_id):
    """Shows, updates, or deletes a tree from the database"""
    if request.user.is_authenticated is False:
        return HttpResponse('User unauthorized.', status=401)
    
    if request.method == 'GET':
        tree = Trees.objects.get(id=trees_id)
        return render(request, 'main/specificTree.html', {'tree' : tree}, status=200)
    elif request.method == 'PATCH':
        # check if it's the seller
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

def cartOperations(request, cart_id):
    """Shows, updates, or delete whole cart"""
    if request.user.is_authenticated is False:
        return HttpResponse('User unauthorized.', status=401)
    
    if request.method == 'GET': # Displays all cart items on a webpage
        cart_items = InCart.objects.filter(cart_id=cart_id)
        all_items = []
        for item in cart_items:
            all_items.append(item)
        return render(request, 'main/cart.html', { 'all_items' : all_items }, status=200)
    elif request.method == 'DELETE':
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        return HttpResponse('Cart successfully emptied')
    elif request.method == 'POST': # Changes all items added to cart pending
        cart = Cart.objects.get(id=cart_id)
        in_cart_items = InCart.objects.filter(cart_id=cart)
        for item in in_cart_items:
            tree = in_cart_items.trees_id
            tree.status = 'PENDING'
            tree.save()
        return HttpResponse('Successfully  cart', status=200)
    else:
        return HttpResponse('Method not allowed.', status=405)

def inCartOperations(request, in_cart_id):
    """Shows, updates, or deletes items in cart"""
    if request.user.is_authenticated is False:
        return HttpResponse('User unauthorized.', status=401)
    
    if request.method == 'GET':
        in_cart_item = InCart.objects.get(id=in_cart_id)
        tree_in_cart = in_cart_item.trees_id
        json_cart = {
            'id': in_cart_id,
            'breed': tree_in_cart.trees_id.breed,
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
                'breed': tree.tree_type_id.breed,
                'age': tree.age
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