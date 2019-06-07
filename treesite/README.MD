
# Endpoints
## /explore
* This endpoint shows the newsfeed of trees adopted by yourself and others. It will display the picture of the tree, the name (breed, type, etc.), the date adopted, and an option to look at a more detailed view of the tree
* This will use a GET request
* The user needs to be authenticated in order to see their own adopted trees as well as others
* The user is given a 200 code response for GET requests. All other methods give error 405 (not allowed on this endpoint)

## /adopt
* This endpoint shows the trees readily available to adopt
* This will use a GET request
* The user needs to be authenticated to view trees ready for adoption
* The user is given a 200 code response for GET requests. All other methods give error 405 (not allowed on this endpoint)

## /checkout
* This endpoint takes the user to a checkout page with trees in their cart
* This will use a POST request in order to send information on what trees are in the cart and who the cart belongs to (whoever is logged in)
* The user needs to be authenticated to checkout a tree
* The user will be returned a response that their purchase has gone through, and then be taken back to their newsfeed

## /profile
* This endpoint takes the user to their profile page
* This will use a GET request
* The user needs to be authenticated to view their profile page. This is a given since the user needs to be logged in anyway to view their personal information
* The user will be returned a 200 code response for GET requests. All other methods give error 405 (not allowed on this endpoint)
* This endpoint shows the status of the trees the user has adopted. For instance, trees could be marked as planted, growing, withering, etc.
* The user needs to be authenticated to see the status of their trees
* The user will be returned a 200 code response for GET requests. All other methods give error 405 (not allowed on this endpoint)

## /cart
* This endpoint shows the items users have in cart
* This point requires user authentication
* This endpoint takes in a GET request