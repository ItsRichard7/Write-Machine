from llvmlite import ir, binding

class CodeGenerator:
    def __init__(self):
        # Crear el módulo LLVM
        self.module = ir.Module(name="modulo_principal")
        
        # Inicializar el target triple y data layout
        binding.initialize()
        binding.initialize_native_target()
        binding.initialize_native_asmprinter()  # Necesario para la impresión ASM
        
        target = binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        self.module.triple = target.triple
        self.module.data_layout = target_machine.target_data

        # Contexto para generar código
        self.builder = None
        self.funciones = {}
        self.variables = {}

    def generar_codigo(self, ast):
        # Iniciar el recorrido del AST
        self.visitar(ast)

    def visitar(self, nodo):
        tipo = nodo[0]

        if tipo == 'sentencias':
            for sentencia in nodo[1:]:
                self.visitar(sentencia)
        elif tipo == 'proc':
            self.generar_procedimiento(nodo)
        elif tipo == 'def_variable':
            self.definir_variable(nodo)
        elif tipo == 'put_variable':
            self.put_variable(nodo)
        elif tipo == 'invocacion_proc':
            self.invocar_procedimiento(nodo)
        elif tipo == 'for_loop':
            self.generar_for_loop(nodo)
        elif tipo == 'case':
            self.generar_case(nodo)
        elif tipo == 'repeat_until':
            self.generar_repeat_until(nodo)
        elif tipo == 'while':
            self.generar_while(nodo)
        elif tipo == 'add_variable_dos' and isinstance(nodo[2], int):
            self.add_variable_dos(nodo)
        elif tipo == 'add_variable_dos' and isinstance(nodo[2], str):
            self.add_variable_dos_var(nodo)
        elif tipo == 'add_variable_uno':
            self.add_variable_uno(nodo)
        elif tipo == 'posx':
            self.generar_posx(nodo)
        elif tipo == 'posy':
            self.generar_posy(nodo)
        elif tipo == 'equal':
            self.generar_equal(nodo)
        elif tipo == 'and':
            self.generar_and(nodo)
        else:
            print(f"Tipo de nodo no manejado: {tipo}")


    def generar_procedimiento(self, nodo):
        nombre = nodo[1]
        cuerpo = nodo[2] if len(nodo) > 3 else nodo[2]

        # Crear la función LLVM sin argumentos
        tipo_funcion = ir.FunctionType(ir.VoidType(), [])
        funcion = ir.Function(self.module, tipo_funcion, name=nombre)
        self.funciones[nombre] = funcion

        # Crear un bloque básico para el cuerpo de la función
        bloque = funcion.append_basic_block(name="entrada")
        self.builder = ir.IRBuilder(bloque)

        # Visitar el cuerpo de la función
        self.visitar(cuerpo)

        # Terminar la función
        self.builder.ret_void()

    def definir_variable(self, nodo):
        # Nodo tiene la forma ('def_variable', 'nombre', 'valor')
        nombre = nodo[1]
        valor = nodo[2]

        # Crear la variable en el ámbito actual
        variable = self.builder.alloca(ir.IntType(1) if isinstance(valor, tuple) and valor[0] == 'logico' else ir.IntType(32), name=nombre)

        # Si es un valor lógico, convertirlo a i1
        if isinstance(valor, tuple) and valor[0] == 'logico':
            valor_inicial = ir.Constant(ir.IntType(1), 1 if valor[1] == 'TRUE' else 0)
        else:
            valor_inicial = ir.Constant(ir.IntType(32), valor)

        # Almacenar el valor en la variable
        self.builder.store(valor_inicial, variable)

        # Registrar la variable
        self.variables[nombre] = variable


    def put_variable(self, nodo):
        # Nodo tiene la forma ('put_variable', 'nombre_variable', nuevo_valor)
        nombre_var = nodo[1]
        nuevo_valor = nodo[2]
        
        # Buscar la variable en la tabla de variables
        variable = self.variables.get(nombre_var)
        if variable:
            # Almacenar el nuevo valor en la variable
            self.builder.store(ir.Constant(ir.IntType(32), nuevo_valor), variable)
            print(f"Cambiando el valor de {nombre_var} a {nuevo_valor}")
        else:
            print(f"Variable {nombre_var} no encontrada.")

    def invocar_procedimiento(self, nodo):
        nombre_proc = nodo[1]
        argumentos = nodo[2] if len(nodo) > 2 else []

        # Obtener los valores de los argumentos
        valores_args = []
        for arg in argumentos:
            if arg[0] == 'number':
                valores_args.append(ir.Constant(ir.IntType(32), arg[1]))
            elif arg[0] in self.variables:
                variable = self.variables[arg[0]]
                valor_arg = self.builder.load(variable, name=f"{arg[0]}_temp")
                valores_args.append(valor_arg)

        # Llamar a la función con los argumentos
        funcion = self.funciones.get(nombre_proc)
        if funcion:
            self.builder.call(funcion, valores_args)
        else:
            print(f"Procedimiento {nombre_proc} no encontrado.")

    def generar_for_loop(self, nodo):
        var_nombre = nodo[1]
        inicio = nodo[2]
        fin = nodo[3]
        cuerpo = nodo[4]

        # Inicializar la variable de control (var1)
        var = self.builder.alloca(ir.IntType(32), name=var_nombre)
        self.builder.store(ir.Constant(ir.IntType(32), inicio), var)
        self.variables[var_nombre] = var

        # Crear bloques para el loop
        cond_bloque = self.builder.append_basic_block("condicion")
        cuerpo_bloque = self.builder.append_basic_block("cuerpo")
        fin_bloque = self.builder.append_basic_block("fin_loop")

        # Saltar al bloque de condición
        self.builder.branch(cond_bloque)
        self.builder.position_at_end(cond_bloque)

        # Cargar la variable y verificar la condición (var <= fin)
        var_valor = self.builder.load(var, name=f"{var_nombre}_temp")
        cond = self.builder.icmp_signed('<', var_valor, ir.Constant(ir.IntType(32), fin))
        self.builder.cbranch(cond, cuerpo_bloque, fin_bloque)

        # Bloque del cuerpo del loop
        self.builder.position_at_end(cuerpo_bloque)
        self.visitar(cuerpo)  # Visitar el cuerpo del bucle

        # Incrementar la variable de control
        incremento = self.builder.add(var_valor, ir.Constant(ir.IntType(32), 1))
        self.builder.store(incremento, var)

        # Saltar de nuevo al bloque de condición
        self.builder.branch(cond_bloque)

        # Posicionar el builder en el bloque de salida
        self.builder.position_at_end(fin_bloque)

    def generar_case(self, nodo):
        # Nodo tiene la forma ('case', 'variable', 'when_cases', 'end_case')
        var_nombre = nodo[1]
        when_cases = nodo[2]

        # Cargar la variable que se va a evaluar
        variable = self.variables.get(var_nombre)
        if not variable:
            print(f"Variable {var_nombre} no encontrada.")
            return

        valor_variable = self.builder.load(variable, name=f"{var_nombre}_valor")

        # Crear el bloque final para después del case
        bloque_final = self.builder.append_basic_block("end_case")

        # Aplanar los 'when_cases' y procesar los 'when_case'
        casos = self.recorrer_when_cases(when_cases)

        # Recorrer los when_case procesados
        for idx, when_case in enumerate(casos):
            valor_case = when_case[1]
            cuerpo = when_case[2]

            # Crear el bloque para este caso
            bloque_caso = self.builder.append_basic_block(f"when_{valor_case}")
            
            # Crear el bloque para continuar si no se cumple la condición
            bloque_siguiente = self.builder.append_basic_block(f"next_{valor_case}")
            
            # Comparar la variable con el valor del case
            condicion = self.builder.icmp_signed('==', valor_variable, ir.Constant(ir.IntType(32), valor_case))
            self.builder.cbranch(condicion, bloque_caso, bloque_siguiente)

            # Posicionar el builder en el bloque del caso actual
            self.builder.position_at_end(bloque_caso)
            self.visitar(cuerpo)  # Visitar las sentencias dentro del when_case

            # Solo agregar branch si el bloque no está ya terminado
            if not self.builder.block.is_terminated:
                self.builder.branch(bloque_final)  # Saltar al bloque final al terminar

            # Posicionar el builder en el bloque siguiente (para el próximo when_case)
            self.builder.position_at_end(bloque_siguiente)

        # Enlazar el último bloque con el bloque final si no está terminado
        if not self.builder.block.is_terminated:
            self.builder.branch(bloque_final)

        # Posicionar el builder en el bloque final
        self.builder.position_at_end(bloque_final)


    def recorrer_when_cases(self, when_cases):
        # Si es un solo 'when_case', procesarlo directamente
        if when_cases[0] == 'when_case':
            return [when_cases]
        
        # Si es un 'when_cases', recorrerlo y procesar todos sus elementos
        casos = []
        for caso in when_cases[1:]:
            if caso[0] == 'when_cases':
                # Recursivamente aplanar los 'when_cases' anidados
                casos.extend(self.recorrer_when_cases(caso))
            else:
                # Añadir el 'when_case' actual
                casos.append(caso)
        
        return casos

    def generar_repeat_until(self, nodo):
        # Nodo tiene la forma ('repeat_until', 'instrucciones', 'condición')
        instrucciones = nodo[1]
        condicion = nodo[2]

        # Crear el bloque de inicio del bucle
        bloque_repeat = self.builder.append_basic_block("repeat_loop")
        bloque_condicion = self.builder.append_basic_block("check_condicion")
        bloque_salida = self.builder.append_basic_block("end_repeat")

        # Saltar al bloque del bucle
        self.builder.branch(bloque_repeat)

        # Posicionar en el bloque del bucle
        self.builder.position_at_end(bloque_repeat)

        # Visitar las instrucciones dentro del repeat
        self.visitar(instrucciones)

        # Saltar al bloque de la condición
        self.builder.branch(bloque_condicion)

        # Posicionar en el bloque de la condición
        self.builder.position_at_end(bloque_condicion)

        # Generar la condición
        var_nombre = condicion[1]
        operador = condicion[0]
        valor_condicion = ir.Constant(ir.IntType(32), 5)  # Por ahora suponemos el valor es 5
        variable = self.variables.get(var_nombre)

        if not variable:
            print(f"Variable {var_nombre} no encontrada.")
            return

        valor_variable = self.builder.load(variable, name=f"{var_nombre}_valor")

        # Dependiendo del operador, generar la comparación
        if operador == '==':
            comparacion = self.builder.icmp_signed('==', valor_variable, valor_condicion)
        elif operador == '>':
            comparacion = self.builder.icmp_signed('>', valor_variable, valor_condicion)
        elif operador == '<':
            comparacion = self.builder.icmp_signed('<', valor_variable, valor_condicion)
        else:
            raise ValueError(f"Operador {operador} no soportado.")

        # Bifurcar condicionalmente según la comparación
        self.builder.cbranch(comparacion, bloque_salida, bloque_repeat)

        # Posicionar en el bloque de salida
        self.builder.position_at_end(bloque_salida)
    
    def generar_while(self, nodo):
        # Nodo tiene la forma ('while', 'condición', 'instrucciones')
        condicion = nodo[1]
        instrucciones = nodo[2]

        # Crear el bloque de la condición y el bloque del cuerpo del while
        bloque_condicion = self.builder.append_basic_block("while_condicion")
        bloque_cuerpo = self.builder.append_basic_block("while_body")
        bloque_salida = self.builder.append_basic_block("end_while")

        # Saltar al bloque de la condición
        self.builder.branch(bloque_condicion)

        # Posicionar en el bloque de la condición
        self.builder.position_at_end(bloque_condicion)

        # Generar la condición
        var_nombre = condicion[1]
        operador = condicion[0]
        valor_condicion = ir.Constant(ir.IntType(32), 10)  # Suponemos que la comparación es con el valor 10
        variable = self.variables.get(var_nombre)

        if not variable:
            print(f"Variable {var_nombre} no encontrada.")
            return

        valor_variable = self.builder.load(variable, name=f"{var_nombre}_valor")

        # Dependiendo del operador, generar la comparación
        if operador == '==':
            comparacion = self.builder.icmp_signed('==', valor_variable, valor_condicion)
        elif operador == '>':
            comparacion = self.builder.icmp_signed('>', valor_variable, valor_condicion)
        elif operador == '<':
            comparacion = self.builder.icmp_signed('<', valor_variable, valor_condicion)
        else:
            raise ValueError(f"Operador {operador} no soportado.")

        # Bifurcar condicionalmente: si la condición es verdadera, vamos al cuerpo, si no, al final
        self.builder.cbranch(comparacion, bloque_cuerpo, bloque_salida)

        # Posicionar en el bloque del cuerpo
        self.builder.position_at_end(bloque_cuerpo)

        # Generar las instrucciones dentro del cuerpo del while
        self.visitar(instrucciones)

        # Al final del cuerpo, saltar de vuelta a la condición
        self.builder.branch(bloque_condicion)

        # Posicionar en el bloque de salida
        self.builder.position_at_end(bloque_salida)    


    def add_variable_dos(self, nodo):
        # Nodo tiene la forma ('add_variable_dos', 'nombre_variable', valor)
        nombre_var = nodo[1]
        valor = nodo[2]
        
        # Cargar el valor actual de la variable
        variable = self.variables.get(nombre_var)
        if variable:
            valor_actual = self.builder.load(variable, name=f"{nombre_var}_actual")
            suma = self.builder.add(valor_actual, ir.Constant(ir.IntType(32), valor))
            self.builder.store(suma, variable)
            print(f"Suma de {valor} a {nombre_var}")
        else:
            print(f"Variable {nombre_var} no encontrada.")

    def add_variable_dos_var(self, nodo):
        # Nodo tiene la forma ('add_variable_dos', 'nombre_variable1', 'nombre_variable2')
        nombre_var1 = nodo[1]
        nombre_var2 = nodo[2]
        
        # Cargar el valor actual de las dos variables
        variable1 = self.variables.get(nombre_var1)
        variable2 = self.variables.get(nombre_var2)
        
        if variable1 and variable2:
            valor_actual1 = self.builder.load(variable1, name=f"{nombre_var1}_actual")
            valor_actual2 = self.builder.load(variable2, name=f"{nombre_var2}_actual")
            suma = self.builder.add(valor_actual1, valor_actual2)
            self.builder.store(suma, variable1)
            print(f"Suma del valor de {nombre_var2} a {nombre_var1}")
        else:
            print(f"Una de las variables no fue encontrada.")
    
    def add_variable_uno(self, nodo):
        # Nodo tiene la forma ('add_variable_uno', 'nombre_variable')
        nombre_var = nodo[1]
        
        # Cargar el valor actual de la variable
        variable = self.variables.get(nombre_var)
        if variable:
            valor_actual = self.builder.load(variable, name=f"{nombre_var}_actual")
            suma = self.builder.add(valor_actual, ir.Constant(ir.IntType(32), 1))
            self.builder.store(suma, variable)
            print(f"Suma de 1 a {nombre_var}")
        else:
            print(f"Variable {nombre_var} no encontrada.")



    def generar_posx(self, nodo):
        valor = nodo[1]
        if isinstance(valor, int):
            print(f"Generando PosX con valor {valor}")
        else:
            variable = self.variables.get(valor)
            if variable:
                valor_posx = self.builder.load(variable, name="posx_temp")
                print(f"Generando PosX con valor de la variable {valor}")
            else:
                print(f"Variable {valor} no encontrada.")

    def generar_posy(self, nodo):
        valor = nodo[1]
        if isinstance(valor, int):
            print(f"Generando PosY con valor {valor}")
        else:
            variable = self.variables.get(valor)
            if variable:
                valor_posy = self.builder.load(variable, name="posy_temp")
                print(f"Generando PosY con valor de la variable {valor}")
            else:
                print(f"Variable {valor} no encontrada.")
    
    def generar_equal(self, nodo):
        # Nodo tiene la forma ('equal', 'op1', 'op2')
        op1 = nodo[1]
        op2 = nodo[2]

        # Obtener el primer operando (variable o constante)
        valor1 = self.builder.load(self.variables[op1], name=f"{op1}_valor") if isinstance(op1, str) else ir.Constant(ir.IntType(32), op1)

        # Obtener el segundo operando (variable, constante o expresión aritmética)
        if isinstance(op2, str):
            valor2 = self.builder.load(self.variables[op2], name=f"{op2}_valor")
        elif isinstance(op2, tuple) and op2[0] == '+':
            # Evaluar la suma de dos constantes
            valor2 = ir.Constant(ir.IntType(32), op2[1] + op2[2])
        else:
            valor2 = ir.Constant(ir.IntType(32), op2)

        # Generar la comparación y retornar el resultado booleano
        return self.builder.icmp_signed('==', valor1, valor2)
    
    def generar_and(self, nodo):
        # Nodo tiene la forma ('and', 'op1', 'op2')
        op1 = nodo[1]
        op2 = nodo[2]

        # Obtener el primer operando (puede ser una variable o un valor lógico)
        if isinstance(op1, str) and op1 in self.variables:
            valor1 = self.builder.load(self.variables[op1], name=f"{op1}_valor")
        elif isinstance(op1, tuple) and op1[0] == 'logico':
            # Si es un valor lógico, convertir a constante LLVM (TRUE -> 1, FALSE -> 0)
            valor1 = ir.Constant(ir.IntType(1), 1 if op1[1] == 'TRUE' else 0)
        else:
            raise ValueError(f"Operando no soportado: {op1}")

        # Si el primer operando es de tipo i32, convertirlo a i1
        if valor1.type != ir.IntType(1):
            valor1 = self.builder.icmp_signed('!=', valor1, ir.Constant(ir.IntType(32), 0))

        # Obtener el segundo operando (puede ser una variable o un valor lógico)
        if isinstance(op2, str) and op2 in self.variables:
            valor2 = self.builder.load(self.variables[op2], name=f"{op2}_valor")
        elif isinstance(op2, tuple) and op2[0] == 'logico':
            # Si es un valor lógico, convertir a constante LLVM (TRUE -> 1, FALSE -> 0)
            valor2 = ir.Constant(ir.IntType(1), 1 if op2[1] == 'TRUE' else 0)
        else:
            raise ValueError(f"Operando no soportado: {op2}")

        # Si el segundo operando es de tipo i32, convertirlo a i1
        if valor2.type != ir.IntType(1):
            valor2 = self.builder.icmp_signed('!=', valor2, ir.Constant(ir.IntType(32), 0))

        # Realizar la operación lógica AND
        resultado = self.builder.and_(valor1, valor2)

        # Almacenar el resultado en una variable
        resultado_and = self.builder.alloca(ir.IntType(1), name="resultado_and")
        self.builder.store(resultado, resultado_and)

        # Retornar la dirección donde se almacenó el resultado
        return resultado_and




# Ejemplo de AST de entrada con un for loop
ast = ('sentencias', ('proc', 'main', ('sentencias', ('def_variable', 'varGlobal1', ('logico', 'TRUE')), ('sentencias', ('and', 'varGlobal1', ('logico', 'TRUE')), ('sentencias', ('and', ('logico', 'TRUE'), ('logico', 'FALSE')))))))




# Crear el generador y generar código
generador = CodeGenerator()
generador.generar_codigo(ast)

# Imprimir el módulo LLVM generado
print(generador.module)

# Opcionalmente: ejecutar el código LLVM usando el motor JIT
modulo_llvm = binding.parse_assembly(str(generador.module))
modulo_llvm.verify()

target_machine = binding.Target.from_default_triple().create_target_machine()

with binding.create_mcjit_compiler(modulo_llvm, target_machine) as ee:
    ee.finalize_object()

    # Llamar a la función main
    if "main" in generador.funciones:
        func_ptr = ee.get_function_address("main")
        import ctypes
        main_fn = ctypes.CFUNCTYPE(None)(func_ptr)
        print("Ejecutando función main...")
        main_fn()
