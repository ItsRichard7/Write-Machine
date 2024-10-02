from lexico import errores
import random
from PIL import Image, ImageDraw, ImageFont

class AnalizadorSemantico:
    def __init__(self, arbol_sintactico):
        # Esta tabla de símbolos almacenará las variables declaradas, sus tipos y valores
        self.tabla_simbolos = {}
        self.main = False
        self.arbol_sintactico = arbol_sintactico
        self.fallido = False

    def analizar(self, nodo, alcance ='global'):
        """
        Analiza recursivamente el nodo del árbol sintáctico y realiza las comprobaciones semánticas.
        """
        if isinstance(nodo, tuple):
            tipo_nodo = nodo[0]

            # Analizar declaraciones de variables
            if self.fallido:
                return
            # Analizar declaraciones de variables
            elif tipo_nodo == 'def_variable':
                self.analizar_declaracion_variable(nodo, alcance)

            # Analizar cambios de variable
            elif tipo_nodo == 'put_variable':
                self.analizar_uso_variable(nodo[1], alcance, nodo[2][1])

            # Analizar operaciones suma de una variable
            elif tipo_nodo == 'add_variable_uno':
                self.analizar_operacion_add(nodo[1], alcance)

            # Analizar operaciones suma con dos argumentos
            elif tipo_nodo == 'add_variable_dos':
                self.analizar_operacion_add(nodo[1], alcance, nodo[2][1])

            # Analizar operaciones continue del lapiz
            elif tipo_nodo == 'continue_up' or tipo_nodo == 'continue_down' or tipo_nodo == 'continue_left' or tipo_nodo == 'continue_right':
                if len(nodo[1]) > 2:
                    mov = self.verificar_operacion(nodo[1], alcance)
                    print(f"Mover lapicero con {tipo_nodo} por {mov} unidades.")
                else:
                    self.verificar_entero(nodo[1][1], alcance)
                    print(f"Mover lapicero con {tipo_nodo} por {nodo[1][1]} unidades.")

            # Analizar operaciones de Pos(x,y)
            elif tipo_nodo == 'pos':
                self.analizar_pos(nodo, alcance)

            # Analizar operaciones PosX y PosY para posicionar el lapicero
            elif tipo_nodo == 'posx' or tipo_nodo == 'posy':
                self.analizar_pos_xy(nodo, alcance)

            # Analizar operaciones de cambio de color del lapicero
            elif tipo_nodo == 'use_color':
                self.verificar_entero(nodo[1][1], alcance)
                valor = self.obtener_valor(nodo[1], alcance)
                if valor != 1 and valor != 2:
                    error = (f"Error semántico: el valor de UseColor debe ser 1 o 2, se obtuvo {valor}.")
                    errores.append(error)
                    self.analisis_fallido()
                else: 
                    print(f"Usar color {valor}.")
            
            # Analizar operaciones para bajar el lapicero
            elif tipo_nodo == 'down':
                print("Mover lapicero hacia abajo.")
            
            # Analizar operaciones para subir el lapicero
            elif tipo_nodo == 'up':
                print("Mover lapicero hacia arriba.")

            # Analizar operaciones para mover el lapicero a la posicion incial
            elif tipo_nodo == 'beginning':
                print("Mover lapicero a [1,1].")

            # Analizar for_loop
            elif tipo_nodo == 'for_loop':
                self.analizar_for(nodo, alcance)
            
            # Analizar case
            elif tipo_nodo == 'case':
                self.analizar_case(nodo, alcance)
                return
            
            # Analizar while loop
            elif tipo_nodo == 'while':
                self.analizar_while(nodo, alcance)
                return
            
            # Analizar repeat until
            elif tipo_nodo == 'repeat_until':
                self.analizar_repeat(nodo, alcance)
                return

            # Analizar Equal(x,y)
            elif tipo_nodo == 'equal':
                self.analizar_equal(nodo, alcance)

            # Analizar And(x,y)
            elif tipo_nodo == 'and':
                self.analizar_and(nodo, alcance)

            # Analizar Or(x,y)
            elif tipo_nodo == 'or':
                self.analizar_or(nodo, alcance)

            # Analizar Greater(x,y)
            elif tipo_nodo == 'greater':
                self.analizar_greater(nodo, alcance)

            # Analizar Smaller(x,y)
            elif tipo_nodo == 'smaller':
                self.analizar_smaller(nodo, alcance)

            # Analizar Substr(x,y)
            elif tipo_nodo == 'substract':
                self.analizar_substract(nodo, alcance)

            # Analizar Random(x,y)
            elif tipo_nodo == 'random':
                self.analizar_random(nodo, alcance)

            # Analizar Mult(x,y)
            elif tipo_nodo == 'mult':
                self.analizar_mult(nodo, alcance)

            # Analizar Div(x,y)
            elif tipo_nodo == 'div':
                self.analizar_div(nodo, alcance)

            # Analizar Sum(x,y)
            elif tipo_nodo == 'sum':
                self.analizar_sum(nodo, alcance)
            
            # Analizar creacion de procedimientos
            elif tipo_nodo == 'proc':
                self.analizar_proc(nodo, alcance)
                return

            # Analizar invocacion de procedimientos
            elif tipo_nodo == 'invocacion_proc':
                self.analizar_invocacion_proc(nodo, alcance)

            # Si el nodo contiene más subnodos (sentencias), procesarlos también
            for subnodo in nodo[1:]:
                self.analizar(subnodo, alcance)

            # Verificar si el procedimiento main fue declarado
            if nodo == self.arbol_sintactico and not self.main:
                error = (f"Error semántico: no se encontró el procedimiento main.")
                errores.append(error)
                self.analisis_fallido = True

    # Funcion que pone la bandera del analisis fallido y borra la tabla de simbolos
    def analisis_fallido(self):
        self.fallido = True
        self.tabla_simbolos = {}


    # Analizar declaraciones de variables
    def analizar_declaracion_variable(self, nodo, alcance):
        """
        Verifica si la variable ya fue declarada, la agrega a la tabla de símbolos y asigna su valor.
        """
        nombre_variable = nodo[1]
        valor_variable = nodo[2][1]  # Suponiendo que el valor es el segundo elemento en el subnodo

        # Verificar si el valor es un entero o un booleano (TRUE o FALSE)
        if isinstance(valor_variable, int):
            tipo_variable = 'entero'
        elif valor_variable in ["TRUE", "FALSE"]:
            tipo_variable = 'booleano'
        else:
            error = (f"Error semántico: el valor '{valor_variable}' no es un tipo válido (se esperaba entero o booleano).")
            errores.append(error)
            self.analisis_fallido()
            return
            
        # Verificar si la variable ya fue declarada
        if nombre_variable in self.tabla_simbolos:
            error = (f"Error semántico: la variable '{nombre_variable}' ya fue declarada.")
            errores.append(error)
            self.analisis_fallido()
            return
        
        # Agregar la variable a la tabla de símbolos
        self.tabla_simbolos[nombre_variable] = {'tipo': tipo_variable, 'valor': valor_variable, 'alcance': alcance}
        print(f"Declarada la variable '{nombre_variable}' como '{tipo_variable}' con valor {valor_variable}.")

    def analizar_uso_variable(self, nombre_variable, alcance, nuevo_valor=None):
        """
        Verifica si la variable ha sido declarada antes de su uso y valida el tipo de la variable.
        """
        if nombre_variable not in self.tabla_simbolos:
            error = (f"Error semántico: la variable '{nombre_variable}' se usa antes de ser declarada.")
            errores.append(error)
            self.analisis_fallido()
            return
        
        # Obtener el tipo y el valor actual de la variable
        tipo_actual = self.tabla_simbolos[nombre_variable]['tipo']
        valor_actual = self.tabla_simbolos[nombre_variable]['valor']
        
        # Imprimir el valor actual de la variable
        print(f"Variable '{nombre_variable}' está siendo usada correctamente. Valor actual: {valor_actual}.")

        # Si hay un nuevo valor proporcionado, verificar su tipo
        if nuevo_valor is not None:
            nuevo_tipo = 'entero' if isinstance(nuevo_valor, int) else 'booleano' if nuevo_valor in ["TRUE", "FALSE"] else None
            
            if self.tabla_simbolos[nombre_variable]['alcance'] != alcance and self.tabla_simbolos[nombre_variable]['alcance'] != 'global':
                error = (f"Error semántico: la variable '{nombre_variable}' no se puede modificar en este alcance.")
                errores.append(error)
                self.analisis_fallido()
                return 

            if nuevo_tipo is None:
                error = (f"Error semántico: el nuevo valor '{nuevo_valor}' no es un tipo válido (se esperaba entero o booleano).")
                errores.append(error)
                self.analisis_fallido()
                return
            
            # Verificar la consistencia de tipos
            if nuevo_tipo != tipo_actual:
                error = (f"Error semántico: no se puede asignar el valor '{nuevo_valor}' de tipo '{nuevo_tipo}' a la variable '{nombre_variable}' que es de tipo '{tipo_actual}'.")
                errores.append(error)
                self.analisis_fallido()
                return

            # Si el tipo es correcto, actualiza el valor
            self.tabla_simbolos[nombre_variable]['valor'] = nuevo_valor
            print(f"Valor de la variable '{nombre_variable}' actualizado a {nuevo_valor}.")
        else:
            error = f"Error semántico: la variable '{nombre_variable}' no se le esta asignando un valor."
            errores.append(error)
            self.analisis_fallido()
            return
    
    def analizar_operacion_add(self, nombre_variable, alcance, valor_b=1):
        """
        Verifica que los valores en la operación Add sean enteros,
        realiza la suma con el valor de la variable y actualiza la tabla de símbolos.
        """
        # Verificar que el primer operando sea una variable y obtener su valor
        if nombre_variable not in self.tabla_simbolos:
            error = (f"Error semántico: la variable '{nombre_variable}' no ha sido declarada.")
            errores.append(error)
            self.analisis_fallido()
            return
        
        elif self.tabla_simbolos[nombre_variable]['alcance'] != alcance and self.tabla_simbolos[nombre_variable]['alcance'] != 'global':
                error = (f"Error semántico: la variable '{nombre_variable}' no se puede modificar en este alcance.")
                errores.append(error)
                self.analisis_fallido()
                return 
        
        valor_a_sumar = self.tabla_simbolos[nombre_variable]['valor']
        tipo_a = self.tabla_simbolos[nombre_variable]['tipo']

        
        
        # Determinar el valor del segundo operando
        if isinstance(valor_b, str):  # Si es una variable
            if valor_b == 'TRUE' or valor_b == 'FALSE':
                error = (f"Error semántico: no se puede sumar un valor booleano.")
                errores.append(error)
                self.analisis_fallido()
                return
            
            elif valor_b not in self.tabla_simbolos:
                error = (f"Error semántico: la variable '{valor_b}' no ha sido declarada.")
                errores.append(error)
                self.analisis_fallido()
                return
            
            elif self.tabla_simbolos[valor_b]['alcance'] != alcance and self.tabla_simbolos[valor_b]['alcance'] != 'global':
                error = (f"Error semántico: la variable '{valor_b}' no se puede modificar en este alcance.")
                errores.append(error)
                self.analisis_fallido()
                return 
            
            valor_b_sumar = self.tabla_simbolos[valor_b]['valor']
            tipo_b = self.tabla_simbolos[valor_b]['tipo']
            
            # Verificar que ambos tipos sean enteros
            if tipo_a != 'entero' or tipo_b != 'entero':
                error = (f"Error semántico: las variables deben ser de tipo entero. '{nombre_variable}' es de tipo '{tipo_a}' y '{valor_b}' es de tipo '{tipo_b}'.")
                errores.append(error)
                self.analisis_fallido()
                return
        else:  # Si es un número
            valor_b_sumar = valor_b  # Asumimos que ya es un entero
            if not isinstance(valor_b_sumar, int):
                error = (f"Error semántico: el valor a sumar debe ser un entero. Se recibió: '{valor_b_sumar}'.")
                errores.append(error)
                self.analisis_fallido()
                return
        
        # Verificar que el tipo de valor_a_sumar sea entero
        if tipo_a != 'entero':
            error = (f"Error semántico: no se puede sumar a la variable '{nombre_variable}' de tipo '{tipo_a}'.")
            errores.append(error)
            self.analisis_fallido()
            return

        # Realizar la suma
        nuevo_valor = valor_a_sumar + valor_b_sumar
        
        # Actualizar el valor en la tabla de símbolos
        self.tabla_simbolos[nombre_variable]['valor'] = nuevo_valor
        print(f"Variable '{nombre_variable}' actualizada. Nuevo valor: {nuevo_valor}.")

    def verificar_entero(self, valor, alcance):
        if isinstance(valor, str):  # Si es una variable
            if valor not in self.tabla_simbolos:
                error = (f"Error semántico: la variable '{valor}' no ha sido declarada.")
                errores.append(error)
                self.analisis_fallido()
                return
            tipo_variable = self.tabla_simbolos[valor]['tipo']
            if tipo_variable != 'entero':
                error = (f"Error semántico: la variable '{valor}' debe ser de tipo entero. Es de tipo '{tipo_variable}'.")
                errores.append(error)
                self.analisis_fallido()
                return
            if self.tabla_simbolos[valor]['alcance'] != alcance and self.tabla_simbolos[valor]['alcance'] != 'global':
                error = (f"Error semántico: la variable '{valor}' no se puede modificar en este alcance.")
                errores.append(error)
                self.analisis_fallido()
                return
        else:  # Se asume que el valor es un número
            if not isinstance(valor, int):
                error = (f"Error semántico: se esperaba un entero, se recibió: '{valor}'.")
                errores.append(error)
                self.analisis_fallido()
                return
     # Función para verificar si el valor es una variable o un número
    def verificar_booleano(self, valor, alcance):
        if isinstance(valor, str):  # Si es una variable
            if valor == 'TRUE':
                return True
            elif valor == 'FALSE':
                    return False
            elif valor not in self.tabla_simbolos:
                error = (f"Error semántico: la variable '{valor}' no ha sido declarada.")
                errores.append(error)
                self.analisis_fallido()
                return
            elif self.tabla_simbolos[valor]['alcance'] != alcance and self.tabla_simbolos[valor]['alcance'] != 'global':
                error = (f"Error semántico: la variable '{valor}' no se puede modificar en este alcance.")
                errores.append(error)
                self.analisis_fallido()
                return
            else:
                booleano = self.tabla_simbolos[valor]['valor']
                if isinstance(booleano, bool):
                    return booleano
                else:
                    error = (f"Error semántico: la variable '{valor}' debe ser de tipo booleano.")
                    errores.append(error)
                    self.analisis_fallido()
                    return
                
    def verificar_operacion(self, node, alcance):
        # Si el nodo es un número, lo devolvemos
        if node[0] == 'number':
            return node[1]
        
        # Si el nodo es una operación (multiplicación, división, suma o resta)
        operator = node[0]
        left = self.obtener_valor(node[1], alcance)  # Evalúa el operando izquierdo
        right = self.obtener_valor(node[2], alcance)  # Evalúa el operando derecho

        # Verificar que ambos operandos sean enteros
        if not isinstance(left, int) or not isinstance(right, int):
            error = f"Error: Los operandos deben ser enteros. Recibido: {left} y {right}"
            errores.append(error)
            self.analisis_fallido()
            return
        
        result = 0
        
        # Realiza la operación en función del operador
        if operator == '*':
            result = left * right
        elif operator == '/':
            # Aseguramos que no se divida por cero
            if right == 0:
                error = f"Error: División por cero."
                errores.append(error)
                raise ZeroDivisionError(error)
            result = round(left / right)
        elif operator == '+':
            result = left + right
        elif operator == '-':
            result = left - right
        
        return result
        
    def verificar_operacion_booleana(self, node, alcance):
        # Si el nodo es un número, lo devolvemos
        if node[0] == 'number':
            return node[1]
        
        # Si el nodo es una operación (multiplicación, división, suma o resta)
        operator = node[0]
        left = self.obtener_valor(node[1], alcance)  # Evalúa el operando izquierdo
        right = self.obtener_valor(node[2], alcance)  # Evalúa el operando derecho

        # Verificar que ambos operandos sean enteros
        if not isinstance(left, int) or not isinstance(right, int):
            error = f"Error: Los operandos deben ser enteros. Recibido: {left} y {right}"
            errores.append(error)
            self.analisis_fallido()
            return
        result = 0
        
        # Realiza la operación en función del operador
        if operator == '>':
            result = left > right
        elif operator == '<':
            result = left < right
        elif operator == '==':
            result = left == right
        elif operator == '>=':
            result = left >= right
        elif operator == '<=':
            result = left <= right
        
        return result

    def analizar_pos(self, nodo, alcance):
        """
        Verifica que ambos valores en la operación Pos sean enteros.
        """

        valor_a = 0
        valor_b = 0

        if len(nodo[1]) > 2:
            valor_a = self.verificar_operacion(nodo[1], alcance)
            if len(nodo[2]) > 2:
                valor_b = self.verificar_operacion(nodo[2], alcance)
            else:
                valor_b = nodo[2][1]
        elif len(nodo[2]) > 2:
            valor_b = self.verificar_operacion(nodo[2], alcance)
            if len(nodo[1]) > 2:
                valor_a = self.verificar_operacion(nodo[1], alcance)
            else:
                valor_b = nodo[2][1]
        else:
            valor_a = self.obtener_valor(nodo[1], alcance)  # Primer argumento
            valor_b = self.obtener_valor(nodo[2], alcance)  # Segundo argumento            print(f"Resultado de {left} - {right} = {result}")

            # Verificar ambos valores
            self.verificar_entero(valor_a, alcance)
            self.verificar_entero(valor_b, alcance)

        print(f"Posicionar lapicero en [{valor_a}, {valor_b}].")

    def analizar_pos_xy(self, nodo, alcance):
        """
        Verifica que ambos valores en la operación Pos sean enteros.
        """

        valor_a = 0 

        if len(nodo[1]) > 2:
            valor_a = self.verificar_operacion(nodo[1], alcance)
        else:
            valor_a = self.obtener_valor(nodo[1], alcance)  # Primer argumento

            # Verificar ambos valores
            self.verificar_entero(valor_a, alcance)

        print(f"Posicionar usando {nodo[0]} en {valor_a}.")

    def analizar_case(self, nodo, alcance):
        
        nombre_variable = nodo[1]
        self.verificar_entero(nombre_variable, alcance)
        valor_actual = self.tabla_simbolos[nombre_variable]['valor']

        casos = self.buscar_todos_when_cases(nodo)
        for i in range(len(casos)):
            caso = casos[i][1][1]
            if not isinstance(caso, int):
                error = (f"Error semántico: el caso debe de ser entero, se obtuvo {caso}.")
                errores.append(error)
                self.analisis_fallido()
                return
            else:
                if caso == valor_actual:
                    print(f"El caso {caso} se cumple.")
                    sentencia = self.obtener_sentencias_a_ejecutar(casos[i], nodo)
                    self.analizar(sentencia, alcance)
                    break

    def obtener_sentencias_a_ejecutar(self, when_case, arbol):
        # Busca el nodo 'when_case' en el árbol y devuelve las sentencias
        if isinstance(arbol, tuple):
            # Verifica si el árbol tiene la estructura del 'when_case'
            if arbol[0] == 'when_case' and arbol[1][1] == when_case[1][1]:
                # Devuelve las sentencias asociadas a este 'when_case'
                return arbol[2]  # 'arbol[2]' contiene las sentencias

            # Recursivamente recorrer los hijos del árbol
            for hijo in arbol[1:]:
                sentencias = self.obtener_sentencias_a_ejecutar(when_case, hijo)
                if sentencias:
                    return sentencias
        return None

    def buscar_todos_when_cases(self, arbol):
     # Lista para acumular los resultados
        resultados = []

        # Verificar si es una tupla
        if isinstance(arbol, tuple):
            # Si el nodo es un 'when_case', agregarlo a los resultados
            if arbol[0] == 'when_case':
                resultados.append(arbol[:2])  # Agregar solo la parte que necesitas

            # Recursivamente recorrer los hijos del árbol
            for hijo in arbol[1:]:
                resultados.extend(self.buscar_todos_when_cases(hijo))

        # Devolver todos los resultados como una tupla
        return tuple(resultados)
    
    def analizar_for(self, nodo, alcance):
        var = nodo[1]
        indice_menor = nodo[2][1]
        indice_mayor = nodo[3][1]
        self.verificar_entero(indice_menor, alcance)
        self.verificar_entero(indice_mayor, alcance)
        if var not in self.tabla_simbolos: 
            self.tabla_simbolos[var] = {'tipo': "entero", 'valor': indice_menor}
            while indice_menor < indice_mayor:
                for i in range(len(self.extraer_sentencias(nodo))):
                    sentencia = self.extraer_sentencias(nodo)[i]
                    self.analizar(sentencia, alcance)
                indice_menor += 1
                self.tabla_simbolos[var]['valor'] = indice_menor
        else:
            error = (f"Error semántico: la variable '{var}' ya ha sido declarada.")
            errores.append(error)
            self.analisis_fallido()
            return
        
        
    def extraer_sentencias(self,node):
        # Lista para almacenar las sentencias encontradas
        sentencias_encontradas = []

        # Si el nodo es una tupla y su primer elemento es 'sentencia', lo agregamos a la lista
        if isinstance(node, tuple) and node[0] == 'sentencia':
            sentencias_encontradas.append(node)
        
        # Si el nodo es una tupla, lo recorremos recursivamente
        if isinstance(node, tuple):
            for subnode in node:
                # Llamada recursiva para explorar las subestructuras del árbol
                sentencias_encontradas.extend(self.extraer_sentencias(subnode))
        
        # Devolvemos las sentencias encontradas
        return sentencias_encontradas
    
    def analizar_while(self, nodo, alcance):
        operacion = nodo[1][0]
        result = True
        
        while result:

            if operacion == 'equal':
                result = self.analizar_equal(nodo[1], alcance)
            elif operacion == 'greater':
                result = self.analizar_greater(nodo[1], alcance)
            elif operacion == 'smaller':
                result = self.analizar_smaller(nodo[1], alcance)
            elif operacion == 'and':
                result = self.analizar_and(nodo[1], alcance)
            elif operacion == 'or':
                result = self.analizar_or(nodo[1], alcance)
            elif operacion == '<' or operacion == '>' or operacion == '==' or operacion == '<=' or operacion == '>=':
                result = self.verificar_operacion_booleana(nodo[-1], alcance)

            for i in range(len(self.extraer_sentencias(nodo))):
                sentencia = self.extraer_sentencias(nodo)[i]
                print("sentencia: ", sentencia)
                self.analizar(sentencia, alcance)
            self.analizar_while(nodo, alcance)

    def analizar_repeat(self, nodo, alcance):
        operacion = nodo[-1][0]
        sentencias = self.extraer_sentencias(nodo)
        resultado = True

        while resultado:
            
            for i in range(len(sentencias)):
                sentencia = sentencias[i]
                self.analizar(sentencia, alcance)

            if operacion == 'equal':
                resultado = self.analizar_equal(nodo[-1], alcance)
            elif operacion == 'greater':
                resultado = self.analizar_greater(nodo[-1], alcance)
            elif operacion == 'smaller':
                resultado = self.analizar_smaller(nodo[-1], alcance)
            elif operacion == 'and':
                resultado = self.analizar_and(nodo[-1], alcance)
            elif operacion == 'or':
                resultado = self.analizar_or(nodo[-1])
            elif operacion == '<' or operacion == '>' or operacion == '==' or operacion == '<=' or operacion == '>=':
                resultado = self.verificar_operacion_booleana(nodo[-1], alcance)   
            else:
                error = (f"Error semántico: operación no válida.")
                errores.append(error)
                self.analisis_fallido()
                return
            print("resultado: ", resultado)


        
    
    # Función para obtener el valor de un operando, ya sea variable o número literal
    def obtener_valor(self,operando, alcance):
        if isinstance(operando, int):
            return operando  
        elif isinstance(operando, tuple) and operando[0] == 'variable':  # Si es una variable
            if operando[1] in self.tabla_simbolos:
                if self.tabla_simbolos[operando[1]]['alcance'] != alcance and self.tabla_simbolos[operando[1]]['alcance'] != 'global':
                    error = (f"Error semántico: la variable '{operando[1]}' no se puede modificar en este alcance.")
                    errores.append(error)
                    self.analisis_fallido()
                    return
                return self.tabla_simbolos[operando[1]]['valor']
            else:
                error = (f"Error: la variable '{operando}' no está definida.")
                errores.append(error)
                self.analisis_fallido()
                return
        elif isinstance(operando, tuple) and operando[0] == 'number' or operando[0] == 'logico':  
            return operando[1]  # Retorna el valor numérico
        else:
            error = ("Error: operando no válido.")
            errores.append(error)
            self.analisis_fallido()
            return

    def analizar_equal(self, nodo, alcance):
        # nodo: ('equal', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]
        valor1 = 0
        valor2 = 0

        if len(operando1) > 2:
            valor1 = self.verificar_operacion(operando1, alcance)
            if len(operando2) > 2:
                valor2 = self.verificar_operacion(operando2, alcance)
            else:
                valor2 = self.obtener_valor(operando2, alcance)

        elif len(operando2) > 2:
            valor2 = self.verificar_operacion(operando2, alcance)
            if len(operando1) > 2:
                valor1 = self.verificar_operacion(operando1, alcance)
            else:
                valor1 = self.obtener_valor(operando1, alcance)
        else:
            # Obtener valores de ambos operandos
            valor1 = self.obtener_valor(operando1, alcance, alcance)
            valor2 = self.obtener_valor(operando2, alcance, alcance)

            # Verificar que ambos valores sean enteros
            self.verificar_entero(valor1)
            self.verificar_entero(valor2)

        # Comparar los valores y devolver el resultado
        resultado = valor1 == valor2
        print(f"Resultado de la comparación {valor1} == {valor2}: {resultado}")
        return resultado
    
    def analizar_and(self, nodo, alcance):
         # nodo: ('equal', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]
        valor1 = 0
        valor2 = 0

        if len(operando1) > 2:
            valor1 = self.verificar_operacion_booleana(operando1, alcance)
            if len(operando2) > 2:
                valor2 = self.verificar_operacion_booleana(operando2, alcance)
            else:
                valor2 = self.obtener_valor(operando2, alcance)

        elif len(operando2) > 2:
            valor2 = self.verificar_operacion_booleana(operando2, alcance)
            if len(operando1) > 2:
                valor1 = self.verificar_operacion_booleana(operando1, alcance)
            else:
                valor1 = self.obtener_valor(operando1, alcance)
        else:
            # Obtener valores de ambos operandos
            valor1 = self.obtener_valor(operando1, alcance)
            valor2 = self.obtener_valor(operando2, alcance)

            # Verificar que ambos valores sean enteros
            self.verificar_booleano(valor1, alcance)
            self.verificar_booleano(valor2, alcance)

        # Comparar los valores y devolver el resultado
        resultado = valor1 and valor2
        print(f"Resultado de la comparación {valor1} and {valor2}: {resultado}")
        return resultado
    
    def analizar_or(self, nodo, alcance):
         # nodo: ('equal', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]
        valor1 = 0
        valor2 = 0

        if len(operando1) > 2:
            valor1 = self.verificar_operacion_booleana(operando1, alcance)
            if len(operando2) > 2:
                valor2 = self.verificar_operacion_booleana(operando2, alcance)
            else:
                valor2 = self.obtener_valor(operando2, alcance)

        elif len(operando2) > 2:
            valor2 = self.verificar_operacion_booleana(operando2, alcance)
            if len(operando1) > 2:
                valor1 = self.verificar_operacion_booleana(operando1, alcance)
            else:
                valor1 = self.obtener_valor(operando1, alcance)
        else:
            # Obtener valores de ambos operandos
            valor1 = self.obtener_valor(operando1, alcance)
            valor2 = self.obtener_valor(operando2, alcance)

            # Verificar que ambos valores sean enteros
            self.verificar_booleano(valor1, alcance)
            self.verificar_booleano(valor2, alcance)

        # Comparar los valores y devolver el resultado
        resultado = valor1 or valor2
        print(f"Resultado de la comparación {valor1} or {valor2}: {resultado}")
        return resultado
    
    def analizar_greater(self, nodo, alcance):
        # nodo: ('equal', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]
        valor1 = 0
        valor2 = 0

        if len(operando1) > 2:
            valor1 = self.verificar_operacion(operando1, alcance)
            if len(operando2) > 2:
                valor2 = self.verificar_operacion(operando2, alcance)
            else:
                valor2 = self.obtener_valor(operando2, alcance)

        elif len(operando2) > 2:
            valor2 = self.verificar_operacion(operando2, alcance)
            if len(operando1) > 2:
                valor1 = self.verificar_operacion(operando1, alcance)
            else:
                valor1 = self.obtener_valor(operando1, alcance)
        else:
            # Obtener valores de ambos operandos
            valor1 = self.obtener_valor(operando1, alcance)
            valor2 = self.obtener_valor(operando2, alcance)

            # Verificar que ambos valores sean enteros
            self.verificar_entero(valor1, alcance)
            self.verificar_entero(valor2, alcance)

        # Comparar los valores y devolver el resultado
        resultado = valor1 > valor2
        print(f"Resultado de la comparación {valor1} > {valor2}: {resultado}")
        return resultado

    def analizar_smaller(self, nodo, alcance):
        operando1 = nodo[1]
        operando2 = nodo[2]
        valor1 = 0
        valor2 = 0

        if len(operando1) > 2:
            valor1 = self.verificar_operacion(operando1, alcance)
            if len(operando2) > 2:
                valor2 = self.verificar_operacion(operando2, alcance)
            else:
                valor2 = self.obtener_valor(operando2, alcance)

        elif len(operando2) > 2:
            valor2 = self.verificar_operacion(operando2, alcance)
            if len(operando1) > 2:
                valor1 = self.verificar_operacion(operando1, alcance)
            else:
                valor1 = self.obtener_valor(operando1, alcance)
        else:
            # Obtener valores de ambos operandos
            valor1 = self.obtener_valor(operando1, alcance)
            valor2 = self.obtener_valor(operando2, alcance)

            # Verificar que ambos valores sean enteros
            self.verificar_entero(valor1, alcance)
            self.verificar_entero(valor2, alcance)

        # Comparar los valores y devolver el resultado
        resultado = valor1 < valor2
        print(f"Resultado de la comparación {valor1} < {valor2}: {resultado}")
        return resultado

    def analizar_substract(self, nodo, alcance):
        # nodo: ('substract', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1, alcance)
        valor2 = self.obtener_valor(operando2, alcance)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor1, alcance)
        self.verificar_entero(valor2, alcance)

        # Comparar los valores y devolver el resultado
        resultado = valor1 - valor2
        print(f"Resultado de la resta {valor1} - {valor2} = {resultado}")
        return resultado

    def analizar_random(self, nodo, alcance):
        # nodo: ('random', operand1)
        operando = nodo[1]

        # Obtener valores de ambos operandos
        valor = self.obtener_valor(operando, alcance)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor, alcance)

        # Comparar los valores y devolver el resultado
        resultado = random.randint(0, valor)
        print(f"Resultado de numero random es  {valor} = {resultado}")
        return resultado

    def analizar_mult(self, nodo, alcance):
        # nodo: ('mult', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1, alcance)
        valor2 = self.obtener_valor(operando2, alcance)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor1, alcance)
        self.verificar_entero(valor2, alcance)

        # Comparar los valores y devolver el resultado
        resultado = valor1 * valor2
        print(f"Resultado de la multiplicacion {valor1} * {valor2} = {resultado}")
        return resultado

    def analizar_div(self, nodo, alcance):
        # nodo: ('div', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1, alcance)
        valor2 = self.obtener_valor(operando2, alcance)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor1, alcance)
        self.verificar_entero(valor2, alcance)

        # Comparar los valores y devolver el resultado
        if valor2 == 0:
            error = ("Error: operando 2 no válido.")
            errores.append(error)
            self.analisis_fallido()
            return
        else:
            resultado = valor1 / valor2
            print(f"Resultado de la division {valor1} / {valor2} = {resultado}")
        return resultado

    def analizar_sum(self, nodo, alcance):
        # nodo: ('sum', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1, alcance)
        valor2 = self.obtener_valor(operando2, alcance)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor1, alcance)
        self.verificar_entero(valor2, alcance)

        # Comparar los valores y devolver el resultado
        resultado = valor1 + valor2
        print(f"Resultado de la suma {valor1} + {valor2} = {resultado}")
        return resultado
    
    def analizar_proc(self, nodo, alcance):
        nombre = nodo[1]
        entradas = nodo[2]
        if nombre == "main":
            self.analizar(nodo[2], alcance)
            self.main = True
            return
        if nombre not in self.tabla_simbolos:
            self.tabla_simbolos[nombre] = {'tipo': 'procedimiento', 'valor': self.extraer_sentencias(nodo), 'entradas': entradas}
            print(f"Procedimiento '{nombre}' declarado.")
        else:
            error = (f"Error semántico: el procedimiento '{nombre}' ya ha sido declarado.")
            errores.append(error)
            self.analisis_fallido()
            return
        
    def analizar_invocacion_proc(self, nodo, alcance):
        nombre = nodo[1]
        if len(nodo) <= 2:
            entradas = None
        else:
            entradas = nodo[2]
        if nombre not in self.tabla_simbolos:
            error = (f"Error semántico: el procedimiento '{nombre}' no ha sido declarado.")
            errores.append(error)
            self.analisis_fallido()
            return
        elif self.tabla_simbolos[nombre]['tipo'] != 'procedimiento':
                error = (f"Error semántico: el nombre '{nombre}' no es un procedimiento.")
                errores.append(error)
                self.analisis_fallido()
                return
        else:
            if entradas is None:
                sentencias = self.tabla_simbolos[nombre]['valor']
                for i in range(len(sentencias)):
                    sentencia = sentencias[i]
                    self.analizar(sentencia, nombre)
                print(f"Invocado el procedimiento '{nombre}'.")
            elif len(entradas) == len(self.tabla_simbolos[nombre]['entradas']):

                for j in range(len(entradas)):
                    entrada = self.obtener_valor(entradas[j], alcance)
                    if isinstance(entrada,int):
                        nodo_variable = ('def_variable', self.tabla_simbolos[nombre]['entradas'][j], ('number',entrada))
                        self.analizar(nodo_variable, nombre)
                    else:
                        nodo_variable = ('def_variable', self.tabla_simbolos[nombre]['entradas'][j], ('booleano',entrada))
                        self.analizar(nodo_variable, nombre)

                sentencias = self.tabla_simbolos[nombre]['valor']

                for i in range(len(sentencias)):
                    sentencia = sentencias[i]
                    self.analizar(sentencia, nombre)
                print(f"Invocado el procedimiento '{nombre}'.")

                for j in range(len(entradas)):
                    variable = self.tabla_simbolos[nombre]['entradas'][j]
                    del self.tabla_simbolos[variable]

            else:
                error = (f"Error semántico: el número de argumentos no coincide con el procedimiento '{nombre}'.")
                errores.append(error)
                self.analisis_fallido()
                return



    def generar_tabla_simbolos(self, tabla_simbolos):
        # Crear una imagen temporal para obtener las dimensiones del texto
        img_temp = Image.new('RGB', (1, 1))
        draw_temp = ImageDraw.Draw(img_temp)

        # Definir una fuente
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        # Calcular el ancho máximo de las columnas "Valor", "Entradas" y "Alcance"
        max_valor_width = max(draw_temp.textbbox((0, 0), str(atributos['valor']), font=font)[2] for atributos in tabla_simbolos.values())
        max_entradas_width = max(draw_temp.textbbox((0, 0), str(atributos.get('entradas', '')), font=font)[2] for atributos in tabla_simbolos.values())
        max_alcance_width = max(draw_temp.textbbox((0, 0), str(atributos.get('alcance', 'global')), font=font)[2] for atributos in tabla_simbolos.values())

        # Anchos de las columnas (ajustar dinámicamente los de las columnas Valor, Entradas y Alcance)
        col_widths = [100, 120, max(120, max_valor_width + 20), max(120, max_entradas_width + 20), max(120, max_alcance_width + 20)]  # Ancho de cada columna
        img_width = sum(col_widths) + 40  # Sumar los anchos de todas las columnas más un margen
        img_height = 100 + len(tabla_simbolos) * 40  # Altura basada en el número de filas
        img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        x_start = 20
        y_start = 20
        row_height = 40

        # Dibujar los encabezados
        encabezados = ['Variable', 'Tipo', 'Valor', 'Entradas', 'Alcance']
        for i, encabezado in enumerate(encabezados):
            x_offset = x_start + sum(col_widths[:i])  # Ajuste horizontal basado en la columna
            draw.text((x_offset + 10, y_start + 10), encabezado, font=font, fill=(0, 0, 0))

        # Dibujar las filas de la tabla
        for idx, (variable, atributos) in enumerate(tabla_simbolos.items()):
            y_offset = y_start + (idx + 1) * row_height
            # Dibujar las celdas de la fila
            draw.text((x_start + 10, y_offset + 10), variable, font=font, fill=(0, 0, 0))
            draw.text((x_start + col_widths[0] + 10, y_offset + 10), atributos['tipo'], font=font, fill=(0, 0, 0))
            draw.text((x_start + col_widths[0] + col_widths[1] + 10, y_offset + 10), str(atributos['valor']), font=font, fill=(0, 0, 0))
            draw.text((x_start + col_widths[0] + col_widths[1] + col_widths[2] + 10, y_offset + 10), str(atributos.get('entradas', '')), font=font, fill=(0, 0, 0))
            draw.text((x_start + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3] + 10, y_offset + 10), str(atributos.get('alcance', 'global')), font=font, fill=(0, 0, 0))

        # Dibujar las líneas de la tabla
        num_rows = len(tabla_simbolos) + 1  # Número de filas (incluye encabezados)
        total_height = y_start + num_rows * row_height

        # Dibujar líneas horizontales
        for i in range(num_rows + 1):  # +1 para la línea de la última fila
            y_pos = y_start + i * row_height
            draw.line([(x_start, y_pos), (x_start + sum(col_widths), y_pos)], fill=(0, 0, 0), width=2)

        # Dibujar líneas verticales (incluso la última de la derecha)
        for i in range(len(col_widths) + 1):  # +1 para la última línea vertical
            x_pos = x_start + sum(col_widths[:i])
            draw.line([(x_pos, y_start), (x_pos, total_height)], fill=(0, 0, 0), width=2)

        # Guardar la imagen
        img.save('tabla_simbolos.png')




