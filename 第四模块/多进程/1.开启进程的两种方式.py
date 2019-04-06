# coding: utf-8
from multiprocessing import Process
from time import sleep
from random import randint

def hehe_test(name):
    print(name)
    sleep(randint(0,10))
    print(name,"finally")

class Piao(Process):
    def __init__(self,name):
        self.name = name
        super().__init__()

    def run(self):
        print(self.name)
        sleep(randint(0,10))
        print(self.name,"finally")

if __name__ == '__main__':
    # Process(target=hehe_test,args=('hehe',)).start()
    # Process(target=hehe_test,args=('alex',)).start()
    # Process(target=hehe_test,args=('book',)).start()
    # Process(target=hehe_test,args=('wusir',)).start()
    Piao(name='asdasd').start()
    Piao(name='adadsda').start()
    Piao(name ='sdaasd').start()
    Piao(name='adsada').start()
    
import socketserver

