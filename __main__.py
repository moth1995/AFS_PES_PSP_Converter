from AFS import AFS
class Main:
    def __init__(self):
        # Ejemplo de como convertir de afs psp a afs generico
        my_afs = AFS("over.afs",True)
        my_afs.convert_to_dkz()
        my_afs.save_file("new_over.afs")

        # Ejemplo de como convertir de afs generico a afs psp
        #my_afs = AFS("new_over.afs",False)
        #my_afs.convert_to_psp()
        #my_afs.save_file("new_over2.afs")

if __name__ == "__main__":
    Main()