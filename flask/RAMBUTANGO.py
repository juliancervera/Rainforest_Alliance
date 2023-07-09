# ToDo: Mantener separadas las variables de costos por categoría hasta sumarlas al último
# ToDo: Add a character limit to every input cell.
# ToDo: Find a more elegant way to write all the table rows in the HTML templates
# ToDo: Añadir un botón de DESHACER, que elimine el elemento más recientemente guardado en las listas
# ToDo: Hacer que las formas sólo puedan submit al dar clic en el botón Enter del final
# ToDo: en los valores numéricos, más que maxlength, debo poner un valor minimo y valor máximo. Maxlength es para texto
# ToDo: añadir columna adicional con un signo de porcentaje pegado a la celda de porcentaje donde aplique
# ToDo: En los htmls de costos, asegurarme de que el step sea 0.00 donde aplique

# Subdominio cálculo de costos.

# Instalación de sistemas de riego.

# Precios varían según el momento de la cosecha.

# En instrucciones: indicar que se debe tomar en cuenta cuántas veces se repite al año la actividad.


# 1-5 <-- pequeño
# 5-15 <-- mediano
# 15 < <--grande



from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/ventas", methods=["GET", "POST"])
def ventas():
    session.clear() #ToDo: check if this line should really go here
    if request.method == "POST":
        producto = request.form["producto"]
        cantidad_vendida = float(request.form["cantidad_vendida"])
        unidad = request.form["unidad"]
        precio_venta = float(request.form["precio_venta"])

        ingreso_ventas = cantidad_vendida * precio_venta

        session['producto'] = producto
        session['cantidad_vendida'] = cantidad_vendida
        session['unidad'] = unidad
        session['precio_venta'] = precio_venta
        session['ingreso_ventas'] = ingreso_ventas

        return render_template("ventas.html", producto=producto, cantidad_vendida=cantidad_vendida,
                               unidad=unidad, precio_venta=precio_venta, ingreso_ventas=ingreso_ventas)
    else:
        return render_template("ventas.html")


