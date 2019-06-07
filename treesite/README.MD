
# Endpoints for main/

## /
* Shows the user options for registering or logging in
* Methods:
    * GET:
        * Shows the user a list of options to login or register for an account
        * Returns 200
    * Else:
        * Returns error 405

## /explore
* This endpoint shows the newsfeed of trees adopted by yourself and others
* Methods:
    * GET:
        * Shows posts from all users about their trees
        * Requires authentication, otherwise returns error 400
        * Returns 200
    * Else:
        * Returns error 405

### /explore/<int:post_id>
* This endpoint deletes a post given the post_id
* Methods:
    * GET:
        * Deletes a user post
        * Requires authentication, otherwise returns error 401
        * Users trying to delete other user posts will return error 401
        * Returns a redirection to the explore page
    * Else:
        * Returns error 405

### /explore/makeapost
* This endpoint lets a user post content to make a post on /explore
* Methods:
    * GET:
        * Shows user a form to type in information
        * Returns 200
    * POST:
        * Posts form data to show post on the explore page
        * Requires authentication, otherwise returns error 401
        * Invalid form input returns error 400
        * Redirects to /explore
    * Else:
        * Returns error 405

## /profile
* Shows details about the user, including name and email
* Methods:
    * GET:
        * Shows user profile, including their name, email, and trees they own
        * Requires authentication, otherwise returns error 401
        * Returns 200
    * Else:
        * Returns error 405

### /profile/edit
* Allows the user to edit their profile
* Methods:
    * GET:
        * Shows a form where user can edit information
        * Returns 200
    * POST:
        * Submits a form to change user information
        * Invalid form input returns error 400
        * Requires authorization, otherwise returns error 401
        * Redirects to profile page
    * Else:
        * Returns error 405

## /adminview
* Shows the "admin" view, where an admin can delete users and user posts
* Methods:
    * GET:
        * Shows a display of users and posts that an admin can delete
        * Requires authentication, otherwise returns error 401
        * Requires admin permission level, otherwise returns error 401
        * Returns 200
    * Else:
        Returns error 405

## /admindeletepost/<int:post_id>
* Deletes a post given post_id
* Methods:
    * GET:
        * Deletes the given post
        * Requires admin level permission, otherwise returns error 401
        * Requires authenticaiton, otherwise returns error 401
        * Redirects to admin view
    * Else:
        * Returns error 405

## /admindeleteuser/<int:user_id>
* Deletes a user given the user_id
* Methods:
    * GET:
        * Deletes the given user
        * Requires admin level permission, otherwise returns error 401
        * Requires authenticaiton, otherwise returns error 401
        * Redirects to admin view
    * Else:
        * Returns error 405

## /adopt
* This endpoint shows the trees readily available to adopt
* Methods:
    * GET:
        * Shows all trees ready to adopt
        * Returns 200
    * Else:
        * Returns error 405

### /adopt/<int:trees_id>
* Shows information, deletes, or updates status of a tree
* Requires user authentication, otherwise returns error 401
* Methods:
    * GET:
        * Shows details on a specific tree
        * Returns 200
    * POST:
        * Adds tree to cart and changes status of tree to "pending"
        * Redirects to the adoption page
    * PATCH:
        * Updates the tree given information in JSON format
        * Format:
        ```
            {
                status: 'SOLD',
                age: 5,
                breed: 'maple',
                description: 'This is a nice tree'
            }
        ```
        * Returns 201
    * DELETE:
        * Deletes the tree from the database
        * Returns 200
    * Else:
        * Returns error 405

## /cart
* Shows info of cart, deletes from cart, and checks out trees in cart
* Requires user authentication, otherwise returns 401
* Methods:
    * GET:
        * Shows all items in the cart
        * Returns 200
    * DELETE:
        * Deletes the whole cart
        * Makes a cart for user if there is not cart, and returns database error 400 if anything happens during this process
        * Returns 200
    * POST:
        * Sets all trees in cart to "SOLD"
        * Returns 400 for any database errors
        * Redirects to cart page
    * Else:
        * Returns error 405

### /cart/items/<int:in_cart_id>
* Shows, updates, or deletes items in cart
* Requires user authentication, otherwise returns 401
* Methods:
    * GET:
        * Returns a JSON response of all items in cart
        * Format:
        ```
        {
            id: 1,
            breed: 'maple',
            age: 5
        }
        ```
    * PATCH:
        * Adds a tree to cart
        * Input format looks like this:
        ```
        {
            trees_id: 5
        }
        ```
        * Returns a JSON response of new cart item like so:
        ```
        {
            id: 5,
            tree: {
                breed: 'maple',
                age: 5
            }
        }
        ```
        * Returns 201
    * DELETE:
        * Deletes the item in cart
        * Returns 400 for any database errors
        * Returns 200

## /scrape
* Loads data of trees webscraped from Wikipedia into our database
* Methods:
    * GET:
        * Loads webscraped trees into database
        * Throws 400 for any database errors
        * Returns 200
    * Else:
        * Returns 405

## /contactus
* Shows a page on contacting us
* Methods:
    * GET:
        * Shows a page on contacting us
        * Returns 200
    * Else:
        * Returns error 405

## /aboutus
* Shows a page about us
* Methods:
    * GET:
        * Shows a page about us
        * Returns 200
    * Else:
        * Returns error 405

## /displayplants
* Displays plants from the USDA API of plants
* Methods:
    * GET:
        * Shows a display of plants from USDA API
        * Throws 400 for any database errors
        * Returns 200
    * Else:
        * Returns 405