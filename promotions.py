from abc import ABC, abstractmethod


class Promotion(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        pass


class SecondHalfPrice(Promotion):
    def apply_promotion(self, product, quantity):
        """Applying promotion for Second item at half price”"""
        full_price_items = (quantity + 1) // 2
        half_price_items = quantity // 2
        return (full_price_items * product.price) + (half_price_items * product.price * 0.5)


class ThirdOneFree(Promotion):
    def apply_promotion(self, product, quantity):
        """Apply the third one free promotion."""
        price = product.price
        paid_items = quantity - (quantity // 3)  # For every 3 items, 1 is free
        return paid_items * price


class PercentDiscount(Promotion):
    def __init__(self, name, percent):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity):
        """Discount applied"""
        price = product.price
        total_price = price * quantity
        discount_price  = total_price -  (total_price * (self.percent/100))
        return discount_price