#ToDo: Hacer que el botón de "go back" borre la última sublista añadida a insumos_actividades y trabajo_actividades
#ToDo: Poner primero trabajo y luego insumos
@app.route("/cuestionario_actividades", methods=["GET", "POST"])
def cuestionario_actividades():
    if request.method == "POST":
        actividad = request.form.get("actividad")

        insumos_actividades = session.get('insumos_actividades', [])
        trabajo_actividades = session.get('trabajo_actividades', [])
        producto = session.get("producto")

        lista_insumos = []
        lista_trabajo = []

        lista_insumos.append(actividad)
        lista_trabajo.append(actividad)

        for i in range(1, 16):
            locals()[f"insumo_{i}"] = request.form.get(f"insumo_{i}")
            locals()[f"cantidad_{i}"] = request.form.get(f"cantidad_{i}")
            locals()[f"unidad_{i}"] = request.form.get(f"unidad_{i}")
            locals()[f"costo_unidad_{i}"] = request.form.get(f"costo_unidad_{i}")
            locals()[f"costo_total_{i}"] = ""

            locals()[f"trabajo_{i}"] = request.form.get(f"trabajo_{i}")
            locals()[f"cantidad_trabajo_{i}"] = request.form.get(f"cantidad_trabajo_{i}")
            locals()[f"unidad_trabajo_{i}"] = request.form.get(f"unidad_trabajo_{i}")
            locals()[f"costo_trabajo_unidad_{i}"] = request.form.get(f"costo_trabajo_unidad_{i}")
            locals()[f"autoempleo_{i}"] = request.form.get(f"autoempleo_{i}")
            locals()[f"costo_total_trabajo_{i}"] = ""

            try:
                locals()[f"cantidad_{i}"] = float(locals()[f"cantidad_{i}"])
                locals()[f"costo_unidad_{i}"] = float(locals()[f"costo_unidad_{i}"])
                locals()[f"costo_total_{i}"] = locals()[f"cantidad_{i}"] * locals()[f"costo_unidad_{i}"]
            except ValueError:
                # Handle the case where either cantidad or costo_unidad is not a valid number
                pass

            try:
                locals()[f"cantidad_trabajo_{i}"] = float(locals()[f"cantidad_trabajo_{i}"])
                locals()[f"costo_trabajo_unidad_{i}"] = float(locals()[f"costo_trabajo_unidad_{i}"])
                locals()[f"costo_total_trabajo_{i}"] = locals()[f"cantidad_trabajo_{i}"] * locals()[f"costo_trabajo_unidad_{i}"]
            except ValueError:
                # Handle the case where either cantidad or costo_unidad is not a valid number
                pass

            sublista_insumos = [
                locals()[f"insumo_{i}"],
                locals()[f"cantidad_{i}"],
                locals()[f"unidad_{i}"],
                locals()[f"costo_unidad_{i}"],
                locals()[f"costo_total_{i}"]
            ]

            sublista_trabajo = [
                locals()[f"trabajo_{i}"],
                locals()[f"cantidad_trabajo_{i}"],
                locals()[f"unidad_trabajo_{i}"],
                locals()[f"costo_trabajo_unidad_{i}"],
                locals()[f"autoempleo_{i}"],
                locals()[f"costo_total_trabajo_{i}"]
            ]

            lista_insumos.append(sublista_insumos)
            lista_trabajo.append(sublista_trabajo)

        insumos_actividades.append([lista_insumos])
        trabajo_actividades.append([lista_trabajo])

        session['insumos_actividades'] = insumos_actividades
        session['trabajo_actividades'] = trabajo_actividades

        # Create a dictionary to store the variables and their values
        variables = {}

        # Generate the variable names and assign their default values
        for i in range(1, 16):
            variables[f"insumo_{i}"] = locals()[f"insumo_{i}"]
            variables[f"cantidad_{i}"] = locals()[f"cantidad_{i}"]
            variables[f"unidad_{i}"] = locals()[f"unidad_{i}"]
            variables[f"costo_unidad_{i}"] = locals()[f"costo_unidad_{i}"]
            variables[f"costo_total_{i}"] = locals()[f"costo_total_{i}"]

            variables[f"trabajo_{i}"] = locals()[f"trabajo_{i}"]
            variables[f"cantidad_trabajo_{i}"] = locals()[f"cantidad_trabajo_{i}"]
            variables[f"unidad_trabajo_{i}"] = locals()[f"unidad_trabajo_{i}"]
            variables[f"costo_trabajo_unidad_{i}"] = locals()[f"costo_trabajo_unidad_{i}"]
            variables[f"costo_total_trabajo_{i}"] = locals()[f"costo_total_trabajo_{i}"]
            variables[f"autoempleo_{i}"] = locals()[f"autoempleo_{i}"]

        return render_template(
            "cuestionario_actividades.html",
            producto=producto,
            actividad=actividad,
            insumos_actividades=insumos_actividades,
            **variables
        )

    else:
        producto = session.get("producto")
        insumos_actividades = session.get("insumos_actividades")
        return render_template(
            "cuestionario_actividades.html",
            producto=producto,
            insumos_actividades=insumos_actividades
        )

# ToDo: Costos fijos: Dos tablas: Sueldos fijos y costos fijos, con base en el Excel
# ToDo: Vaciar las listas correspondientes si el usuario vuelve al formulario vacío (get request?)
# ToDo: la variable de porcentaje debe guardarse tal cual para reaparecer en la página, pero...
# ...debe transformarse en número y dividirse entre cien para ser multiplicada y guardarse en la lista

