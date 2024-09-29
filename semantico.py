from lexico import errores
import random

class AnalizadorSemantico:
    def __init__(self):
        # Esta tabla de símbolos almacenará las variables declaradas, sus tipos y valores
        self.tabla_simbolos = {}

    def analizar(self, nodo):
        """
        Analiza recursivamente el nodo del árbol sintáctico y realiza las comprobaciones semánticas.
        """
        if isinstance(nodo, tuple):
            tipo_nodo = nodo[0]

            # Analizar declaraciones de variables
            if tipo_nodo == 'def_variable':
                self.analizar_declaracion_variable(nodo)

            # Analizar expresiones como PUT, ADD, operaciones, etc.
            elif tipo_nodo == 'put_variable':
                self.analizar_uso_variable(nodo[1], nodo[2][1])

            elif tipo_nodo == 'add_variable_uno':
                self.analizar_operacion_add(nodo[1])

            elif tipo_nodo == 'add_variable_dos':
                self.analizar_operacion_add(nodo[1], nodo[2][1])

            elif tipo_nodo == 'continue_up' or tipo_nodo == 'continue_down' or tipo_nodo == 'continue_left' or tipo_nodo == 'continue_right':
                if len(nodo[1]) > 2:
                    mov = self.verificar_operacion(nodo[1])
                    print(f"Mover lapicero con {tipo_nodo} por {mov} unidades.")
                else:
                    self.verificar_entero(nodo[1][1])
                    print(f"Mover lapicero hacia {tipo_nodo} por {nodo[1][1]} unidades.")

            elif tipo_nodo == 'pos':
                self.analizar_pos(nodo)

            elif tipo_nodo == 'posx' or tipo_nodo == 'posy':
                self.analizar_pos_xy(nodo)

            elif tipo_nodo == 'use_color':
                self.verificar_entero(nodo[1][1])
                valor = self.obtener_valor(nodo[1])
                if valor != 1 and valor != 2:
                    error = (f"Error semántico: el valor de UseColor debe ser 1 o 2, se obtuvo {valor}.")
                    errores.append(error)
                    raise Exception(error)
                else: 
                    print(f"Usar color {valor}.")
            
            elif tipo_nodo == 'down':
                print("Mover lapicero hacia abajo.")

            elif tipo_nodo == 'up':
                print("Mover lapicero hacia arriba.")

            elif tipo_nodo == 'beginning':
                print("Mover lapicero a [1,1].")

            # Analizar estructuras como bucles (loops), case, etc.
            elif tipo_nodo == 'for_loop':
                self.analizar_for(nodo)
            
            elif tipo_nodo == 'case':
                self.analizar_case(nodo)
                return
            
            elif tipo_nodo == 'for':
                self.analizar_for(nodo)
                return

            elif tipo_nodo == 'equal':
                self.analizar_equal(nodo)

            elif tipo_nodo == 'and':
                self.analizar_and(nodo)

            elif tipo_nodo == 'or':
                self.analizar_or(nodo)

            elif tipo_nodo == 'greater':
                self.analizar_greater(nodo)

            elif tipo_nodo == 'smaller':
                self.analizar_smaller(nodo)

            elif tipo_nodo == 'substract':
                self.analizar_substract(nodo)

            elif tipo_nodo == 'random':
                self.analizar_random(nodo)

            elif tipo_nodo == 'mult':
                self.analizar_mult(nodo)

            elif tipo_nodo == 'div':
                self.analizar_div(nodo)

            elif tipo_nodo == 'sum':
                self.analizar_sum(nodo)
            
            # Si el nodo contiene más subnodos (sentencias), procesarlos también
            for subnodo in nodo[1:]:
                self.analizar(subnodo)

            # Manejar otros tipos de sentencias aquí...

    def analizar_declaracion_variable(self, nodo):
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
            raise Exception(error)
            
        # Verificar si la variable ya fue declarada
        if nombre_variable in self.tabla_simbolos:
            error = (f"Error semántico: la variable '{nombre_variable}' ya fue declarada.")
            errores.append(error)
            raise Exception(error)
        
        # Agregar la variable a la tabla de símbolos
        self.tabla_simbolos[nombre_variable] = {'tipo': tipo_variable, 'valor': valor_variable}
        print(f"Declarada la variable '{nombre_variable}' como '{tipo_variable}' con valor {valor_variable}.")

    def analizar_uso_variable(self, nombre_variable, nuevo_valor=None):
        """
        Verifica si la variable ha sido declarada antes de su uso y valida el tipo de la variable.
        """
        if nombre_variable not in self.tabla_simbolos:
            error = (f"Error semántico: la variable '{nombre_variable}' se usa antes de ser declarada.")
            errores.append(error)
            raise Exception(error)
        
        # Obtener el tipo y el valor actual de la variable
        tipo_actual = self.tabla_simbolos[nombre_variable]['tipo']
        valor_actual = self.tabla_simbolos[nombre_variable]['valor']
        
        # Imprimir el valor actual de la variable
        print(f"Variable '{nombre_variable}' está siendo usada correctamente. Valor actual: {valor_actual}.")

        # Si hay un nuevo valor proporcionado, verificar su tipo
        if nuevo_valor is not None:
            nuevo_tipo = 'entero' if isinstance(nuevo_valor, int) else 'booleano' if nuevo_valor in ["TRUE", "FALSE"] else None
            
            if nuevo_tipo is None:
                error = (f"Error semántico: el nuevo valor '{nuevo_valor}' no es un tipo válido (se esperaba entero o booleano).")
                errores.append(error)
                raise Exception(error)
            
            # Verificar la consistencia de tipos
            if nuevo_tipo != tipo_actual:
                error = (f"Error semántico: no se puede asignar el valor '{nuevo_valor}' de tipo '{nuevo_tipo}' a la variable '{nombre_variable}' que es de tipo '{tipo_actual}'.")
                errores.append(error)
                raise Exception(error)

            # Si el tipo es correcto, actualiza el valor
            self.tabla_simbolos[nombre_variable]['valor'] = nuevo_valor
            print(f"Valor de la variable '{nombre_variable}' actualizado a {nuevo_valor}.")
    
    def analizar_operacion_add(self, nombre_variable, valor_b=1):
        """
        Verifica que los valores en la operación Add sean enteros,
        realiza la suma con el valor de la variable y actualiza la tabla de símbolos.
        """
        # Verificar que el primer operando sea una variable y obtener su valor
        if nombre_variable not in self.tabla_simbolos:
            error = (f"Error semántico: la variable '{nombre_variable}' no ha sido declarada.")
            errores.append(error)
            raise Exception(error)
        
        valor_a_sumar = self.tabla_simbolos[nombre_variable]['valor']
        tipo_a = self.tabla_simbolos[nombre_variable]['tipo']
        
        # Determinar el valor del segundo operando
        if isinstance(valor_b, str):  # Si es una variable
            if valor_b == 'TRUE' or valor_b == 'FALSE':
                error = (f"Error semántico: no se puede sumar un valor booleano.")
                errores.append(error)
                raise Exception(error)
            
            elif valor_b not in self.tabla_simbolos:
                error = (f"Error semántico: la variable '{valor_b}' no ha sido declarada.")
                errores.append(error)
                raise Exception(error)
            
            valor_b_sumar = self.tabla_simbolos[valor_b]['valor']
            tipo_b = self.tabla_simbolos[valor_b]['tipo']
            
            # Verificar que ambos tipos sean enteros
            if tipo_a != 'entero' or tipo_b != 'entero':
                error = (f"Error semántico: las variables deben ser de tipo entero. '{nombre_variable}' es de tipo '{tipo_a}' y '{valor_b}' es de tipo '{tipo_b}'.")
                errores.append(error)
                raise Exception(error)
        else:  # Si es un número
            valor_b_sumar = valor_b  # Asumimos que ya es un entero
            if not isinstance(valor_b_sumar, int):
                error = (f"Error semántico: el valor a sumar debe ser un entero. Se recibió: '{valor_b_sumar}'.")
                errores.append(error)
                raise Exception(error)
        
        # Verificar que el tipo de valor_a_sumar sea entero
        if tipo_a != 'entero':
            error = (f"Error semántico: no se puede sumar a la variable '{nombre_variable}' de tipo '{tipo_a}'.")
            errores.append(error)
            raise Exception(error)

        # Realizar la suma
        nuevo_valor = valor_a_sumar + valor_b_sumar
        
        # Actualizar el valor en la tabla de símbolos
        self.tabla_simbolos[nombre_variable]['valor'] = nuevo_valor
        print(f"Variable '{nombre_variable}' actualizada. Nuevo valor: {nuevo_valor}.")

    def verificar_entero(self, valor):
        if isinstance(valor, str):  # Si es una variable
            if valor not in self.tabla_simbolos:
                error = (f"Error semántico: la variable '{valor}' no ha sido declarada.")
                errores.append(error)
                raise Exception(error)
            tipo_variable = self.tabla_simbolos[valor]['tipo']
            if tipo_variable != 'entero':
                error = (f"Error semántico: la variable '{valor}' debe ser de tipo entero. Es de tipo '{tipo_variable}'.")
                errores.append(error)
                raise Exception(error)
            
        else:  # Se asume que el valor es un número
            if not isinstance(valor, int):
                error = (f"Error semántico: se esperaba un entero, se recibió: '{valor}'.")
                errores.append(error)
                raise Exception(error)

     # Función para verificar si el valor es una variable o un número
    def verificar_booleano(self, valor):
        if isinstance(valor, str):  # Si es una variable
            if valor == 'TRUE':
                return True
            elif valor == 'FALSE':
                    return False
            elif valor not in self.tabla_simbolos:
                error = (f"Error semántico: la variable '{valor}' no ha sido declarada.")
                errores.append(error)
                raise Exception(error)
            else:
                booleano = self.tabla_simbolos[valor]['valor']
                if isinstance(booleano, bool):
                    return booleano
                else:
                    error = (f"Error semántico: la variable '{valor}' debe ser de tipo booleano.")
                    errores.append(error)
                    raise Exception(error)
                
    def verificar_operacion(self, node):
        # Si el nodo es un número, lo devolvemos
        if node[0] == 'number':
            return node[1]
        
        # Si el nodo es una operación (multiplicación, división, suma o resta)
        operator = node[0]
        left = self.obtener_valor(node[1])  # Evalúa el operando izquierdo
        right = self.obtener_valor(node[2])  # Evalúa el operando derecho

        # Verificar que ambos operandos sean enteros
        if not isinstance(left, int) or not isinstance(right, int):
            raise Exception(f"Error: Los operandos deben ser enteros. Recibido: {left} y {right}")
        
        result = 0
        
        # Realiza la operación en función del operador
        if operator == '*':
            result = left * right
        elif operator == '/':
            # Aseguramos que no se divida por cero
            if right == 0:
                raise ZeroDivisionError("Error: División por cero")
            result = round(left / right)
        elif operator == '+':
            result = left + right
        elif operator == '-':
            result = left - right
        
        return result
        

    def analizar_pos(self, nodo):
        """
        Verifica que ambos valores en la operación Pos sean enteros.
        """

        valor_a = 0
        valor_b = 0

        if len(nodo[1]) > 2:
            valor_a = self.verificar_operacion(nodo[1])
            if len(nodo[2]) > 2:
                valor_b = self.verificar_operacion(nodo[2])
            else:
                valor_b = nodo[2][1]
        elif len(nodo[2]) > 2:
            valor_b = self.verificar_operacion(nodo[2])
            if len(nodo[1]) > 2:
                valor_a = self.verificar_operacion(nodo[1])
            else:
                valor_b = nodo[2][1]
        else:
            valor_a = self.obtener_valor(nodo[1])  # Primer argumento
            valor_b = self.obtener_valor(nodo[2])  # Segundo argumento            print(f"Resultado de {left} - {right} = {result}")

            # Verificar ambos valores
            self.verificar_entero(valor_a)
            self.verificar_entero(valor_b)

        print(f"Posicionar lapicero en [{valor_a}, {valor_b}].")

    def analizar_pos_xy(self, nodo):
        """
        Verifica que ambos valores en la operación Pos sean enteros.
        """

        valor_a = 0 
        print(nodo)

        if len(nodo[1]) > 2:
            valor_a = self.verificar_operacion(nodo[1])
        else:
            valor_a = self.obtener_valor(nodo[1])  # Primer argumento

            # Verificar ambos valores
            self.verificar_entero(valor_a)

        print(f"Posicionar usando {nodo[0]} en {valor_a}.")

    def analizar_bucle(self, nodo):
        """
        Realiza las comprobaciones para las variables de control de un bucle y asegura que los límites del bucle sean correctos.
        """
        var_bucle = nodo[2]
        self.analizar_uso_variable(var_bucle)

        inicio_bucle = nodo[4]
        fin_bucle = nodo[6]

        if not isinstance(inicio_bucle, int) or not isinstance(fin_bucle, int):
            error = (f"Error semántico: los límites del bucle deben ser enteros, se obtuvo {inicio_bucle} a {fin_bucle}.")
            errores.append(error)
            raise Exception(error)

        if inicio_bucle >= fin_bucle:
            error = (f"Error semántico: el valor inicial del bucle ({inicio_bucle}) debe ser menor al valor final ({fin_bucle}).")
            errores.append(error)
            raise Exception(error)

        print(f"Bucle válido desde {inicio_bucle} hasta {fin_bucle} con la variable '{var_bucle}'.")

    def analizar_case(self, nodo):
        
        nombre_variable = nodo[1]
        self.verificar_entero(nombre_variable)
        valor_actual = self.tabla_simbolos[nombre_variable]['valor']

        casos = self.buscar_todos_when_cases(nodo)
        for i in range(len(casos)):
            caso = casos[i][1][1]
            if not isinstance(caso, int):
                error = (f"Error semántico: el caso debe de ser entero, se obtuvo {caso}.")
                errores.append(error)
                raise Exception(error)
            else:
                if caso == valor_actual:
                    print(f"El caso {caso} se cumple.")
                    sentencia = self.obtener_sentencias_a_ejecutar(casos[i], nodo)
                    self.analizar(sentencia)
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
    
    def analizar_for(self, nodo):
        var = nodo[1]
        indice_menor = nodo[2][1]
        indice_mayor = nodo[3][1]
        if var not in self.tabla_simbolos: 
            self.tabla_simbolos[var] = {'tipo': "entero", 'valor': indice_menor}
            while indice_menor < indice_mayor:
                for i in range(len(self.extraer_sentencias(nodo))):
                    sentencia = self.extraer_sentencias(nodo)[i]
                    print("sentencia: ", sentencia)
                    self.analizar(sentencia)
                indice_menor += 1
                self.tabla_simbolos[var]['valor'] = indice_menor
        else:
            error = (f"Error semántico: la variable '{var}' ya ha sido declarada.")
            errores.append(error)
            raise Exception(error)
        
        
            


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

    def analizar_expresion(self, nodo_expresion):
        """UseColor 1
        Comprueba si expresiones como ADD, PUT y otras están siendo usadas con variables declaradas.
        """
        if nodo_expresion[0] == 'add_variable':
            nombre_variable = nodo_expresion[2]
            self.analizar_uso_variable(nombre_variable)
            print(f"Analizada la operación ADD para la variable '{nombre_variable}'.")
    
    # Función para obtener el valor de un operando, ya sea variable o número literal
    def obtener_valor(self,operando):
        if isinstance(operando, int):
            return operando  
        elif isinstance(operando, tuple) and operando[0] == 'variable':  # Si es una variable
            if operando[1] in self.tabla_simbolos:
                return self.tabla_simbolos[operando[1]]['valor']
            else:
                error = (f"Error: la variable '{operando}' no está definida.")
                errores.append(error)
                raise Exception(error)
        elif isinstance(operando, tuple) and operando[0] == 'number' or operando[0] == 'logico':  
            return operando[1]  # Retorna el valor numérico
        else:
            error = ("Error: operando no válido.")
            errores.append(error)
            raise Exception(error)

    def analizar_equal(self, nodo):
        # nodo: ('equal', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1)
        valor2 = self.obtener_valor(operando2)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor1)
        self.verificar_entero(valor2)

        # Comparar los valores y devolver el resultado
        resultado = valor1 == valor2
        print(f"Resultado de la comparación {valor1} == {valor2}: {resultado}")
        return resultado
    
    def analizar_and(self, nodo):
        # nodo: ('equal', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1)
        valor2 = self.obtener_valor(operando2)

        booleano1 = self.verificar_booleano(valor1)
        booleano2 = self.verificar_booleano(valor2)

        # Comparar los valores y devolver el resultado
        resultado = booleano1 and booleano2
        print(f"Resultado del and {booleano1} and {booleano2}: {resultado}")
        return resultado
    
    def analizar_or(self, nodo):
        # nodo: ('equal', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1)
        valor2 = self.obtener_valor(operando2)

        # Verificar que ambos valores sean enteros
        booleano1 = self.verificar_booleano(valor1)
        booleano2 = self.verificar_booleano(valor2)

        # Comparar los valores y devolver el resultado
        resultado = booleano1 or booleano2
        print(f"Resultado del or {booleano1} or {booleano2}: {resultado}")
        return resultado
    
    def analizar_greater(self, nodo):
        # nodo: ('equal', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1)
        valor2 = self.obtener_valor(operando2)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor1)
        self.verificar_entero(valor2)

        # Comparar los valores y devolver el resultado
        resultado = valor1 > valor2
        print(f"Resultado de la comparación {valor1} > {valor2}: {resultado}")
        return resultado

    def analizar_smaller(self, nodo):
        # nodo: ('equal', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1)
        valor2 = self.obtener_valor(operando2)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor1)
        self.verificar_entero(valor2)

        # Comparar los valores y devolver el resultado
        resultado = valor1 < valor2
        print(f"Resultado de la comparación {valor1} < {valor2}: {resultado}")
        return resultado

    def analizar_substract(self, nodo):
        # nodo: ('substract', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1)
        valor2 = self.obtener_valor(operando2)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor1)
        self.verificar_entero(valor2)

        # Comparar los valores y devolver el resultado
        resultado = valor1 - valor2
        print(f"Resultado de la resta {valor1} - {valor2} = {resultado}")
        return resultado

    def analizar_random(self, nodo):
        # nodo: ('random', operand1)
        operando = nodo[1]

        # Obtener valores de ambos operandos
        valor = self.obtener_valor(operando)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor)

        # Comparar los valores y devolver el resultado
        resultado = random.randint(0, valor)
        print(f"Resultado de numero random es  {valor} = {resultado}")
        return resultado

    def analizar_mult(self, nodo):
        # nodo: ('mult', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1)
        valor2 = self.obtener_valor(operando2)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor1)
        self.verificar_entero(valor2)

        # Comparar los valores y devolver el resultado
        resultado = valor1 * valor2
        print(f"Resultado de la multiplicacion {valor1} * {valor2} = {resultado}")
        return resultado

    def analizar_div(self, nodo):
        # nodo: ('div', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1)
        valor2 = self.obtener_valor(operando2)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor1)
        self.verificar_entero(valor2)

        # Comparar los valores y devolver el resultado
        if valor2 == 0:
            error = ("Error: operando 2 no válido.")
            errores.append(error)
            raise Exception(error)
        else:
            resultado = valor1 / valor2
            print(f"Resultado de la division {valor1} / {valor2} = {resultado}")
        return resultado

    def analizar_sum(self, nodo):
        # nodo: ('sum', operand1, operand2)
        operando1 = nodo[1]
        operando2 = nodo[2]

        # Obtener valores de ambos operandos
        valor1 = self.obtener_valor(operando1)
        valor2 = self.obtener_valor(operando2)

        # Verificar que ambos valores sean enteros
        self.verificar_entero(valor1)
        self.verificar_entero(valor2)

        # Comparar los valores y devolver el resultado
        resultado = valor1 + valor2
        print(f"Resultado de la suma {valor1} + {valor2} = {resultado}")
        return resultado

    def analizar_condicional(self, nodo_condicional):
        """
        Realiza las comprobaciones para condicionales como IF, WHILE, REPEAT-UNTIL, etc.
        """
        # Realizar las comprobaciones adecuadas para el nodo de condicional
        pass

# Ejemplo de uso en integración con el árbol sintáctico de sintactico.py
if __name__ == "__main__":
    from sintactico import parser

    data = '''
    //comentario
    Def(var2,1);
    For var1(1 to 5) Loop
        [Add(var2,var1);
        ContinueRight 9;]
    End Loop;
    '''
    

    # Parsear el código para generar el árbol sintáctico (AST)
    arbol_sintactico = parser.parse(data)
    
    print("Árbol Sintáctico Generado:", arbol_sintactico)

    # Crear y ejecutar el analizador semántico
    analizador = AnalizadorSemantico()
    analizador.analizar(arbol_sintactico)
   
    #print("Análisis semántico completado correctamente")
    print("Tabla de Símbolos:", analizador.tabla_simbolos)