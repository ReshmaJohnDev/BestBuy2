# Custom exceptions for specific error scenarios
class InvalidQuantityError(Exception):
    """Raised when the entered quantity is less than or equal to zero."""
    def __init__(self):
        super().__init__("Enter a valid quantity (must be greater than 0)")


class InsufficientStockError(Exception):
    """Raised when the requested quantity is more than available stock."""
    def __init__(self):
        super().__init__("Error while making order! Quantity larger than what exists")


class Product:
    """The Product class represents a specific type of
     product available in the store"""
    def __init__(self, name, price, quantity):
        """Initiator (constructor) method."""
        if not name or price <= 0 or quantity < 0:
            raise ValueError("Enter valid input: name must be non-empty,"
                             " price > 0, and quantity >= 0")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity >= 0
        self.backup_quantity = quantity

    def get_quantity(self):
        """Returns the quantity (int)"""
        return self.quantity

    def set_quantity(self, quantity):
        """Setter function for quantity. If quantity reaches 0, deactivates the product."""
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()
        else :
            self.activate()

    def is_active(self):
        """Returns True if the product is active, otherwise False."""
        return self.active

    def deactivate(self):
        """Deactivates the product."""
        self.active = False

    def activate(self):
        """Activates the product."""
        self.active = True

    def show(self):
        """Returns a string that represents the product"""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity):
        """
        Buys a given quantity of the product.
        Returns the total price of the purchase.
        Updates the quantity of the product.
        """
        if quantity <= 0:
            raise InvalidQuantityError()

        if quantity > self.quantity:
            raise InsufficientStockError()

        total_price = self.price * quantity
        self.quantity -= quantity
        self.set_quantity(self.quantity)
        return total_price

    def rollback_quantity(self):
        """Rolls back the quantity to the backed-up state."""
        self.quantity = self.backup_quantity
        self.set_quantity(self.quantity)
        if self.quantity > 0:  # Reactivate if there is any stock
            self.activate()
        else:  # Deactivate if quantity is 0
            self.deactivate()


prod = Product("MacBook Air M2", price=10, quantity=10)
prod_num_buy = 10
prod.buy(prod_num_buy)