@app.route("/cuestionario_costos_fijos", methods=["GET", "POST"])
def cuestionario_costos_fijos():
    if request.method == "POST":

        producto = session.get("producto")

        sueldos_fijos = []
        costos_fijos = []

        for i in range(1, 16):
            locals()[f"trabajo_fijo_{i}"] = request.form.get(f"trabajo_fijo_{i}")
            locals()[f"cantidad_trabajo_fijo_{i}"] = request.form.get(f"cantidad_trabajo_fijo_{i}")
            locals()[f"sueldo_trabajo_fijo_{i}"] = request.form.get(f"sueldo_trabajo_fijo_{i}")
            locals()[f"autoempleo_fijo_{i}"] = request.form.get(f"autoempleo_fijo_{i}")
            locals()[f"porcentaje_trabajo_fijo_{i}"] = request.form.get(f"porcentaje_trabajo_fijo_{i}")
            locals()[f"costo_total_trabajo_fijo_{i}"] = ""

            locals()[f"costo_fijo_{i}"] = request.form.get(f"costo_fijo_{i}")
            locals()[f"monto_fijo_{i}"] = request.form.get(f"monto_fijo_{i}")
            locals()[f"porcentaje_costo_fijo_{i}"] = request.form.get(f"porcentaje_costo_fijo_{i}")
            locals()[f"costo_fijo_total_{i}"] = ""

            try:
                locals()[f"cantidad_trabajo_fijo_{i}"] = float(locals()[f"cantidad_trabajo_fijo_{i}"])
                locals()[f"sueldo_trabajo_fijo_{i}"] = float(locals()[f"sueldo_trabajo_fijo_{i}"])
                locals()[f"porcentaje_trabajo_fijo_{i}"] = float(locals()[f"porcentaje_trabajo_fijo_{i}"])
                locals()[f"costo_total_trabajo_fijo_{i}"] = locals()[f"cantidad_trabajo_fijo_{i}"] * locals()[f"sueldo_trabajo_fijo_{i}"] * (locals()[f"porcentaje_trabajo_fijo_{i}"] / 100)
            except ValueError:
                # Handle the case where either cantidad or costo_unidad is not a valid number
                pass

            try:
                locals()[f"monto_fijo_{i}"] = float(locals()[f"monto_fijo_{i}"])
                locals()[f"porcentaje_costo_fijo_{i}"] = float(locals()[f"porcentaje_costo_fijo_{i}"])
                locals()[f"costo_fijo_total_{i}"] = locals()[f"monto_fijo_{i}"] * (locals()[f"porcentaje_costo_fijo_{i}"] / 100)
            except ValueError:
                # Handle the case where either cantidad or costo_unidad is not a valid number
                pass

            sublista_trabajo = [
                locals()[f"trabajo_fijo_{i}"],
                locals()[f"cantidad_trabajo_fijo_{i}"],
                locals()[f"sueldo_trabajo_fijo_{i}"],
                locals()[f"porcentaje_trabajo_fijo_{i}"],
                locals()[f"autoempleo_fijo_{i}"],
                locals()[f"costo_total_trabajo_fijo_{i}"]
            ]

            sublista_insumos = [
                locals()[f"costo_fijo_{i}"],
                locals()[f"monto_fijo_{i}"],
                locals()[f"porcentaje_costo_fijo_{i}"],
                locals()[f"costo_fijo_total_{i}"]
            ]

            sueldos_fijos.append(sublista_trabajo)
            costos_fijos.append(sublista_insumos)

        session['sueldos_fijos'] = sueldos_fijos
        session['costos_fijos'] = costos_fijos

        # Create a dictionary to store the variables and their values
        variables = {}

        # Generate the variable names and assign their default values
        for i in range(1, 16):
            variables[f"trabajo_fijo_{i}"] = locals()[f"trabajo_fijo_{i}"]
            variables[f"cantidad_trabajo_fijo_{i}"] = locals()[f"cantidad_trabajo_fijo_{i}"]
            variables[f"sueldo_trabajo_fijo_{i}"] = locals()[f"sueldo_trabajo_fijo_{i}"]
            variables[f"porcentaje_trabajo_fijo_{i}"] = locals()[f"porcentaje_trabajo_fijo_{i}"]
            variables[f"autoempleo_fijo_{i}"] = locals()[f"autoempleo_fijo_{i}"]
            variables[f"costo_total_trabajo_fijo_{i}"] = locals()[f"costo_total_trabajo_fijo_{i}"]

            variables[f"costo_fijo_{i}"] = locals()[f"costo_fijo_{i}"]
            variables[f"monto_fijo_{i}"] = locals()[f"monto_fijo_{i}"]
            variables[f"porcentaje_costo_fijo_{i}"] = locals()[f"porcentaje_costo_fijo_{i}"]
            variables[f"costo_fijo_total_{i}"] = locals()[f"costo_fijo_total_{i}"]

        return render_template(
            "cuestionario_costos_fijos.html",
            producto=producto,
            sueldos_fijos=sueldos_fijos,
            costos_fijos=costos_fijos,
            **variables
        )

    else:
        producto = session.get("producto")

        costos_fijos = []
        sueldos_fijos = []

        session["costos_fijos"] = costos_fijos
        session["sueldos_fijos"] = sueldos_fijos

        porcentajes_default = {}

        # Generate the variable names and assign their default values
        for i in range(1, 16):
            locals()[f"porcentaje_costo_fijo_{i}"] = 100
            locals()[f"porcentaje_trabajo_fijo_{i}"] = 100
            porcentajes_default[f"porcentaje_costo_fijo_{i}"] = locals()[f"porcentaje_costo_fijo_{i}"]
            porcentajes_default[f"porcentaje_trabajo_fijo_{i}"] = locals()[f"porcentaje_trabajo_fijo_{i}"]

        return render_template(
            "cuestionario_costos_fijos.html",
            producto=producto,
            costos_fijos=costos_fijos,
            sueldos_fijos=sueldos_fijos,
            **porcentajes_default
        )

