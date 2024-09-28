from lexico import tokens, errores  # Importamos los tokens definidos
import ply.yacc as yacc
import pydot

# 1. Definir la estructura más general

# Definir sentencias múltiples
def p_sentencias(p):
    '''sentencias : sentencia sentencias
                  | sentencia'''
    if len(p) == 3:
        p[0] = ('sentencias', p[1], p[2])
    else:
        p[0] = ('sentencias', p[1])

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
    p[0] = ('sentencia', p[1])

# 2. Reglas más específicas

# 2.1. Definir una variable
def p_def_variable(p):
    '''def_variable : DEF PARIZQ VARIABLE COMA valor PARDER PUNTOCOMA'''
    p[0] = ('def_variable', p[3], p[5])

# 2.2. Asignar valor con PUT
def p_put_variable(p):
    '''put_variable : PUT PARIZQ VARIABLE COMA valor PARDER PUNTOCOMA'''
    p[0] = ('put_variable', p[3], p[5])

# 2.3. Incremente el valor de la variable con ADD
def p_add_variable_uno(p):
    '''add_variable : ADD PARIZQ VARIABLE PARDER PUNTOCOMA'''
    p[0] = ('add_variable_uno', p[3])

def p_add_variable_dos(p):
    '''add_variable : ADD PARIZQ VARIABLE COMA valor PARDER PUNTOCOMA'''
    p[0] = ('add_variable_dos', p[3], p[5])

# 2.4. Movimientos: ContinueUp, ContinueDown, ContinueRight, ContinueLeft
def p_continue_up(p):
    '''continue_up : CONUP valor PUNTOCOMA'''
    p[0] = ('continue_up', p[2])

def p_continue_down(p):
    '''continue_down : CONDOWN valor PUNTOCOMA'''
    p[0] = ('continue_down', p[2])

def p_continue_right(p):
    '''continue_right : CONRIGHT valor PUNTOCOMA'''
    p[0] = ('continue_right', p[2])

def p_continue_left(p):
    '''continue_left : CONLEFT valor PUNTOCOMA'''
    p[0] = ('continue_left', p[2])

# 2.5. Posicionar el lápiz: Pos, PosX, PosY
def p_pos(p):
    '''pos : POS PARIZQ valor COMA valor PARDER PUNTOCOMA'''
    p[0] = ('pos', p[3], p[5])

def p_posx(p):
    '''posx : POSX valor PUNTOCOMA'''
    p[0] = ('posx', p[2])

def p_posy(p):
    '''posy : POSY valor PUNTOCOMA'''
    p[0] = ('posy', p[2])

# 2.6. Cambiar el color con UseColor
def p_use_color(p):
    '''use_color : USECOLOR valor PUNTOCOMA'''
    p[0] = ('use_color', p[2])

# 2.7. Subir o bajar el lápiz
def p_down(p):
    '''down : DOWN PUNTOCOMA'''
    p[0] = ('down',)

def p_up(p):
    '''up : UP PUNTOCOMA'''
    p[0] = ('up',)

# 2.8. Volver al inicio
def p_beginning(p):
    '''beginning : BEGIN PUNTOCOMA'''
    p[0] = ('beginning',)

# 2.9. Sentencia FOR-LOOP
def p_for_loop(p):
    '''for_loop : FOR VARIABLE PARIZQ valor TO valor PARDER LOOP BRAIZQ sentencias BRADER END LOOP PUNTOCOMA'''
    p[0] = ('for_loop', p[2], p[4], p[6], p[9])

# 2.10. Sentencia CASE-WHEN
def p_case(p):
    '''case : CASE VARIABLE when_cases end_case'''
    p[0] = ('case', p[2], p[3], p[4])

def p_when_cases(p):
    '''when_cases : when_cases when_case
                  | when_case'''
    if len(p) == 3:
        p[0] = ('when_cases', p[1], p[2])
    else:
        p[0] = ('when_cases', p[1])

def p_when_case(p):
    '''when_case : WHEN valor THEN BRAIZQ sentencias BRADER'''
    p[0] = ('when_case', p[2], p[5])

def p_end_case(p):
    '''end_case : ELSE BRAIZQ sentencias BRADER END CASE PUNTOCOMA
                | END CASE PUNTOCOMA'''
    if len(p) == 8:
        p[0] = ('end_case', p[3])
    else:
        p[0] = ('end_case',)

# 2.11. Sentencia REPEAT-UNTIL
def p_repeat_until(p):
    '''repeat_until : REPEAT BRAIZQ sentencias BRADER UNTIL PARIZQ condicion PARDER PUNTOCOMA'''
    p[0] = ('repeat_until', p[3], p[7])

