from datetime import datetime
from functools import total_ordering
import itertools
import pandas as pd

@total_ordering
class Order :
    
    newid = itertools.count()
    
    def __init__(self, quantity, price, buy=True):
        self.__quantity = quantity
        self.__price = price
        self.__buy = buy
        self.__date=datetime.now()
        self.id = next(self.newid)+1 #"+1" to start at 1

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
        temp="--- Insert %s %s | ID : % s| Date : %s | on %s \n" % ("BUY" ,
                                                                    self.__list_buy_orders[n] ,
                                                                    self.__list_buy_orders[n].id,
                                                                    self.__list_buy_orders[n].get_date(),
                                                                    self.__name)#We make the order public
        self.__string+=temp
        self.__list_buy_orders.sort(key= lambda o: (o,o.get_date()), reverse=True)
        temp+=self.execute_order()
        
        print(temp)
        print("Book on %s \n" % (self.__name))
        df1,df2=self.print_book()
        print(df2)
        print("\n")
        print(df1)
        print("\n__________________________")
       
        
        
        
    def insert_sell(self, quantity, price):
        self.__list_sell_orders.append(Order(quantity,price,False))#We had the order to the book
        n=len(self.__list_sell_orders)-1
        temp="--- Insert %s %s | ID : % s| Date : %s | on %s \n" % ("SELL",
                                                                    self.__list_sell_orders[n] ,
                                                                    self.__list_sell_orders[n].id,
                                                                    self.__list_sell_orders[n].get_date(),
                                                                    self.__name)#We make the order public
        self.__string+=temp
        self.__list_sell_orders.sort(key= lambda o: (o,o.get_date()), reverse=False)
        self.__list_sell_orders.reverse()
        temp+=self.execute_order()
        
        print(temp)
        print("Book on %s \n" % (self.__name))
        df1,df2=self.print_book()
        print(df2)
        print("\n")
        print(df1)
        print("\n__________________________")
        
            
    def get_list_buy_orders(self):
        return self.__list_buy_orders
    
    def get_list_sell_orders(self):
        return self.__list_sell_orders
    
    
    def print_book(self):
        temp=""
        temp+="Book on %s \n" % (self.__name)
        for k in self.__list_sell_orders + self.__list_buy_orders:
            temp+="\t %s %s | %s\n" % ("BUY" if k.get_buy() else "SELL", k, k.get_date())
        temp+="------------------------\n\n"
        self.__string+=temp


        list_df1=[]
        list_df2=[]
        for k in self.__list_sell_orders + self.__list_buy_orders:
            if k.get_buy():
                list_df1.append(["BUY",k,k.get_date()])
                
            else :
                list_df2.append(["SELL",k,k.get_date()])
        df1=pd.DataFrame(list_df1,columns=['type','Quantity & Price','Date'])
        df2=pd.DataFrame(list_df2,columns=['type','Quantity & Price','Date'])

        return df1,df2

    
    def execute_order(self):
        temp=""
        while (self.__list_sell_orders and self.__list_buy_orders) and self.__list_sell_orders[-1].get_price()<=self.__list_buy_orders[0].get_price() :
            
            if self.__list_sell_orders[-1].get_quantity()>self.__list_buy_orders[0].get_quantity():
                temp+="Execute %s at %s on %s\n" % (self.__list_buy_orders[0].get_quantity(),
                                                             self.__list_buy_orders[0].get_price(),
                                                             self.__name)
                self.__list_sell_orders[-1].set_quantity(self.__list_sell_orders[-1].get_quantity()-self.__list_buy_orders[0].get_quantity())
                self.__list_buy_orders.pop(0)

            else :
                temp+="Execute %s at %s on %s\n" % (self.__list_sell_orders[-1].get_quantity(),
                                                             self.__list_buy_orders[0].get_price(),
                                                             self.__name)
                self.__list_buy_orders[0].set_quantity(self.__list_buy_orders[0].get_quantity()-self.__list_sell_orders[-1].get_quantity())
                self.__list_sell_orders.pop()
            self.__string+=temp
        return temp

book = Book("TEST")
book.insert_buy(10, 10.0)
book.insert_sell(120, 12.0)
book.insert_buy(5, 10.0)
book.insert_buy(2, 11.0)
book.insert_sell(1, 10.0)
book.insert_sell(10, 10.0)
