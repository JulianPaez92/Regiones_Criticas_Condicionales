import threading
import logging
import random
import time
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class Recurso1(Recurso):
    dato1 = 0
    numEscritores = 0

recurso1 = Recurso1()

def condicionLector():
    return recurso1.numEscritores == 0

regionLector = RegionCondicional(recurso1, condicionLector)
regionEscritor = Region(recurso1)

@regionLector.condicion
def seccionCriticaLector():
    logging.info(f'Lector lee dato1 = {regionLector.recurso.dato1}')

@regionEscritor.region
def seccionCriticaEscritor():
    regionEscritor.recurso.numEscritores += 1
    regionEscritor.recurso.dato1 = random.randint(0,100)
    logging.info(f'Escritor escribe dato1 = {regionEscritor.recurso.dato1}')
    time.sleep(1)
    regionEscritor.recurso.numEscritores -= 1


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

    for k in range(nlector):
        threading.Thread(target=Lector, daemon=True).start()

    for k in range(nescritor):
        threading.Thread(target=Escritor, daemon=True).start()

    time.sleep(300)


if __name__ == "__main__":
    main()

