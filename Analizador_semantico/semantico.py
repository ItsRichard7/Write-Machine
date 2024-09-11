import ply.yacc as yacc

# Tabla de símbolos para almacenar variables y sus tipos
symbol_table = {}

# Función para agregar variables a la tabla de símbolos
def agregar_variable(nombre, tipo):
    if nombre in symbol_table:
        print(f"Error semántico: la variable '{nombre}' ya fue declarada.")
    else:
        symbol_table[nombre] = tipo

# Función para verificar si una variable existe
def verificar_variable(nombre):
    if nombre not in symbol_table:
        print(f"Error semántico: la variable '{nombre}' no ha sido declarada.")
        return False
    return True

# Función para verificar compatibilidad de tipos en operaciones
def verificar_compatibilidad(tipo1, tipo2, operacion):
    if tipo1 != tipo2:
        print(f"Error semántico: tipos incompatibles en la operación '{operacion}' entre {tipo1} y {tipo2}.")
        return False
    return True


# 1. Definir una variable
def p_def_variable(p):
    '''def_variable : DEF PARIZQ VARIABLE COMA valor PARDER PUNTOCOMA'''
    agregar_variable(p[3], 'number')  # Se asume que la variable es de tipo numérico

# 2. Asignar valor con PUT
def p_put_variable(p):
    '''put_variable : PUT PARIZQ VARIABLE COMA valor PARDER PUNTOCOMA'''
    if verificar_variable(p[3]):
        if not verificar_compatibilidad('number', 'number', 'PUT'):
            print(f"Error semántico en la asignación de la variable {p[3]}.")

# 3. Incremente el valor de la variable con ADD
def p_add_variable_uno(p):
    '''add_variable : ADD PARIZQ VARIABLE PARDER PUNTOCOMA'''
    if verificar_variable(p[3]):
        # Instrucción para incrementar la variable
        pass

def p_add_variable_dos(p):
    '''add_variable : ADD PARIZQ VARIABLE COMA valor PARDER PUNTOCOMA'''
    if verificar_variable(p[3]):
        pass

# 4. Posicionar el lápiz
def p_pos(p):
    '''pos : POS PARIZQ valor COMA valor PARDER PUNTOCOMA'''
    pass

# Definir expresiones básicas (operaciones matemáticas)
def p_expr(p):
    '''expr : valor MULT valor
            | valor DIV valor
            | valor SUM valor
            | valor SUBSTR valor'''
    if verificar_variable(p[1]) and verificar_variable(p[3]):
        if not verificar_compatibilidad('number', 'number', p[2]):
            print(f"Error semántico en la operación '{p[2]}' entre {p[1]} y {p[3]}.")

# Manejo de valores que pueden ser números, variables o expresiones
def p_valor_numero(p):
    '''valor : NUMBER'''
    p[0] = p[1]

def p_valor_variable(p):
    '''valor : VARIABLE'''
    p[0] = p[1]

# Construir el parser
parser = yacc.yacc()
def analizar_semantico(data):
    try:
        parser.parse(data)
        print("Análisis sintáctico completado sin errores")
        print("Tabla de símbolos:", symbol_table)
    except SyntaxError as se:
        print(str(se))


if __name__ == "__main__":
    data = '''
    Def(x, 10);
    Put(x, 5);
    Add(x, 10);
    ContinueUp 5;
    '''
    analizar_semantico(data)
