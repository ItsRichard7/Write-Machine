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
            print(f"Analizando nodo: {tipo_nodo}")

            # Analizar declaraciones de variables
            if tipo_nodo == 'def_variable':
                self.analizar_declaracion_variable(nodo)

            # Analizar expresiones como PUT, ADD, operaciones, etc.
            elif tipo_nodo == 'put_variable':
                self.analizar_uso_variable(nodo[2])

            elif tipo_nodo == 'add_variable':
                self.analizar_uso_variable(nodo[2])

            # Analizar estructuras como bucles (loops), case, etc.
            elif tipo_nodo == 'for_loop':
                self.analizar_bucle(nodo)

            # Si el nodo contiene más subnodos (sentencias), procesarlos también
            for subnodo in nodo[1:]:
                self.analizar(subnodo)

            # Manejar otros tipos de sentencias aquí...

    def analizar_declaracion_variable(self, nodo):
        """
        Agrega o actualiza la variable en la tabla de símbolos, validando su tipo.
        """
        nombre_variable = nodo[1]
        valor_variable = nodo[2][1]  # Suponiendo que el valor está en nodo[2]

        # Determinar el tipo de la variable basada en el valor
        tipo_variable = 'entero' if isinstance(valor_variable, int) else 'booleano' if valor_variable in ["TRUE", "FALSE"] else None

        if tipo_variable is None:
            raise Exception(f"Error semántico: el valor '{valor_variable}' no es un tipo válido (se esperaba entero o booleano).")

        print(f"Analizando declaración de variable: {nombre_variable} con valor {valor_variable} y tipo {tipo_variable}")

        # Validar si la variable ya existe y si el tipo coincide
        if nombre_variable in self.tabla_simbolos:
            tipo_existente = self.tabla_simbolos[nombre_variable]['tipo']
            if tipo_existente != tipo_variable:
                raise Exception(f"Error semántico: no se puede redeclarar la variable '{nombre_variable}' como '{tipo_variable}' porque ya fue declarada como '{tipo_existente}'.")
        
        # Actualizar o agregar la variable con su tipo y valor
        self.tabla_simbolos[nombre_variable] = {'tipo': tipo_variable, 'valor': valor_variable}
        
        print(f"Variable '{nombre_variable}' actualizada/declarada con valor {valor_variable} y tipo {tipo_variable}.")


    def analizar_uso_variable(self, nombre_variable):
        """
        Verifica si la variable ha sido declarada antes de su uso.
        """
        if nombre_variable not in self.tabla_simbolos:
            raise Exception(f"Error semántico: la variable '{nombre_variable}' se usa antes de ser declarada.")
        valor_actual = self.tabla_simbolos[nombre_variable]['valor']
        print(f"Variable '{nombre_variable}' está siendo usada correctamente. Valor actual: {valor_actual}.")

    def analizar_bucle(self, nodo):
        """
        Realiza las comprobaciones para las variables de control de un bucle y asegura que los límites del bucle sean correctos.
        """
        var_bucle = nodo[2]
        self.analizar_uso_variable(var_bucle)

        inicio_bucle = nodo[4]
        fin_bucle = nodo[6]

        if not isinstance(inicio_bucle, int) or not isinstance(fin_bucle, int):
            raise Exception(
                f"Error semántico: los límites del bucle deben ser enteros, se obtuvo {inicio_bucle} a {fin_bucle}.")

        if inicio_bucle >= fin_bucle:
            raise Exception(
                f"Error semántico: el valor inicial del bucle ({inicio_bucle}) debe ser menor al valor final ({fin_bucle}).")

        print(f"Bucle válido desde {inicio_bucle} hasta {fin_bucle} con la variable '{var_bucle}'.")

    def analizar_expresion(self, nodo_expresion):
        """
        Comprueba si expresiones como ADD, PUT y otras están siendo usadas con variables declaradas.
        """
        if nodo_expresion[0] == 'add_variable':
            nombre_variable = nodo_expresion[2]
            self.analizar_uso_variable(nombre_variable)
            print(f"Analizada la operación ADD para la variable '{nombre_variable}'.")

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
    Def(variable1, 5);
    Def(variable1, 9); 
    ContinueUp 10;
    '''

    # Parsear el código para generar el árbol sintáctico (AST)
    arbol_sintactico = parser.parse(data)
    print("Árbol Sintáctico Generado:", arbol_sintactico)

    # Crear y ejecutar el analizador semántico
    analizador = AnalizadorSemantico()
    analizador.analizar(arbol_sintactico)
    print("Análisis semántico completado correctamente")
    print("Tabla de Símbolos:", analizador.tabla_simbolos)
