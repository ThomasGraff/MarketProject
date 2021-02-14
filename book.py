from datetime import datetime
from functools import total_ordering

@total_ordering
class Order :
    
    
    
    def __init__(self, quantity, price, buy=True):
        self.__quantity = quantity
        self.__price = price
        self.__buy = buy
        self.__date=datetime.now()

    def __str__(self): # human-readable content
        return "%s @ %s" % (self.__quantity, self.__price)

    def __repr__(self): # unambiguous representation of the object
        return "Order(%s, %s, %s)" % (self.__quantity, self.__price,
                                                                  self.__buy)

    def __eq__(self, other): # self == other
        return other and self.__quantity == other.__quantity and self.__price == other.__price
                     
    def __lt__(self, other): # self < other
        return other and self.__price < other.__price
    
    def get_quantity(self):
        return self.__quantity
    
    def set_quantity(self, x):
        self.__quantity=x
        
    def get_price(self):
        return self.__price
    
    def get_buy(self):
        return self.__buy
    
    def get_date(self):
        return self.__date
    
    

class Book :
    
   
    
    
    def __init__(self, name, list_buy_orders=[], list_sell_orders=[] ):
        self.__name = name
        self.__list_buy_orders = list_buy_orders
        self.__list_sell_orders = list_sell_orders
        self.__string=""

    def __str__(self): 
        return self.__string
    
    def __repr__(self): 
        return "Book(%s, %s, %s)" % (self.__name, self.__list_buy_orders, 
                                                     self.__list_sell_orders)
    
    def insert_buy(self, quantity, price):
        
        self.__list_buy_orders.append(Order(quantity,price,True))#We had the order to the book
        n=len(self.__list_buy_orders)-1
        self.__string+="--- Insert %s %s | Date : %s | on %s \n" % ("BUY" ,
                                                                    self.__list_buy_orders[n] ,
                                                                    self.__list_buy_orders[n].get_date(),
                                                                    self.__name)#We make the order public
        self.__list_buy_orders.sort(key= lambda o: (o,o.get_date()), reverse=True)
        self.execute_order()
        self.print_book()
        
        
        
        
    def insert_sell(self, quantity, price):
        self.__list_sell_orders.append(Order(quantity,price,False))#We had the order to the book
        n=len(self.__list_sell_orders)-1
        self.__string+="--- Insert %s %s | Date : %s | on %s \n" % ("SELL",
                                                                    self.__list_sell_orders[n] ,
                                                                    self.__list_sell_orders[n].get_date(),
                                                                    self.__name)#We make the order public
        self.__list_sell_orders.sort(key= lambda o: (o,o.get_date()), reverse=False)
        self.__list_sell_orders.reverse()
        self.execute_order()
        self.print_book()
        
            
    def get_list_buy_orders(self):
        return self.__list_buy_orders
    
    def get_list_sell_orders(self):
        return self.__list_sell_orders
    
    
    def print_book(self):
        self.__string+="Book on %s \n" % (self.__name)
        for k in self.__list_sell_orders + self.__list_buy_orders:
            self.__string+="    %s %s | %s\n" % ("BUY" if k.get_buy() else "SELL", k, k.get_date())
        self.__string+="------------------------\n\n"
    
    def execute_order(self):
        while (self.__list_sell_orders and self.__list_buy_orders) and self.__list_sell_orders[-1].get_price()<=self.__list_buy_orders[0].get_price() :

            if self.__list_sell_orders[-1].get_quantity()>self.__list_buy_orders[0].get_quantity():
                self.__string+="Execute %s at %s on %s\n" % (self.__list_buy_orders[0].get_quantity(),
                                                             self.__list_buy_orders[0].get_price(),
                                                             self.__name)
                self.__list_sell_orders[-1].set_quantity(self.__list_sell_orders[-1].get_quantity()-self.__list_buy_orders[0].get_quantity())
                self.__list_buy_orders.pop(0)

            else :
                self.__string+="Execute %s at %s on %s\n" % (self.__list_sell_orders[-1].get_quantity(),
                                                             self.__list_buy_orders[0].get_price(),
                                                             self.__name)
                self.__list_buy_orders[0].set_quantity(self.__list_buy_orders[0].get_quantity()-self.__list_sell_orders[-1].get_quantity())
                self.__list_sell_orders.pop()
