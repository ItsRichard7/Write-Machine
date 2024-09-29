import ply.lex as lex
import re

# Lista para almacenar los errores léxicos
errores = []

# Definición de tokens
tokens = [
    'DEF',
    'PUT',
    'ADD',
    'CONUP',
    'CONDOWN',
    'CONRIGHT',
    'CONLEFT',
    'POS',
    'POSX',
    'POSY',
    'USECOLOR',
    'DOWN',
    'UP',
    'BEGIN',
    'EQUAL',
    'AND',
    'OR',
    'GREATER',
    'SMALLER',
    'SUBSTR',
    'RANDOM',
    'MULT',
    'DIV',
    'SUM',
    'PARIZQ',
    'PARDER',
    'BRAIZQ',
    'BRADER',
    'TRUE',
    'FALSE',
    'PUNTOCOMA',
    'NUMBER',
    'VARIABLE',
    'TO',
    'COMMENT',
    'TEXT',
    'FOR',
    'LOOP',
    'END',
    'CASE',
    'WHEN',
    'THEN',
    'ELSE',
    'REPEAT',
    'UNTIL',
    'WHILE',
    'WHEND',
    'PROC',
    'COMA',
    'OP_MULT',    # Operador de multiplicación *
    'OP_DIV',     # Operador de división /
    'OP_SUM',     # Operador de suma +
    'OP_SUB'      # Operador de resta -
]

# Expresiones regulares para tokens simples
t_DEF = r'Def'
t_PUT = r'Put'
t_PROC = r'Proc'
t_ADD = r'Add'
t_CONUP = r'ContinueUp'
t_CONDOWN = r'ContinueDown'
t_CONRIGHT = r'ContinueRight'
t_CONLEFT = r'ContinueLeft'
t_POS = r'Pos'
t_POSX = r'PosX'
t_POSY = r'PosY'
t_USECOLOR = r'UseColor'
t_DOWN = r'Down'
t_UP = r'Up'
t_BEGIN = r'Beginning'
t_EQUAL = r'Equal'
t_AND = r'And'
t_OR = r'Or'
t_TO = r'to'
t_GREATER = r'Greater'
t_SMALLER = r'Smaller'
t_SUBSTR = r'Substr'
t_RANDOM = r'Random'

t_MULT = r'Mult'
t_DIV = r'Div'
t_SUM = r'Sum'

t_OP_MULT = r'\*'  # Operador estándar de multiplicación *
t_OP_DIV = r'/'    # Operador estándar de división /
t_OP_SUM = r'\+'   # Operador estándar de suma +
t_OP_SUB = r'-'    # Operador estándar de resta -

t_FOR = r'For'
t_LOOP = r'Loop'
t_CASE = r'Case'
t_WHEN = r'When'
t_THEN = r'Then'
t_ELSE = r'Else'
t_REPEAT = r'Repeat'
t_UNTIL = r'Until'
t_WHILE = r'While'
t_WHEND = r'Whend'

t_PARIZQ = r'\('
t_PARDER = r'\)'
t_BRAIZQ = r'\['
t_BRADER = r'\]'
t_TRUE = r'TRUE'
t_FALSE = r'FALSE'
t_PUNTOCOMA = r';'
t_COMA = r',' 
t_END = r'End'

# Expresión regular para reconocer números enteros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expresión regular para variables con nuevas reglas
def t_VARIABLE(t):
    r'[a-z][a-zA-Z0-9_@]{2,9}'  # Empieza con minúscula, 3-10 caracteres
    return t

# Expresión regular para comentarios
def t_COMMENT(t):
    r'//.*'
    if t.lexer.lineno == 1:
        t.lexer.first_comment = True  # Marca que el primer comentario fue encontrado
    pass  # Ignorar comentarios

# Expresión regular para reconocer texto (cadenas de caracteres)
def t_TEXT(t):
    r'\"[^\"]*\"'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Función para manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores de token
def t_error(t):
    error_msg = f"Error léxico: carácter no válido '{t.value[0]}' en la línea {t.lexer.lineno}"
    errores.append(error_msg)
    t.lexer.skip(1)

# Crear y construir el analizador léxico
lexer = lex.lex()

# Verificación de que la primera línea sea un comentario
def verificar_comentario_inicial(data):
    primera_linea = data.splitlines()[0].strip()  # Obtenemos la primera línea del código fuente
    if re.match(r'//', primera_linea):  # Verificamos si la primera línea es un comentario
        return True
    else:
        error_msg = "Error: La primera línea debe ser un comentario."
        errores.append(error_msg)
        return False

# Función que recibe el código fuente y lo analiza léxicamente
def analizar(data):
    errores.clear()  # Limpiamos la lista de errores
    if verificar_comentario_inicial(data):
        lexer.input(data)  # Reiniciamos el lexer para el análisis completo
        """for token in lexer:
            print(token)"""
    # Imprimir errores si los hay
    if errores:
        print("Errores encontrados:")
        for error in errores:
            print(error)
            
data = '''// Este es un comentario
Def(xxx, 5);
UseColor 255;
Proc myProc(zzz, www)
    [PosX 10; Down;]
End;
'''

analizar(data)