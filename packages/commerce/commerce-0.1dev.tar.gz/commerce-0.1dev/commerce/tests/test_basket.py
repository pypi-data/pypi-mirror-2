import unittest
from commerce import basket
from couchish import jsonutil
from decimal import Decimal


class Item():

    def __init__(self, price, label):
        self.unit_price = price
        self.label = label


item_json = """
{"_id":"43b8df0439a44022befbe8514e930395","_rev":"3185942293","available":false,"code":"Foo","description":"really nice","title":"Nice Pho","photo":{"mimetype":"image/jpeg","__type__":"file","filename":"e56482effff644f99be0cb76282fe81b-jc.jpg","file":null,"inline":false,"doc_id":null,"id":"03339887d20246bca4f0366d01e1d9dd"},"show":false,"location":"Scotland","model_type":"photo","ref":"001","categories":["location.uk","location.uk.scotland.arran"],"pricing":[{"price":{"__type__":"decimal","value":"10.02"},"option":"01","label":"default"}],"_attachments":{"03339887d20246bca4f0366d01e1d9dd":{"stub":true,"content_type":"image/jpeg","length":61167}}}
"""
item2_json = """
{"_id":"0059821210844753866d5ff145367ddb","_rev":"988918512","available":true,"size":"205x150","code":"G0123","description":null,"show":true,"photo":{"mimetype":"image/jpeg","metadata":{"width":71,"height":89},"__type__":"file","id":"790268f97d9c48099745748d577a7e6a","filename":"4ff5dce76c4149f09900335138fb00fe-joe-cornish.jpg"},"title":"Cleveland Hills from Cliff Ridge","edition":"","location":"North Yorkshire, England","series":"A5 Landscape","model_type":"photo","ref":"G0123","categories":[],"pricing":[{"price":{"__type__":"decimal","value":"400.00"},"option":"standard","label":"Standard"},{"price":{"__type__":"decimal","value":"800.00"},"option":"special","label":"Special"}],"_attachments":{"790268f97d9c48099745748d577a7e6a":{"stub":true,"content_type":"image/jpeg","length":3329}}}
"""


item = jsonutil.loads(item_json)
item2 = jsonutil.loads(item2_json)
    

class BasketItem(object):

    def __init__(self, original):
        self.id = original['_id']
        self.original = original
        self.categories = original['categories']
        self.code = original['code']
        self.options = original['pricing']

    def description(self, option_id):
        option = [o for o in self.options if o['option'] == option_id][0]
        return '%s, %s'%(self.original['description'],option['label'])

    def get_price(self, option_id):
        option = [o for o in self.options if o['option'] == option_id][0]
        return option['price']

    def __repr__(self):
        return '<CouchishBasketItem id="%s", code="%s", options="%r">'%(self.id, self.code, self.options)




class TestBasket(unittest.TestCase):

    def test_addingitem(self):
        b = basket.Basket()
        b.add(BasketItem(item),'01',1)
        assert len(b._items) == 1
        assert b._items[0].id == 'Foo.01'
        assert b._items[0].item.id == "43b8df0439a44022befbe8514e930395"
       
    def test_addingitems(self):
        b = basket.Basket()
        b.add(BasketItem(item),'01',1)
        b.add(BasketItem(item2),'standard',1)
        assert len(b._items) == 2
        assert b._items[0].id == 'Foo.01'
        assert b._items[0].item.id == "43b8df0439a44022befbe8514e930395"
        assert b._items[1].id == 'G0123.standard'
        assert b._items[1].item.id == "0059821210844753866d5ff145367ddb"
        assert b.get_total_price() == Decimal('410.02')
       
    def test_addingoptions(self):
        b = basket.Basket()
        b.add(BasketItem(item2),'special',1)
        b.add(BasketItem(item2),'standard',1)
        assert len(b._items) == 2
        assert b._items[0].id == 'G0123.special'
        assert b._items[0].item.id == "0059821210844753866d5ff145367ddb"
        assert b._items[1].id == 'G0123.standard'
        assert b._items[1].item.id == "0059821210844753866d5ff145367ddb"
        assert b.get_total_price() == Decimal('1200.00')
        items = b.get_items()
        assert items == b._items

    def test_addmultiples(self):
        b = basket.Basket()
        b.add(BasketItem(item2),'special',1)
        b.add(BasketItem(item2),'special',1)
        assert len(b._items) == 1
        assert b._items[0].id == 'G0123.special'
        assert b._items[0].quantity == 2

    def test_remove(self):
        b = basket.Basket()
        b.add(BasketItem(item2),'special',1)
        b.add(BasketItem(item2),'special',1)
        b.remove('G0123.special')
        assert len(b._items) == 0
        b = basket.Basket()
        b.add(BasketItem(item2),'special',1)
        b.add(BasketItem(item2),'standard',1)
        b.remove('G0123.standard')
        assert len(b._items) == 1
        assert b._items[0].id == 'G0123.special'
        assert b._items[0].item.id == "0059821210844753866d5ff145367ddb"
        
    def test_update_quantity(self):
        b = basket.Basket()
        b.add(BasketItem(item2),'special',1)
        b.add(BasketItem(item2),'special',1)
        b.update_quantity('G0123.special',4)
        assert b._items[0].quantity == 4
       
    def test_update_quantity_to_zero(self):
        b = basket.Basket()
        b.add(BasketItem(item2),'special',1)
        b.add(BasketItem(item2),'special',1)
        assert len(b._items) == 1
        b.update_quantity('G0123.special',0)
        assert len(b._items) == 0

    def test_empty(self):
        b = basket.Basket()
        b.add(BasketItem(item2),'special',1)
        b.add(BasketItem(item2),'special',1)
        assert len(b._items) == 1
        b.empty()
        assert len(b._items) == 0

    def test_get_item(self):
        b = basket.Basket()
        b.add(BasketItem(item2),'special',1)
        b.add(BasketItem(item2),'standard',1)
        item = b.get('G0123.special')
        assert item.code == 'G0123'

