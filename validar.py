from re import compile

def validarTitulo(datoAValidar):
        patron = compile("^[A-Za-z]+(?:[ _-][A-Za-z]+)*$")  
        return patron.match(datoAValidar)

if __name__ == '__main__':
    titulo = input('Ingrese un titulo: ')
    while titulo != '-1':
        print(validarTitulo(titulo))
        titulo = input('Ingrese un titulo: ')
        