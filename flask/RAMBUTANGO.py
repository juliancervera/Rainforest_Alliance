# ToDo: Mantener separadas las variables de costos por categoría hasta sumarlas al último
# ToDo: Add a character limit to every input cell.

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

#ToDo: Hacer que el botón de "go back" borre la última sublista añadida a costos_actividades
#ToDo: Cambiar nombre de la siguiente función y adaptar todo alrededor de eso.
#ToDo: Añadir un if al template del formulario de actividades.
# Este if detecta si ya hay contenido numérico en al menos uno de las casillas de costos totales.
# Si ya está ese contenido, saca los botones de regitrar nueva actividad o pasar a otros costos.
# NO OLVIDAR QUE EL FORMULARIO PARA TRABAJO TENGA LA OPCIÓN DE AUTOEMPLEO
@app.route("/pregunta_primera_actividad", methods=["GET", "POST"])
def pregunta_primera_actividad():
    if request.method == "POST":
        actividad = request.form.get("actividad")

        insumos_actividades = session.get('insumos_actividades', [])
        trabajo_actividades = session.get('trabajo_actividades', [])

        lista_insumos = []
        lista_trabajo = []

        lista_insumos.append(actividad)
        lista_trabajo.append(actividad)

        for i in range(1, 16):
            insumo = request.form.get(f"insumo_{i}")
            cantidad = request.form.get(f"cantidad_{i}")
            unidad = request.form.get(f"unidad_{i}")
            costo_unidad = request.form.get(f"costo_unidad_{i}")
            costo_total = ""

            try:
                cantidad = float(cantidad)
                costo_unidad = float(costo_unidad)
                costo_total = cantidad * costo_unidad
            except ValueError:
                # Handle the case where either cantidad or costo_unidad is not a valid number
                pass

            sublist = [insumo, cantidad, unidad, costo_unidad, costo_total]
            lista_insumos.append(sublist)

        """
        insumo_1 = request.form["insumo_1"]
        cantidad_1 = request.form["cantidad_1"]
        unidad_1 = request.form["unidad_1"]
        costo_unidad_1 = request.form["costo_unidad_1"]
        costo_total_1 = ""
        try:
            cantidad_1 = float(request.form.get("cantidad_1"))
            costo_unidad_1 = float(request.form.get("costo_unidad_1"))
            costo_total_1 = cantidad_1 * costo_unidad_1
        except ValueError:
            # Handle the case where either cantidad_1 or costo_unidad_1 is not a valid number
            pass
        """

        insumos_actividades.append([lista_insumos])
        trabajo_actividades.append([lista_trabajo])

        session['insumos_actividades'] = insumos_actividades
        session['trabajo_actividades'] = trabajo_actividades

        return redirect("/info_actividades")
    else:
        producto = session.get("producto")
        insumos_actividades = session.get("insumos_actividades")
        return render_template(
            "pregunta_primera_actividad.html",
            producto=producto,
            costos_actividades=insumos_actividades
        )


""" RESPALDO DE CUANDO FUNCIONABA
@app.route("/pregunta_primera_actividad", methods=["GET", "POST"])
def pregunta_primera_actividad():
    if request.method == "POST":
        actividad = request.form.get("actividad")
        session["actividad_1"] = actividad
        return redirect("/info_actividades")
    else:
        producto = session.get("producto")
        return render_template("pregunta_primera_actividad.html", producto=producto)
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