@app.route("/pregunta_impuestos_venta")
def pregunta_impuestos_venta():
    return render_template("pregunta_impuestos_venta.html")

@app.route("/pregunta_impuestos_fijos")
def pregunta_impuestos_fijos():
    return render_template("pregunta_impuestos_fijos.html")

@app.route("/pregunta_costos_certificacion")
def pregunta_costos_certificacion():
    return render_template("pregunta_costos_certificacion.html")

@app.route("/pregunta_costos_exportacion")
def pregunta_costos_exportacion():
    return render_template("pregunta_costos_exportacion.html")

@app.route("/cuestionario_impuestos_venta", methods=["GET", "POST"])
def cuestionario_impuestos_venta():
    if request.method == "POST":

        producto = session.get("producto")

        impuestos_venta = []

        for i in range(1, 6):
            locals()[f"impuesto_venta_{i}"] = request.form.get(f"impuesto_venta_{i}")
            try:
                locals()[f"porcentaje_{i}"] = float(request.form.get(f"porcentaje_{i}"))
            except ValueError:
                locals()[f"porcentaje_{i}"] = request.form.get(f"porcentaje_{i}")

            try:
                locals()[f"unidades_consideradas_{i}"] = float(request.form.get(f"unidades_consideradas_{i}"))
            except ValueError:
                locals()[f"unidades_consideradas_{i}"] = request.form.get(f"unidades_consideradas_{i}")

            sublista_impuestos = [
                locals()[f"impuesto_venta_{i}"],
                locals()[f"porcentaje_{i}"],
                locals()[f"unidades_consideradas_{i}"],
            ]

            impuestos_venta.append(sublista_impuestos)

        session['impuestos_venta'] = impuestos_venta

        # Create a dictionary to store the variables and their values
        variables = {}

        # Generate the variable names and assign their default values
        for i in range(1, 6):
            variables[f"impuesto_venta_{i}"] = locals()[f"impuesto_venta_{i}"]
            variables[f"porcentaje_{i}"] = locals()[f"porcentaje_{i}"]
            variables[f"unidades_consideradas_{i}"] = locals()[f"unidades_consideradas_{i}"]
        print(impuestos_venta)
        return render_template(
            "cuestionario_impuestos_venta.html",
            producto=producto,
            impuestos_venta=impuestos_venta,
            **variables
        )

    else:
        producto = session.get("producto")
        cantidad_vendida = session.get("cantidad_vendida")

        impuestos_venta = []

        session["impuestos_venta"] = impuestos_venta

        unidades_consideradas_default = {}

        # Generate the variable names and assign their default values
        for i in range(1, 6):
            locals()[f"unidades_consideradas_{i}"] = cantidad_vendida
            unidades_consideradas_default[f"unidades_consideradas_{i}"] = locals()[f"unidades_consideradas_{i}"]

        return render_template(
            "cuestionario_impuestos_venta.html",
            producto=producto,
            impuestos_venta=impuestos_venta,
            **unidades_consideradas_default
        )

