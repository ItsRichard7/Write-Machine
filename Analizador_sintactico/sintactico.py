import ply.yacc as yacc
from Analizador_lexico.lexico import tokens  # Asegúrate de que todos los tokens estén definidos aquí

# Definición de las reglas de producción

def p_program(p):
    '''program : COMMENT statements'''
    pass

def p_statements(p):
    '''statements : statement statements
                  | statement'''
    pass

def p_statement(p):
    '''statement : assign_stmt
                 | proc_stmt
                 | for_loop
                 | case_stmt
                 | repeat_stmt
                 | while_stmt
                 | boolean_expr
                 | move_stmt
                 | color_stmt'''
    pass

def p_assign_stmt(p):
    '''assign_stmt : DEF PARIZQ VARIABLE COMA NUMBER PARDER PUNTOCOMA
                   | PUT PARIZQ VARIABLE COMA NUMBER PARDER PUNTOCOMA'''
    pass

def p_proc_stmt(p):
    '''proc_stmt : DEF VARIABLE PARIZQ param_list PARDER proc_body END PUNTOCOMA'''
    pass

def p_proc_body(p):
    '''proc_body : BRAIZQ statements BRADER'''
    pass

def p_param_list(p):
    '''param_list : VARIABLE
                  | VARIABLE COMA param_list
                  | empty'''
    pass

def p_for_loop(p):
    '''for_loop : FOR VARIABLE PARIZQ NUMBER COMA NUMBER PARDER BRAIZQ statements BRADER END LOOP PUNTOCOMA'''
    pass

def p_case_stmt(p):
    '''case_stmt : CASE VARIABLE case_when_list case_else END CASE PUNTOCOMA'''
    pass

def p_case_when_list(p):
    '''case_when_list : when_clause
                      | when_clause case_when_list'''
    pass

def p_when_clause(p):
    '''when_clause : WHEN NUMBER THEN BRAIZQ statements BRADER'''
    pass

def p_case_else(p):
    '''case_else : ELSE BRAIZQ statements BRADER
                 | empty'''
    pass

def p_repeat_stmt(p):
    '''repeat_stmt : REPEAT BRAIZQ statements BRADER UNTIL PARIZQ boolean_expr PARDER PUNTOCOMA'''
    pass

def p_while_stmt(p):
    '''while_stmt : WHILE PARIZQ boolean_expr PARDER BRAIZQ statements BRADER WHEND PUNTOCOMA'''
    pass

def p_boolean_expr(p):
    '''boolean_expr : EQUAL PARIZQ expr COMA expr PARDER
                    | AND PARIZQ expr COMA expr PARDER
                    | OR PARIZQ expr COMA expr PARDER
                    | GREATER PARIZQ expr COMA expr PARDER
                    | SMALLER PARIZQ expr COMA expr PARDER'''
    pass

def p_expr(p):
    '''expr : NUMBER
            | VARIABLE
            | SUM PARIZQ expr COMA expr PARDER
            | MULT PARIZQ expr COMA expr PARDER
            | DIV PARIZQ expr COMA expr PARDER
            | RANDOM PARIZQ NUMBER PARDER'''
    pass

def p_move_stmt(p):
    '''move_stmt : CONUP NUMBER PUNTOCOMA
                 | CONDOWN NUMBER PUNTOCOMA
                 | CONRIGHT NUMBER PUNTOCOMA
                 | CONLEFT NUMBER PUNTOCOMA
                 | POSX NUMBER PUNTOCOMA
                 | POSY NUMBER PUNTOCOMA
                 | POS PARIZQ NUMBER COMA NUMBER PARDER PUNTOCOMA'''
    pass

def p_color_stmt(p):
    '''color_stmt : USECOLOR NUMBER PUNTOCOMA'''
    pass

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Error de sintaxis en token: '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de sintaxis al final de la entrada")

# Construcción del parser
parser = yacc.yacc()

# Prueba del analizador sintáctico
data = '''
// Este es el nombre del programa
Def(zzz, 5);
Proc myProc(zzz, zzz);
    [PosX 10; Down;]
End;
'''

result = parser.parse(data)

if result:
    print("Entrada válida")
else:
    print("Error en la entrada")
