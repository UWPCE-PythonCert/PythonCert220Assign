"""
Inventory class
"""
# TODO: this probably shoudn't be a class, and subclasses probably shouldn't be either

class Inventory:
    """
    Inventory Class, specific inventory types subclass this
    """

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_dictionary(self):
        """
        Returns product information as dictionary
        """
        product_dict = {}
        product_dict['product_code'] = self.product_code
        product_dict['description'] = self.description
        product_dict['market_price'] = self.market_price
        product_dict['rental_price'] = self.rental_price

        return product_dict