@app.route("/cuestionario_impuestos_fijos", methods=["GET", "POST"])
def cuestionario_impuestos_fijos():
    if request.method == "POST":

        producto = session.get("producto")

        impuestos_fijos = []

        for i in range(1, 6):
            locals()[f"impuesto_fijo_{i}"] = request.form.get(f"impuesto_fijo_{i}")
            locals()[f"monto_{i}"] = request.form.get(f"monto_{i}")
            locals()[f"porcentaje_{i}"] = request.form.get(f"porcentaje_{i}")
            locals()[f"monto_total_{i}"] = ""

            try:
                locals()[f"monto_{i}"] = float(request.form.get(f"monto_{i}"))
                locals()[f"porcentaje_{i}"] = float(request.form.get(f"porcentaje_{i}"))
                locals()[f"monto_total_{i}"] = locals()[f"monto_{i}"] * (locals()[f"porcentaje_{i}"] / 100)
            except ValueError:
                pass

            sublista_impuestos = [
                locals()[f"impuesto_fijo_{i}"],
                locals()[f"monto_{i}"],
                locals()[f"porcentaje_{i}"],
                locals()[f"monto_total_{i}"]
            ]

            impuestos_fijos.append(sublista_impuestos)

        session['impuestos_fijos'] = impuestos_fijos

        # Create a dictionary to store the variables and their values
        variables = {}

        # Generate the variable names and assign their default values
        for i in range(1, 6):
            variables[f"impuesto_fijo_{i}"] = locals()[f"impuesto_fijo_{i}"]
            variables[f"monto_{i}"] = locals()[f"monto_{i}"]
            variables[f"porcentaje_{i}"] = locals()[f"porcentaje_{i}"]
            variables[f"monto_total_{i}"] = locals()[f"monto_total_{i}"]
        print(impuestos_fijos)
        return render_template(
            "cuestionario_impuestos_fijos.html",
            producto=producto,
            impuestos_fijos=impuestos_fijos,
            **variables
        )

    else:
        producto = session.get("producto")

        impuestos_fijos = []

        session["impuestos_fijos"] = impuestos_fijos

        porcentaje_default = {}

        # Generate the variable names and assign their default values
        for i in range(1, 6):
            locals()[f"porcentaje_{i}"] = 100
            porcentaje_default[f"porcentaje_{i}"] = locals()[f"porcentaje_{i}"]

        return render_template(
            "cuestionario_impuestos_fijos.html",
            producto=producto,
            impuestos_fijos=impuestos_fijos,
            **porcentaje_default
        )

@app.route("/cuestionario_costos_certificacion", methods=["GET", "POST"])
def cuestionario_costos_certificacion():
    if request.method == "POST":

        producto = session.get("producto")

        costos_certificacion = []

        for i in range(1, 6):
            locals()[f"certificacion_{i}"] = request.form.get(f"certificacion_{i}")
            locals()[f"costo_{i}"] = request.form.get(f"costo_{i}")
            locals()[f"porcentaje_{i}"] = request.form.get(f"porcentaje_{i}")
            locals()[f"costo_total_{i}"] = ""

            try:
                locals()[f"costo_{i}"] = float(request.form.get(f"costo_{i}"))
                locals()[f"porcentaje_{i}"] = float(request.form.get(f"porcentaje_{i}"))
                locals()[f"costo_total_{i}"] = locals()[f"costo_{i}"] * (locals()[f"porcentaje_{i}"] / 100)
            except ValueError:
                pass

            sublista_certificacion = [
                locals()[f"certificacion_{i}"],
                locals()[f"costo_{i}"],
                locals()[f"porcentaje_{i}"],
                locals()[f"costo_total_{i}"]
            ]

            costos_certificacion.append(sublista_certificacion)

        session['costos_certificacion'] = costos_certificacion

        # Create a dictionary to store the variables and their values
        variables = {}

        # Generate the variable names and assign their default values
        for i in range(1, 6):
            variables[f"certificacion_{i}"] = locals()[f"certificacion_{i}"]
            variables[f"costo_{i}"] = locals()[f"costo_{i}"]
            variables[f"porcentaje_{i}"] = locals()[f"porcentaje_{i}"]
            variables[f"costo_total_{i}"] = locals()[f"costo_total_{i}"]
        print(costos_certificacion)
        return render_template(
            "cuestionario_costos_certificacion.html",
            producto=producto,
            costos_certificacion=costos_certificacion,
            **variables
        )

    else:
        producto = session.get("producto")

        costos_certificacion = []

        session["costos_certificacion"] = costos_certificacion

        porcentaje_default = {}

        # Generate the variable names and assign their default values
        for i in range(1, 6):
            locals()[f"porcentaje_{i}"] = 100
            porcentaje_default[f"porcentaje_{i}"] = locals()[f"porcentaje_{i}"]

        return render_template(
            "cuestionario_costos_certificacion.html",
            producto=producto,
            costos_certificacion=costos_certificacion,
            **porcentaje_default
        )

