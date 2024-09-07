import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = ('num', p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print(f"Syntax error at '{p.value}'")

parser = yacc.yacc()

def check_semantics(ast):
    if isinstance(ast, tuple):
        if ast[0] == 'binop':
            op = ast[1]
            left = check_semantics(ast[2])  # Evalúa el operando izquierdo
            right = check_semantics(ast[3])  # Evalúa el operando derecho

            # Depuración: imprimir los valores de la izquierda y la derecha
            print(f"Operando izquierdo: {left}, Operación: {op}, Operando derecho: {right}")
            
            # Verificar división por cero
            if op == '/' and right == 0:
                raise Exception("Error semántico: División por cero")
            
            # Comprobar si ambos son números
            if isinstance(left, int) and isinstance(right, int):
                if op == '+':
                    return left + right
                elif op == '-':
                    return left - right
                elif op == '*':
                    return left * right
                elif op == '/':
                    return left // right  # División entera
            else:
                raise Exception("Error semántico: Operación entre tipos incompatibles")
        if ast[0] == 'num':
            return ast[1]
    else:
        # Es un número, así que devolvemos el valor numérico
        return ast[1]  # En el caso de ('num', valor), devolver el valor directamente

# Probar
ast = parser.parse("3 + 5 * (2 - 1)")
print("Árbol sintáctico:", ast)
resultado = check_semantics(ast)  # Debería devolver el resultado correcto: 8
print("Resultado:", resultado)


