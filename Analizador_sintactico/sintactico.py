import sys
sys.path.append('./Analizador_lexico')  # Ajustar según la estructura de carpetas
from lexico import tokens  # Importamos los tokens definidos
import ply.yacc as yacc

# 1. Definir la estructura más general

# Definir sentencias múltiples
def p_sentencias(p):
    '''sentencias : sentencia sentencias
                  | sentencia'''
    pass

# Definir una sentencia que puede ser cualquier instrucción válida
def p_sentencia(p):
    '''sentencia : def_variable
                 | put_variable
                 | add_variable
                 | continue_up
                 | continue_down
                 | continue_right
                 | continue_left
                 | pos
                 | posx
                 | posy
                 | use_color
                 | down
                 | up
                 | beginning
                 | for_loop
                 | case
                 | repeat_until
                 | while
                 | equal
                 | and
                 | or
                 | greater
                 | smaller
                 | substr
                 | random
                 | mult
                 | div
                 | sum'''
    pass

# 2. Reglas más específicas

# 2.1. Definir una variable
def p_def_variable(p):
    '''def_variable : DEF PARIZQ VARIABLE COMA valor PARDER PUNTOCOMA'''
    pass

# 2.2. Asignar valor con PUT
def p_put_variable(p):
    '''put_variable : PUT PARIZQ VARIABLE COMA valor PARDER PUNTOCOMA'''
    pass

# 2.3. Incremente el valor de la variable con ADD
def p_add_variable_uno(p):
    '''add_variable : ADD PARIZQ VARIABLE PARDER PUNTOCOMA'''
    pass

def p_add_variable_dos(p):
    '''add_variable : ADD PARIZQ VARIABLE COMA valor PARDER PUNTOCOMA'''
    pass

# 2.4. Movimientos: ContinueUp, ContinueDown, ContinueRight, ContinueLeft
def p_continue_up(p):
    '''continue_up : CONUP valor PUNTOCOMA'''
    pass

def p_continue_down(p):
    '''continue_down : CONDOWN valor PUNTOCOMA'''
    pass

def p_continue_right(p):
    '''continue_right : CONRIGHT valor PUNTOCOMA'''
    pass

def p_continue_left(p):
    '''continue_left : CONLEFT valor PUNTOCOMA'''
    pass

# 2.5. Posicionar el lápiz: Pos, PosX, PosY
def p_pos(p):
    '''pos : POS PARIZQ valor COMA valor PARDER PUNTOCOMA'''
    pass

def p_posx(p):
    '''posx : POSX valor PUNTOCOMA'''
    pass

def p_posy(p):
    '''posy : POSY valor PUNTOCOMA'''
    pass

# 2.6. Cambiar el color con UseColor
def p_use_color(p):
    '''use_color : USECOLOR valor PUNTOCOMA'''
    pass

# 2.7. Subir o bajar el lápiz
def p_down(p):
    '''down : DOWN PUNTOCOMA'''
    pass

def p_up(p):
    '''up : UP PUNTOCOMA'''
    pass

# 2.8. Volver al inicio
def p_beginning(p):
    '''beginning : BEGIN PUNTOCOMA'''
    pass

# 2.9. Sentencia FOR-LOOP
def p_for_loop(p):
    '''for_loop : FOR VARIABLE PARIZQ valor TO valor PARDER LOOP BRAIZQ sentencias BRADER END LOOP PUNTOCOMA'''
    pass

# 2.10. Sentencia CASE-WHEN
def p_case(p):
    '''case : CASE VARIABLE when_cases end_case'''
    pass

def p_when_cases(p):
    '''when_cases : when_cases when_case
                  | when_case'''
    pass

def p_when_case(p):
    '''when_case : WHEN valor THEN BRAIZQ sentencias BRADER'''
    pass

def p_end_case(p):
    '''end_case : ELSE BRAIZQ sentencias BRADER END CASE PUNTOCOMA
                | END CASE PUNTOCOMA'''
    pass

# 2.11. Sentencia REPEAT-UNTIL
def p_repeat_until(p):
    '''repeat_until : REPEAT BRAIZQ sentencias BRADER UNTIL PARIZQ condicion PARDER PUNTOCOMA'''
    pass

# 2.12. Sentencia WHILE-WHEND
def p_while(p):
    '''while : WHILE PARIZQ condicion PARDER BRAIZQ sentencias BRADER WHEND PUNTOCOMA'''
    pass

# 2.13. Funciones: Equal, And, Or, Greater, Smaller
def p_equal(p):
    '''equal : EQUAL PARIZQ valor COMA valor PARDER'''
    pass

def p_and(p):
    '''and : AND PARIZQ valor COMA valor PARDER'''
    pass

def p_or(p):
    '''or : OR PARIZQ valor COMA valor PARDER'''
    pass

def p_greater(p):
    '''greater : GREATER PARIZQ valor COMA valor PARDER'''
    pass

def p_smaller(p):
    '''smaller : SMALLER PARIZQ valor COMA valor PARDER'''
    pass

# 2.14. Operaciones: Substr, Random, Mult, Div, Sum
def p_substr(p):
    '''substr : SUBSTR PARIZQ valor COMA valor PARDER'''
    pass

def p_random(p):
    '''random : RANDOM PARIZQ valor PARDER'''
    pass

def p_mult(p):
    '''mult : MULT PARIZQ valor COMA valor PARDER'''
    pass

def p_div(p):
    '''div : DIV PARIZQ valor COMA valor PARDER'''
    pass

def p_sum(p):
    '''sum : SUM PARIZQ valor COMA valor PARDER'''
    pass

# Manejo de valores que pueden ser números, variables o expresiones
def p_valor_numero(p):
    '''valor : NUMBER'''
    p[0] = p[1]

def p_valor_variable(p):
    '''valor : VARIABLE'''
    p[0] = p[1]

def p_valor_expr(p):
    '''valor : expr'''
    p[0] = p[1]

def p_valor_logico(p):
    '''valor : TRUE
             | FALSE'''
    p[0] = p[1]

# Definir expresiones básicas (operaciones matemáticas)
def p_expr(p):
    '''expr : valor MULT valor
            | valor DIV valor
            | valor SUM valor
            | valor SUBSTR valor'''
    p[0] = p[1]

# Condiciones para bucles y otras sentencias
def p_condicion(p):
    '''condicion : equal
                 | greater
                 | smaller
                 | and
                 | or'''
    pass

# Manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"Error sintáctico en línea {p.lineno}: token inesperado '{p.value}'")
    else:
        print("Error sintáctico: fin de archivo inesperado")

# Construir el parser
parser = yacc.yacc()

# Función para analizar sintácticamente el código fuente
def analizar_sintactico(data):
    try:
        parser.parse(data)
        print("Análisis completado sin errores")
    except SyntaxError as se:
        print(str(se))

# Ejemplo de prueba
if __name__ == "__main__":
    data = '''// Ejemplo de código fuente
    Def(variable1, 5);
    Add(variable1, 10);
    ContinueUp 10;
    '''
    analizar_sintactico(data)