@app.route("/cuestionario_costos_exportacion", methods=["GET", "POST"])
def cuestionario_costos_exportacion():
    if request.method == "POST":

        producto = session.get("producto")

        costos_exportacion = []

        for i in range(1, 6):
            locals()[f"costo_exportacion_{i}"] = request.form.get(f"costo_exportacion_{i}")

            try:
                locals()[f"costo_unidad_{i}"] = float(request.form.get(f"costo_unidad_{i}"))
            except ValueError:
                locals()[f"costo_unidad_{i}"] = request.form.get(f"costo_unidad_{i}")

            try:
                locals()[f"unidades_consideradas_{i}"] = float(request.form.get(f"unidades_consideradas_{i}"))
            except ValueError:
                locals()[f"unidades_consideradas_{i}"] = request.form.get(f"unidades_consideradas_{i}")

            sublista_exportacion = [
                locals()[f"costo_exportacion_{i}"],
                locals()[f"costo_unidad_{i}"],
                locals()[f"unidades_consideradas_{i}"],
            ]

            costos_exportacion.append(sublista_exportacion)

        session['costos_exportacion'] = costos_exportacion

            # Create a dictionary to store the variables and their values
        variables = {}

            # Generate the variable names
        for i in range(1, 6):
            variables[f"costo_exportacion_{i}"] = locals()[f"costo_exportacion_{i}"]
            variables[f"costo_unidad_{i}"] = locals()[f"costo_unidad_{i}"]
            variables[f"unidades_consideradas_{i}"] = locals()[f"unidades_consideradas_{i}"]
        print(costos_exportacion)
        return render_template(
            "cuestionario_costos_exportacion.html",
            producto=producto,
            costos_exportacion=costos_exportacion,
            **variables
        )

    else:
        producto = session.get("producto")

        costos_exportacion = []

        session["costos_exportacion"] = costos_exportacion

        return render_template(
            "cuestionario_costos_exportacion.html",
            producto=producto,
            costos_exportacion=costos_exportacion
        )

@app.route("/analisis_final", methods=["GET"])
def analisis_final():
    producto = session.get("producto")
    cantidad_vendida = session.get("cantidad_vendida")
    unidad = session.get("unidad")
    insumos_actividades = session.get("insumos_actividades")
    trabajo_actividades = session.get("trabajo_actividades")
    sueldos_fijos = session.get("sueldos_fijos")
    costos_fijos = session.get("costos_fijos")
    impuestos_venta = session.get("impuestos_venta")
    impuestos_fijos = session.get("impuestos_fijos")
    costos_certificacion = session.get("costos_certificacion")
    costos_exportacion = session.get("costos_exportacion")

    print("Producto:", producto)
    print("Cantidad Vendida:", cantidad_vendida)
    print("Unidad:", unidad)
    print("Insumos Actividades:", insumos_actividades)
    print("Trabajo Actividades:", trabajo_actividades)
    print("Sueldos Fijos:", sueldos_fijos)
    print("Costos Fijos:", costos_fijos)
    print("Impuestos Venta:", impuestos_venta)
    print("Impuestos Fijos:", impuestos_fijos)
    print("Costos Certificacion:", costos_certificacion)
    print("Costos Exportacion:", costos_exportacion)

    return render_template("analisis_final.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

"""
costos_actividades = [
    [
        "siembra",
        ["Fertilizante", 4.5, "saco", 1300, 5850],
        ["Otro insumo", 34, "kilos", 10, 340],
    ],
    [
        "siembra",
        ["Fertilizante", 4.5, "saco", 1300, 5850],
        ["Otro insumo", 34, "kilos", 10, 340],
    ]
]
"""

#


insumos_actividades = [
    [
        ['Siembra',
         ['Sembrar', 3.0, 'días de trabajo', 1000.0, 'Sí', 3000.0],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', '']
        ]
    ],
    [
        ['Deschuponar',
         ['Cortar', 2.0, 'días de trabajo', 1000.0, 'Sí', 2000.0],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', ''],
         ['', '', '', '', 'No', '']
        ]
    ]
]


for actividad in insumos_actividades:


