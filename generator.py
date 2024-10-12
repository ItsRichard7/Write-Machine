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
        nombre = nodo[1]
        valor = nodo[2]

        # Definir variable como local (alloca) y almacenarla
        variable = self.builder.alloca(ir.IntType(32), name=nombre)
        self.builder.store(ir.Constant(ir.IntType(32), valor), variable)
        self.variables[nombre] = variable

        print(f"Definiendo variable {nombre} con valor {valor}")

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

# Ejemplo de AST de entrada con un for loop
ast = ('sentencias', ('proc', 'main', ('sentencias', ('def_variable', 'varGlobal1', 1), ('sentencias', ('def_variable', 'varGlobal2', 2), ('sentencias', ('put_variable', 'varGlobal1', 2), ('sentencias', ('put_variable', 'varGlobal2', 4)))))))

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
