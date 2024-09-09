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
    'BRAIZQ',
    'BRADER',
    'TRUE',
    'FALSE',
    'PUNTOCOMA',
    'NUMBER',
    'VARIABLE',
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
t_BRAIZQ = r'\['
t_BRADER = r'\]'
t_TRUE = r'True'
t_FALSE = r'False'
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
    # Si es la primera línea y es un comentario, marcamos first_comment como True
    if t.lexer.lineno == 1:
        t.lexer.first_comment = True
    pass  # Ignoramos los comentarios

# Expresión regular para reconocer texto (cadenas de caracteres)
def t_TEXT(t):
    r'\"[^\"]*\"'
    return t

# Ignorar espacios y saltos de línea
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores de token
def t_error(t):
    print(f"Carácter no válido: '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Verificación de que la primera línea es un comentario
def verificar_comentario_inicial(lexer, data):
    lexer.first_comment = False  # Inicializamos el estado del comentario
    lexer.input(data)
    # Revisar tokens para encontrar el primer token
    for tok in lexer:
        # Si es un comentario y está en la primera línea
        if lexer.lineno == 1 and tok.type == 'COMMENT':
            lexer.first_comment = True
        break  # Solo verificamos el primer token
    
    # Si no se encontró el comentario, lanzar error
    if not lexer.first_comment:
        print(f"Error en la línea {lexer.lineno}: La primera línea debe ser un comentario.")
        return False
    return True

# Programa para verificar el funcionamiento
data = '''
Def(xxx, 5);
UseColor 255;
Proc myProc(zzz, www)
    [PosX 10; Down;]
End;
'''
# Verificaciones Léxicas
verificar_comentario_inicial(lexer, data)
lexer.input(data)
for token in lexer:
    print(token)