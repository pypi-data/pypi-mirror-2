from breve.tags.html import tags as T
from breve.flatten import flatten
from decimal import Decimal
import uuid


DECIMAL_ZERO = Decimal('0.00')


def encodeid(item_id, option_id):
    return '%s.%s'%(item_id, option_id)


def decodeid(id):
    parts = id.split('.', 1)
    item_id = parts[0]
    option_id = parts[1]
    return item_id, option_id


class BasketItem(object):

    quantity = 0

    def __init__(self, item, option, uid):
        self.uid = uid
        self.id = encodeid(item.code, option)
        self.item = item
        self.option = option

        self.categories = getattr(item,'categories',[])
        self.code = item.code

        self.description = item.description(option)
        self.unit_price = item.get_price(option)
        self.unit_postage = item.get_postage(option)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return '<CommerceBasketItem id="%s", code="%s", item="%r", option="%s", description="%s", unit_price="%r">'% \
          (self.id, self.code, self.item, self.option, self.description, self.unit_price)

class Basket:
    """Basic basket implementation.

    The basket keeps track of items and quantities of the items in the
    basket. It also applies any rules when a renderer asks for the
    basket items.
    """

    rules = []

    def __init__(self):
        self._items = []

    def add(self, original, option, quantity=1):
        original_item = BasketItem(original, option, uuid.uuid4().hex)
        if quantity <= 0:
            return

        match = None 
        for item in self._items:
            if original_item == item:
                break
        else:
            item = original_item
            self._items.append(item)
            
        item.quantity += quantity
        
    def get(self, id):
        for item in self._items:
            if item.id == id:
                return item
 
    def remove(self, id):
        for n, item in enumerate(self._items):
            if item.id == id:
                del self._items[n]
                break 

    def empty(self):
        self._items =[]

    def update_quantity(self, id, quantity):
        
        if quantity <= 0:
            self.remove(id)
            return
        
        for item in self._items:
            if item.id == id:
                item.quantity = quantity
                break
            
    def get_items(self, rules=True):
        items = list(self._items)
        if rules:
            return self.apply_rules(items)
        else:
            return items

    @property
    def total_price(self):
        total_price = 0
        for item in self.get_items():
            total_price += (item.unit_price+item.unit_postage) * item.quantity
        return total_price

    @property
    def products_price(self):
        total_price = 0
        for item in self.get_items():
            total_price += item.unit_price * item.quantity
        return total_price
    
    @property
    def postage_price(self):
        total_price = 0
        for item in self.get_items():
            total_price += item.unit_postage * item.quantity
        return total_price

    def apply_rules(self, items):
        for rule in self.rules:
            items = rule(self, items)
        return items

    def __repr__(self):
        return repr(self._items)
        
        

