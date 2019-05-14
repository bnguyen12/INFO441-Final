# Methods

Here's the proper input and output for methods that aren't GET requests:

## main/useCart

### POST:
Input:
```
{
    cart_id: 1
}
```

## main/adopt/<int:trees_id>

### PATCH:
Input:
```
{
    status: 'AVAILABLE',
    age: 2,
    tree_type_id: {
        breed: 'maple',
        description: 'this is a tall tree'
    }
}
```

Response:
```
    id: 1,
    tree_type_id: 2
    status: 'AVAILABLE',
    age: 2,
    tree_type: {
        breed: 'maple',
        description: 'this is a tall tree'
    }
```

## main/cart/<int:in_cart_id>

### PATCH:
Input:
```
{
    trees_id: 1
}
```