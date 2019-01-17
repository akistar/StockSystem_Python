import json
from order import PendingOrder
import uuid
import time
buyOrdersList = []
sellOrdersList = []
pendingBuyOrderList = []
pendingSellOrderList = []
with open('buy_pending_order.json') as data:
    buyOrders = json.load(data)
    for order in buyOrders:
        buyOrdersList.append(
            PendingOrder(order['id'], order['userID'],order['amount'], order['price'], order['action'], order['create'])
        )
        pendingBuyOrderList.append(
            PendingOrder(order['id'], order['userID'], order['amount'], order['price'], order['action'],
                         order['create'])
        )


with open('sell_pending_order.json') as data:
    sellOrders = json.load(data)
    for order in sellOrders:
        sellOrdersList.append(
            PendingOrder(order['id'], order['userID'],order['amount'], order['price'], order['action'], order['create'])
        )
        pendingSellOrderList.append(
            PendingOrder(order['id'], order['userID'], order['amount'], order['price'], order['action'],
                         order['create'])
        )

buyOrdersList.sort(key = lambda x: x.price, reverse=True)
sellOrdersList.sort(key=lambda x: x.price, reverse=False)

price = -1

completeBuyOrdersIds = []
completeSellOrdersIds = []

currentSellInfo = {'id': None, 'amount': 0}
currentBuyInfo = {'id': None, 'amount': 0}
i = 0
while sellOrdersList[0].price - buyOrdersList[0].price <= 0:
    if sellOrdersList[0].amount - buyOrdersList[0].amount == 0:
        completeBuyOrdersIds.append(buyOrdersList[0].id)
        completeSellOrdersIds.append(sellOrdersList[0].id)
        price = (sellOrdersList[0].price + buyOrdersList[0].price) / 2
        currentSellInfo = {'id': None, 'amount': 0}
        currentBuyInfo = {'id': None, 'amount': 0}
        print('e', i, sellOrdersList[0].id,buyOrdersList[0].id)

        del sellOrdersList[0]
        del buyOrdersList[0]
    elif sellOrdersList[0].amount - buyOrdersList[0].amount > 0:
        completeBuyOrdersIds.append(buyOrdersList[0].id)
        sellOrdersList[0].amount = sellOrdersList[0].amount - buyOrdersList[0].amount
        price = (sellOrdersList[0].price + buyOrdersList[0].price) / 2
        currentSellOrderId = sellOrdersList[0].id
        currentSellInfo['id'] = sellOrdersList[0].id,
        currentSellInfo['amount'] = sellOrdersList[0].amount
        currentBuyInfo = {'id': None, 'amount': 0}
        print('s', i, sellOrdersList[0].id,buyOrdersList[0].id)
        del buyOrdersList[0]
    else:
        completeSellOrdersIds.append(sellOrdersList[0].id)
        buyOrdersList[0].amount = buyOrdersList[0].amount - sellOrdersList[0].amount
        price = (sellOrdersList[0].price + buyOrdersList[0].price) / 2
        currentBuyOrderId = buyOrdersList[0].id
        currentBuyInfo['id'] = buyOrdersList[0].id
        currentBuyInfo['amount'] = buyOrdersList[0].amount
        currentSellInfo = {'id': None, 'amount': 0}
        print('b', i, sellOrdersList[0].id,buyOrdersList[0].id)
        del sellOrdersList[0]
    i = i+1

completeBuyOrderList = []
completeSellOrderList = []

for order in pendingBuyOrderList:
    if order.id in completeBuyOrdersIds:
        completeBuyOrderList.append(
            {
                "id": uuid.uuid4().__str__(),
                "userId": order.userId,
                "amount": order.amount,
                "price": price,
                "action": order.action,
                "status": "success",
                "create": time.time(),
                "order_ref": order.id
            }
        )
    elif order.id == currentBuyInfo['id']:
        completeBuyOrderList.append({
            "id": uuid.uuid4().__str__(),
            "userId": order.userId,
            "amount": order.amount - currentBuyInfo['amount'],
            "price": price,
            "action": order.action,
            "status": "success",
            "create": time.time(),
            "order_ref": order.id
        })
        completeBuyOrderList.append({
            "id": uuid.uuid4().__str__(),
            "userId": order.userId,
            "amount": currentBuyInfo['amount'],
            "price": order.price,
            "action": order.action,
            "status": "fail",
            "create": time.time(),
            "order_ref": order.id
        })
    else:
        completeBuyOrderList.append({
            "id": uuid.uuid4().__str__(),
            "userId": order.userId,
            "amount": order.amount,
            "price": order.price,
            "action": order.action,
            "status": "fail",
            "create": time.time(),
            "order_ref": order.id
        })
with open('buy_final_order.json','w') as fp:
    fp.write(json.dumps(completeBuyOrderList))


for order in pendingSellOrderList:
    if order.id in completeSellOrdersIds:
        completeSellOrderList.append(
            {
                "id": uuid.uuid4().__str__(),
                "userId": order.userId,
                "amount": order.amount,
                "price": price,
                "action": order.action,
                "status": "success",
                "create": time.time(),
                "order_ref": order.id
            }
        )
    elif order.id == currentSellInfo['id']:
        completeSellOrderList.append({
            "id": uuid.uuid4().__str__(),
            "userId": order.userId,
            "amount": order.amount - currentBuyInfo['amount'],
            "price": price,
            "action": order.action,
            "status": "success",
            "create": time.time(),
            "order_ref": order.id
        })
        completeSellOrderList.append({
            "id": uuid.uuid4().__str__(),
            "userId": order.userId,
            "amount": currentBuyInfo['amount'],
            "price": order.price,
            "action": order.action,
            "status": "fail",
            "create": time.time(),
            "order_ref": order.id
        })
    else:
        completeSellOrderList.append({
            "id": uuid.uuid4().__str__(),
            "userId": order.userId,
            "amount": order.amount,
            "price": order.price,
            "action": order.action,
            "status": "fail",
            "create": time.time(),
            "order_ref": order.id
        })

with open('sell_final_order.json','w') as fp:
    fp.write(json.dumps(completeSellOrderList))