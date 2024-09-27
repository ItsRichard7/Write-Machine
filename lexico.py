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

t_FOR = r'For'
t_LOOP = r'Loop'
t_CASE = r'Case'
t_WHEN = r'When'
t_THEN = r'Then'
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
    print(f"Error léxico: carácter no válido '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Crear y construir el analizador léxico
lexer = lex.lex()

# Verificación de que la primera línea sea un comentario
def verificar_comentario_inicial(lexer, data):
    lexer.first_comment = False  # Inicializamos la bandera
    lexer.input(data)  # Alimentamos el lexer con el código

    # Revisamos todos los tokens en la primera línea
    while True:
        tok = lexer.token()
        if not tok or tok.lineno > 1:
            break
        # Si es un comentario en la primera línea, marcamos como válido
        if tok.type == 'COMMENT':
            lexer.first_comment = True

    # Si no se encontró el comentario, lanzamos el error
    if not lexer.first_comment:
        print(f"Error en la línea {lexer.lineno}: La primera línea debe ser un comentario.")
        return False
    return True

# Función que recibe el código fuente y lo analiza léxicamente
def analizar(data):
    if verificar_comentario_inicial(lexer, data):
        lexer.input(data)  # Reiniciamos el lexer para el análisis completo
        for token in lexer:
            print(token)

data = '''// Este es el nombre del programa
Def(xxx, 5);
UseColor 255;
Proc myProc(zzz, www)
    [PosX 10; Down;]
End;
'''

analizar(data)