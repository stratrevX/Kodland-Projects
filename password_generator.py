import time, random, os

def root():
    os.system('cls')
    chars = '+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    print("Ciao! Questo e' un generatore di password.")
    try:
        while True:
            lenght = int(input("Inserisci lunghezza:  "))
            quantity = int(input("Inserisci quantita':  "))

            if lenght <= 32:
                pass
            else:
                print("La lunghezza massima e' 32.")
                time.sleep(2)
                root()

            if quantity <= 128:
                break
            else:
                print("quantita' massima e' 128.")
                time.sleep(2)
                root()

        for i in range(quantity):
            password = ''
            for _ in range(lenght):
                password += random.choice(chars)
            print(f'Password N.{i + 1}: {password}')
            time.sleep(0.1)

        time.sleep(15)

    except ValueError:
        print('Per favore inserisci un numero.')
        time.sleep(2)
        root()

    except Exception as e:
        print(f"errore: {e}")
        time.sleep(5)
        root()

root()
