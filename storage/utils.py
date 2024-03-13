from .models import Product, Operation, Action

def get_remaining_product(product: Product) -> int:
    result = 0
    
    operations = Operation.objects.filter(product=product)
    
    for operation in operations:
        if operation.action == Action.SALE:
            result -= operation.quantity
        else:
            result += operation.quantity
    return result