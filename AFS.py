from utils import read_int32

class AFS:

    def __init__(self,file_location=None):
        """
        Inicializamos la clase, variables de la misma, y luego leemos el archivo
        Recibe dos parametros file_location que es un string de la ubicacion del archivo y
        is_psp la cual indica si es un afs de psp
        """
        self.file_location = file_location
        self.data = bytearray()
        self.toc = bytearray()
        self.toc_size = 2048
        self.afs_header_data = bytearray("AFS","utf8") + bytearray(1)
        self.files_indexes = []
        self.files_sizes = []
        self.read_file()

    def read_file(self):
        """
        Lectura del archivo a un bytearray y carga de las variables inicializadas con el contenido del archivo
        """
        afs_file = open(self.file_location, "rb")
        file_contents = bytearray(afs_file.read())
        afs_file.close()
        self.toc_size = read_int32(file_contents[:4]) # The start of first file will indicate the size of TOC
        self.toc = file_contents[:self.toc_size]
        self.data = file_contents[self.toc_size:]
        self.files_indexes = [read_int32(self.toc[i:i+4]) for i in range(0,self.toc_size,8)]
        self.files_sizes = [read_int32(self.toc[i:i+4]) for i in range(4,self.toc_size,8)]

    def save_file(self, file_location=None):
        """
        Guardado del archivo, si se recibe el parametro file_location entonces no se sobreescribe el archivo brindado originalmente,
        si no que se sobre escribe sobre la nueva ubicacion, si es un afs de psp lo guarda como un afs generico
        si no es un afs de psp lo guarda como afs de psp
        """
        file_location = self.file_location = file_location or self.file_location
        
        afs_file = open(file_location,"wb")
        afs_file.write(self.toc)
        afs_file.write(self.data)
        
    def get_number_of_files(self):
        """
        Retorna un numero entero que indica la cantidad de archivos o indices encontrados
        Lee la lista que contiene los indices si encuentra un valor que no es 0 sumariza 1
        """
        return sum(map(lambda x : x != 0, self.files_indexes))

    def convert_to_dkz(self):
        """
        Convierte los indices y tama??os de archivo al formato generico de afs, asi mismo reinicia el TOC y lo carga con los nuevos valores
        """
        self.files_indexes = [index * 2048 for index in self.files_indexes]
        self.files_sizes = [index * 2048 for index in self.files_sizes]
        index_and_sizes = [x for y in zip(self.files_indexes, self.files_sizes) for x in y]
        self.toc = bytearray()
        for i in range(len(index_and_sizes)):
            self.toc+=(index_and_sizes[i].to_bytes(4,"little"))

    def convert_to_psp(self):
        """
        Convierte los indices y tama??os de archivo al formato afs psp, asi mismo reinicia el TOC y lo carga con los nuevos valores
        """
        self.files_indexes = [int(index / 2048) for index in self.files_indexes]
        self.files_sizes = [int(index / 2048) for index in self.files_sizes]
        index_and_sizes = [x for y in zip(self.files_indexes, self.files_sizes) for x in y]
        self.toc = bytearray()
        for i in range(len(index_and_sizes)):
            self.toc+=(index_and_sizes[i].to_bytes(4,"little"))