# 2.12. Sentencia WHILE-WHEND
def p_while(p):
    '''while : WHILE PARIZQ condicion PARDER BRAIZQ sentencias BRADER WHEND PUNTOCOMA'''
    p[0] = ('while', p[3], p[6])

# 2.13. Funciones: Equal, And, Or, Greater, Smaller
def p_equal(p):
    '''equal : EQUAL PARIZQ valor COMA valor PARDER'''
    p[0] = ('equal', p[3], p[5])

def p_and(p):
    '''and : AND PARIZQ valor COMA valor PARDER'''
    p[0] = ('and', p[3], p[5])

def p_or(p):
    '''or : OR PARIZQ valor COMA valor PARDER'''
    p[0] = ('or', p[3], p[5])

def p_greater(p):
    '''greater : GREATER PARIZQ valor COMA valor PARDER'''
    p[0] = ('greater', p[3], p[5])

def p_smaller(p):
    '''smaller : SMALLER PARIZQ valor COMA valor PARDER'''
    p[0] = ('smaller', p[3], p[5])

# 2.14. Operaciones: Substr, Random, Mult, Div, Sum
def p_substr(p):
    '''substr : SUBSTR PARIZQ valor COMA valor PARDER'''
    p[0] = ('substr', p[3], p[5])

def p_random(p):
    '''random : RANDOM PARIZQ valor PARDER'''
    p[0] = ('random', p[3])

def p_mult(p):
    '''mult : MULT PARIZQ valor COMA valor PARDER'''
    p[0] = ('mult', p[3], p[5])

def p_div(p):
    '''div : DIV PARIZQ valor COMA valor PARDER'''
    p[0] = ('div', p[3], p[5])

def p_sum(p):
    '''sum : SUM PARIZQ valor COMA valor PARDER'''
    p[0] = ('sum', p[3], p[5])

# Manejo de valores que pueden ser números, variables o expresiones
def p_valor_numero(p):
    '''valor : NUMBER'''
    p[0] = ('number', p[1])

def p_valor_variable(p):
    '''valor : VARIABLE'''
    p[0] = ('variable', p[1])

def p_valor_expr(p):
    '''valor : expr'''
    p[0] = p[1]

def p_valor_logico(p):
    '''valor : TRUE
             | FALSE'''
    p[0] = ('logico', p[1])

# Definir expresiones básicas (operaciones matemáticas)
def p_expr(p):
    '''expr : valor MULT valor
            | valor DIV valor
            | valor SUM valor
            | valor SUBSTR valor'''
    p[0] = (p[2], p[1], p[3])

# Condiciones para bucles y otras sentencias
def p_condicion(p):
    '''condicion : equal
                 | greater
                 | smaller
                 | and
                 | or'''
    p[0] = p[1]

# Manejo de errores sintácticos
def p_error(p):
    if p:
        error = f"Error sintáctico en línea {p.lineno-1}: token inesperado '{p.value}'"
    else:
        error = "Error sintáctico: fin de archivo inesperado"
    errores.append(error)

# Construir el parser
parser = yacc.yacc()

# Función para crear el árbol de parseo
def crear_nodo_arbol(nodo, grafo, padre=None):
    if isinstance(nodo, tuple):
        nodo_actual = pydot.Node(str(id(nodo)), label=nodo[0])
        grafo.add_node(nodo_actual)
        if padre:
            grafo.add_edge(pydot.Edge(padre, nodo_actual))
        for subnodo in nodo[1:]:
            crear_nodo_arbol(subnodo, grafo, nodo_actual)
    else:
        nodo_hoja = pydot.Node(str(id(nodo)), label=str(nodo))
        grafo.add_node(nodo_hoja)
        if padre:
            grafo.add_edge(pydot.Edge(padre, nodo_hoja))

# Función para visualizar el árbol
def visualizar_arbol(arbol):
    grafo = pydot.Dot(graph_type="graph")
    crear_nodo_arbol(arbol, grafo)
    grafo.write_png("arbol_parseo.png")

# Función para analizar sintácticamente el código fuente
def analizar_sintactico(data):
    try:
        resultado = parser.parse(data)
        if errores:
            for error in errores:
                print(error)
        else:
            visualizar_arbol(resultado)
            print("Árbol de parseo generado y guardado como 'arbol_parseo.png'")
    except SyntaxError as se:
        print(str(se))

# Ejemplo de prueba
if __name__ == "__main__":

    data = '''
    Def(var2,0);
    Put(var2, 10);
    '''
    
    analizar_sintactico(data)



