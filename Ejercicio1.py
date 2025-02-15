import threading
import logging
import random
import time
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class Recurso1(Recurso):
    dato1 = 0
    numLectores = 0

recurso1 = Recurso1()

def condicionEscritor():
    return recurso1.numLectores == 0

regionLector = Region(recurso1)
regionEscritor = RegionCondicional(recurso1, condicionEscritor)

@regionLector.region
def seccionCriticaLector():
    regionLector.recurso.numLectores += 1
    logging.info(f'Lector lee dato1 = {regionLector.recurso.dato1}')
    time.sleep(1)
    regionLector.recurso.numLectores -= 1

@regionEscritor.condicion
def seccionCriticaEscritor():
    regionEscritor.recurso.dato1 = random.randint(0,100)
    logging.info(f'Escritor escribe dato1 = {regionEscritor.recurso.dato1}')

def Lector():
    while True:
        seccionCriticaLector()
        time.sleep(random.randint(3,6))

def Escritor():
    while True:
        seccionCriticaEscritor()
        time.sleep(random.randint(1,4))


def main():
    nlector = 10
    nescritor = 2

    for k in range(nescritor):
        threading.Thread(target=Escritor, daemon=True).start()

    for k in range(nlector):
        threading.Thread(target=Lector, daemon=True).start()



    time.sleep(300)


if __name__ == "__main__":
    main()

