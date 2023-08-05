import cgi
from nevow import inevow, util as n_util
from pollen.commerce import basket


class BasketResourceHelper(object):

    def __init__(self, basket, basketURL, checkoutURL, itemFromId=None):
        super(BasketResourceHelper, self).__init__()
        self.basket = basket
        self.basketURL = basketURL
        self.checkoutURL = checkoutURL
        self.itemFromId = itemFromId

    def renderHTTP(self, ctx):
        request = inevow.IRequest(ctx)
        if request.method == 'POST':
            return self.handlePOST(ctx, request.args)
        return super(BasketResource, self).renderHTTP(ctx)

    def handlePOST(self, ctx, args):
        args = dict(args)
        command = args.pop('command')[0]
        command = command.lower()
        func = getattr(self, 'command_%s'%command)
        return func(ctx, args)

    def render_basket(self, ctx, data):
        return basket.IBasketRenderer(self.basket).rend(ctx, data)

    def command_add(self, ctx, args):
        """
        Add a product to the basket.

        Args contains:
            id -- the ID of the product to add.
            quantity -- optional number of the product to add, default to 1
        """

        if "_id" not in args:
            print "Switching to command_add_old"
            return self.command_add_old(ctx, args)

        encoding = n_util.getPOSTCharset(ctx)

        # Decode the args
        productID = args['_id'][0].decode(encoding)
        quantity = int(args.get('_quantity', [1])[0])
        option = args.get("_option", [None])[0]
        if option is not None:
            option = dict((k,v[0]) for (k,v) in cgi.parse_qs(option).iteritems())
        else:
            option = dict((k,v[0]) for (k,v) in args.iteritems() if k[0] != "_")

        def checkResult(item, id, option):
            if item is None:
                raise Exception("Item %r, %r not found" % (id, option))
            return item

        def success(item):
            self.basket.addItem(item, quantity)
            return self.basketURL

        d = self.basketItemFactory(ctx, productID, option)
        d.addCallback(checkResult, productID, option)
        d.addCallback(success)
        return d

    def command_add_old(self, ctx, args):
        # Decode the args
        productID = args['id'][0].decode(n_util.getPOSTCharset(ctx))
        quantity = args.get('quantity', [1])[0]
        # Lookup the product
        def gotProduct(product):
            if product is not None:
                self.basket.addItem(product, quantity)
            return self.basketURL
        d = self.itemFromId(productID)
        d.addCallback(gotProduct)
        return d

    def command_update(self, ctx, args):
        def parse(args):
            removals = []
            updates = []
            for id in args.get('remove', []):
                try:
                    removals.append(int(id))
                except ValueError:
                    continue
            for name, values in args.items():
                if not name.startswith('item_'):
                    continue
                id = name[5:]
                quantity = values[0].strip() or 0
                try:
                    id = int(id)
                    quantity = int(quantity)
                except ValueError:
                    continue
                if id not in removals:
                    updates.append((id, quantity))
            return removals, updates
        # Parse the request
        removals, updates = parse(args)
        # Process removals.
        for removal in removals:
            self.basket.removeItem(removal)
        # Process updates.
        for id, quantity in updates:
            self.basket.updateItemQuantity(id, quantity)
        # Start checkout
        if 'checkout' in args or 'checkout.x' in args:
            return self.checkoutURL
        return self.basketURL

