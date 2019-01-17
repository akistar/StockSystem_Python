import time
from random import randint
STATUS = ['pending', 'failed', 'success']
# rand = randint(10000000000000, 99999999999999)
#the_uuid = ('%sID%s' % (user_id, rand))[:20]


class Order(object):
    _status = None

    def __init__(self, orderid, user_id, amount, price, action, create_time):
        self.id = orderid
        self.userId = user_id
        self.amount = amount
        self.price = price
        self.action = action
        self.createTime = create_time
    #
    # @property
    # def id(self):
    #     return self._id
    #
    # @id.setter
    # def status(self, value):
    #     self._id = value
    #
    # @property
    # def userid(self):
    #     return self._userId
    #
    # @userid.setter
    # def status(self, value):
    #     self._userId = value
    #

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in STATUS:
            raise ValueError('should be a normal status')
        self._status = value


class PendingOrder(Order):
    def __init__(self, orderid, user_id, amount, price, action, create_time):
        Order.__init__(self, orderid, user_id, amount, price, action, create_time)
        self.status = 'pending'


class CompleteOrder(Order):
    def __init__(self, orderid, user_id, amount, price, action, create_time, status, order_ref):
        Order.__init__(self, orderid, user_id, amount, price, action, create_time)
        self.status = status
        self.order_ref = order_ref

