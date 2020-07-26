import re
def validar(datoAValidar):
    # Admite caracteres alfanumericos y espacios
    patron = re.compile("^[A-Za-z]+(?:[ _-][A-Za-z]+)*$")  
    return patron.match(datoAValidar)