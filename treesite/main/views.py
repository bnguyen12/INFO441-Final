from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

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
    """Shows, adds, or deletes a tree from the database"""
    if request.user.is_authenticated is False:
        return HttpResponse('User unauthorized.', status=401)
    
    if request.method == 'GET':
        tree = Trees.objects.filter(id=trees_id)
        location = TreeAddress.objects.filter(trees_id=tree)
        return render(request, 'main/specificTree.html', 
            {'tree' : tree, 'location' : location}, status=200)
    # elif request.method == 'POST':

    elif request.method == 'DELETE':
        tree = Trees.objects.get(id=trees_id)
        tree.delete()
        return HttpResponse('Tree successfully deleted', status=200)
    else:
        return HttpResponse('Method not allowed.', status=405)

def useCart(request, cart_id):
    """Shows, updates, or deletes from cart"""
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
        return HttpResponse('Successfully added to cart', status=200)
    else:
        return HttpResponse('Method not allowed.', status=405)

def userTrees(request, user_id):
    """Shows, updates, or deletes user's trees"""
    if request.user.is_authenticated is False:
        return HttpResponse('User unauthorized.', status=401)
    ### TODO

def getJSON(request):
    """Helper method that gets parsable json"""
    try: # try getting data from POST body
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError: # JSON failed to decode
        return HttpResponse('Failed to decode JSON', status=400)
    except Exception: # any other error
        return HttpResponse('Bad request.', status=405)
    return data