# Ejemplo de uso en integración con el árbol sintáctico de sintactico.py

if __name__ == "__main__":
    from sintactico import parser

    data = '''
    // Programa de Prueba
    Proc linea1()
        [
            //Define variable local
            Def(varLocal1, 1);
            PosY varLocal1;
        ];
    End;

    Proc posiciona(valorX, valorY)
        [
            PosX valorX;
            PosY valorY;
        ];
    End;

    Proc impCruz(varx, vary)
        [
            Down;
            Pos(varx,vary);
            For var1(1 to 11) Loop
                [PosY 6;
                ContinueRight 9;]
            End Loop;
            Up; 
            PosX Substr(varx, 6);
            PosY Substr(vary, 5);
            Down;
            For var2(1 to 5) Loop
                [PosY 5;
                ContinueRight 9;]
            End Loop;
            Up;
            Beginning;
        ];
    End;
     //comentario
    Proc main()
        [
            // Define variable global
            Def(varGlobal1, 1);
            //Llama al procedimiento linea1
            linea1();
            //Llama al procedimiento posiciona
            posiciona(1,1);
            //El color es 1
            UseColor varGlobal1;
            //Llama al procedimiento para dibujar una Cruz
            impCruz(5,5);
        ];
    End;

    '''
    

    # Parsear el código para generar el árbol sintáctico (AST)
    arbol_sintactico = parser.parse(data)
    
    print("Árbol Sintáctico Generado:", arbol_sintactico)

    # Crear y ejecutar el analizador semántico
    analizador = AnalizadorSemantico(arbol_sintactico)
    analizador.analizar(arbol_sintactico)
   
    #print("Análisis semántico completado correctamente")
    print("Tabla de Símbolos:", analizador.tabla_simbolos)
   