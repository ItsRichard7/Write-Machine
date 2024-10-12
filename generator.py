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
        elif tipo == 'invocacion_proc':
            self.invocar_procedimiento(nodo)
        elif tipo == 'posx':
            self.generar_posx(nodo)
        elif tipo == 'posy':
            self.generar_posy(nodo)
        else:
            print(f"Tipo de nodo no manejado: {tipo}")

    def generar_procedimiento(self, nodo):
        nombre = nodo[1]
        argumentos = nodo[2] if isinstance(nodo[2], list) else []
        cuerpo = nodo[3] if len(nodo) > 3 else nodo[2]

        # Crear la función LLVM con argumentos
        tipo_args = [ir.IntType(32)] * len(argumentos)
        tipo_funcion = ir.FunctionType(ir.VoidType(), tipo_args)
        funcion = ir.Function(self.module, tipo_funcion, name=nombre)
        self.funciones[nombre] = funcion

        # Crear un bloque básico para el cuerpo de la función
        bloque = funcion.append_basic_block(name="entrada")
        self.builder = ir.IRBuilder(bloque)

        # Definir los argumentos como variables locales
        for i, arg in enumerate(funcion.args):
            arg_name = argumentos[i]
            arg.name = arg_name
            var_local = self.builder.alloca(ir.IntType(32), name=arg_name)
            self.builder.store(arg, var_local)
            self.variables[arg_name] = var_local

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

    def generar_posx(self, nodo):
        valor = nodo[1]
        variable = self.variables.get(valor)
        if variable:
            valor_posx = self.builder.load(variable, name="posx_temp")
            print(f"Generando PosX con valor de la variable {valor}")
        else:
            print(f"Variable {valor} no encontrada.")

    def generar_posy(self, nodo):
        valor = nodo[1]
        variable = self.variables.get(valor)
        if variable:
            valor_posy = self.builder.load(variable, name="posy_temp")
            print(f"Generando PosY con valor de la variable {valor}")
        else:
            print(f"Variable {valor} no encontrada.")

# Ejemplo de AST de entrada
ast = ('sentencias', 
        ('proc', 'posiciona', ['valorX', 'valorY'], 
            ('sentencias', ('posx', 'valorX'), 
            ('sentencias', ('posy', 'valorY')))),
        ('sentencias', ('proc', 'main', 
            ('sentencias', ('def_variable', 'varGlobal1', 1), 
            ('sentencias', ('invocacion_proc', 'posiciona', [('number', 1), ('number', 1)]))))))

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
