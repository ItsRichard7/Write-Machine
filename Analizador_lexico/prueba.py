#Codigo tomado de https://www.youtube.com/watch?v=iXArNJWLYes

import ply.lex as lex

#Definición de tokens
tokens = ['NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE']

#Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'

#Expresión regular para reconocer números enteros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

#Ignorar caracteres como espacios y saltos de línea
t_ignore = ' \n'

#Manejo de errores de token
def t_error(t):
    print("Carácter no válido: '%s'" % t.value[0])
    t.lexer.skip(1)

#Construcción del analizador léxico
lexer = lex.lex()

#Ejemplo de uso
data = "3 + 4 * 2"
lexer.input(data)

#Obtener los tokens reconocidos
while True:
    token = lexer.token()
    if not token:
        break
    print(token)