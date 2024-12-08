import random
import string

class GeneraCodigo:
    
    def generar_codigo():
        parte1 = ''.join(random.choices(string.ascii_uppercase, k=2)) 
        parte2 = ''.join(random.choices(string.digits, k=2))            
        parte3 = ''.join(random.choices(string.ascii_uppercase, k=2)) 

        codigo = f"{parte1}-{parte2}-{parte3}"
        return codigo


