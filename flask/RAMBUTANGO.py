# ToDo: Mantener separadas las variables de costos por categoría hasta sumarlas al último
# ToDo: Add a character limit to every input cell.
# ToDo: Find a more elegant way to write all the table rows in the HTML templates

# Subdominio cálculo de costos.

# Instalación de sistemas de riego.

# Precios varían según el momento de la cosecha.

# En instrucciones: indicar que se debe tomar en cuenta cuántas veces se repite al año la actividad.

# Añadir botón autoempleo versus contrato. variable versus fijo

# 1-5 <-- pequeño
# 5-15 <-- mediano
# 15 < <--grande


# La app va a funcionar con un número finito de actividades que formen parte del proceso productivo.


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


@app.route("/pregunta_donativos")
def pregunta_donativos():
    producto = session.get('producto')
    return render_template('pregunta_donativos.html', producto=producto)

# ToDo: Añadir pregunta otros ingresos.
@app.route("/info_donativos")
def info_donativos():
    # Process the request or perform any other necessary actions
    return "You chose 'Yes' for receiving donativos."

#ToDo: Hacer que el botón de "go back" borre la última sublista añadida a insumos_actividades y trabajo_actividades

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


""" RESPALDO DE CUANDO FUNCIONABA
@app.route("/cuestionario_actividades", methods=["GET", "POST"])
def cuestionario_actividades():
    if request.method == "POST":
        actividad = request.form.get("actividad")
        session["actividad_1"] = actividad
        return redirect("/info_actividades")
    else:
        producto = session.get("producto")
        return render_template("cuestionario_actividades.html", producto=producto)
"""


@app.route("/info_actividades")
def info_actividades():
    return "Hola, Mundo"


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