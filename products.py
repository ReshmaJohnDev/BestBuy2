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
    def __init__(self, name, price, quantity, promotion = None):
        """Initiator (constructor) method."""
        if not name or price <= 0 or quantity < 0:
            raise ValueError("Enter valid input: name must be non-empty,"
                             " price > 0, and quantity >= 0")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.promotion = promotion
        self.active = quantity >= 0
        self.backup_quantity = quantity

    @property #getter for quantity
    def quantity(self):
        """Returns the quantity (int)"""
        return self._quantity

    @quantity.setter #setter for quantity
    def quantity(self, quantity):
        """Setter function for quantity. If quantity reaches 0, deactivates the product."""
        self._quantity = quantity
        if self._quantity == 0:
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
        promotion_info = f", Promotion: {self.promotion.name}" if self.promotion else None
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, Promotion: {promotion_info}"

    def buy(self, quantity):
        """
        Buys a given quantity of the product.
        Returns the total price of the purchase.
        Updates the quantity of the product.
        """
        if quantity <= 0:
            raise InvalidQuantityError()

        elif quantity > self.quantity:
            raise InsufficientStockError()

        total_price = (self.promotion.apply_promotion(self, quantity) if self.promotion else self.price * quantity)
        self.quantity -= quantity
        return total_price

    @property #getter for promotion
    def promotion(self):
        return self._promotion

    @promotion.setter
    def promotion(self,promotion):
        self._promotion = promotion

    def rollback_quantity(self):
        """Rolls back the quantity to the backed-up state."""
        self.quantity = self.backup_quantity
        # self.set_quantity(self.quantity)
        if self.quantity > 0:  # Reactivate if there is any stock
            self.activate()
        else:  # Deactivate if quantity is 0
            self.deactivate()


class NonStockedProduct(Product):
    def __init__(self, name, price):
        super().__init__(name, price, 0)

    def show(self):
        """Overrides the show method to display 'Unlimited' for quantity."""
        promotion_info = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: ${self.price}, Quantity: Unlimited, Promotion: {promotion_info}"

    @property
    def quantity(self):
        """Overrides get_quantity to always return 0."""
        return 0

    @quantity.setter
    def quantity(self, quantity):
        """Setter function for quantity. If quantity reaches 0, deactivates the product."""
        self.activate()

    def is_active(self):
        """Overrides is_active to always return True."""
        return True

    def buy(self, quantity):
        """
        Overrides buy method of parent class to update the quantity to 0
        """
        if quantity <= 0:
            raise InvalidQuantityError()

        total_price = (self.promotion.apply_promotion(self, quantity) if self.promotion else self.price * quantity)
        self._quantity = 0
        return total_price


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum):
        self.maximum = maximum
        super().__init__(name, price, quantity)

    def show(self):
        """Overrides the show method to display 'Unlimited' for quantity."""
        promotion_info = f", Promotion: {self.promotion.name}" if self.promotion else None
        return (f"{self.name}, Price: ${self.price},"
                f" Limited to {self.maximum} per order!,"
                f" Promotion: {promotion_info}")

    def buy(self, quantity):
        """Overrides the buy method to update the quantity
        when quantity is greater than maximum"""
        if quantity <= 0:
            raise InvalidQuantityError()
        elif quantity > self.maximum:
            raise ValueError(f"Only {self.maximum} is allowed from this prod")
        total_price = (self.promotion.apply_promotion(self, quantity) if self.promotion else self.price * quantity)
        self.quantity -= quantity
        return total_price

