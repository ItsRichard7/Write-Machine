import ply.lex as lex

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
    'TRUE',
    'FALSE',
    'PUNTOCOMA',
    'NUMBER',
    'VARIABLE',
    'COMMENT',
    'TEXT'
]

# Expresiones regulares para tokens simples
t_DEF = r'Def'
t_PUT = r'Put'
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
t_BEGIN = r'Beginning;'
t_EQUAL = r'Equal'
t_AND = r'And'
t_OR = r'Or'
t_GREATER = r'Greater'
t_SMALLER = r'Smaller'
t_SUBSTR = r'Substr'
t_RANDOM = r'Random'
t_MULT = r'Mult'
t_DIV = r'Div'
t_SUM = r'Sum'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_TRUE = r'True'
t_FALSE = r'False'
t_PUNTOCOMA = r';'

# Expresión regular para reconocer números enteros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expresión regular para variables (3-10 caracteres, letras, números, '@', '_')
def t_VARIABLE(t):
    r'[a-zA-Z0-9_@]{3,10}'
    return t

# Expresión regular para reconocer comentarios que inician con //
def t_COMMENT(t):
    r'//.*'
    pass  # Ignoramos los comentarios, no se generan tokens

# Expresión regular para reconocer texto (cadenas de caracteres)
def t_TEXT(t):
    r'\".*?\"'
    return t

# Ignorar caracteres como espacios y saltos de línea
t_ignore = ' \n'

# Manejo de errores de token
def t_error(t):
    print("Carácter no válido: '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Ejemplo de uso
data = "ContinueUp 10; // Esto es un comentario\nVar1 = \"Hello world\";"

lexer.input(data)

# Obtener los tokens reconocidos
while True:
    token = lexer.token()
    if not token:
        break
    print(token)
