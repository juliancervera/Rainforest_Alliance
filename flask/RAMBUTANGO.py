from flask import Flask, render_template, request, redirect, url_for, session
import sys

app = Flask(__name__)
app.secret_key = '4prKZ_3$%_ztprd_24_P_!?'


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/ventas", methods=["GET", "POST"])
def ventas():
    session.clear()
    if request.method == "POST":
        producto = request.form["producto"]
        cantidad_vendida = float(request.form["cantidad_vendida"])
        unidad = request.form["unidad"]

        session['producto'] = producto.lower()
        session['cantidad_vendida'] = cantidad_vendida
        session['unidad'] = unidad.lower()

        return redirect(url_for('pregunta_actividades'))
    else:
        return render_template("ventas.html")

@app.route("/pregunta_actividades", methods=["GET", "POST"])
def pregunta_actividades():
    if request.method == "POST":
        actividad = request.form.get("actividad")
        actividad = actividad.lower()  # Convert to lowercase

        nombres_actividades = session.get("nombres_actividades", [])

        # Check if actividad already exists in nombres_actividades
        if actividad in nombres_actividades:
            # Generate a unique version of actividad
            counter = 2
            while f"{actividad}_{counter}" in nombres_actividades:
                counter += 1
            actividad = f"{actividad}_{counter}"

        nombres_actividades.append(actividad)
        session["nombres_actividades"] = nombres_actividades
        session["actividad"] = actividad

        return redirect(url_for('cuestionario_actividades'))
    else:
        producto = session.get("producto")
        unidad = session.get("unidad")
        cantidad_vendida = session.get("cantidad_vendida")
        nombres_actividades = session.get("nombres_actividades", [])

        return render_template("pregunta_actividades.html",
                               nombres_actividades=nombres_actividades,
                               producto=producto,
                               unidad=unidad,
                               cantidad_vendida=cantidad_vendida)


@app.route("/cuestionario_actividades", methods=["GET", "POST"])
def cuestionario_actividades():
    if request.method == "POST":
        num_rows_trabajo = int(request.form.get("rowCounter_trabajo"))
        num_rows_costos = int(request.form.get("rowCounter_insumos"))

        actividad = session.get("actividad")
        nombres_actividades = session.get("nombres_actividades")
        producto = session.get("producto")
        unidad = session.get("unidad")
        cantidad_vendida = session.get("cantidad_vendida")

        insumos_actividades = session.get('insumos_actividades', [])
        trabajo_actividades = session.get('trabajo_actividades', [])

        lista_insumos = []
        lista_trabajo = []

        for i in range(1, num_rows_trabajo + 1):
            try:
                locals()[f"trabajo_{i}"] = request.form.get(f"trabajo_{i}")
                locals()[f"cantidad_trabajo_{i}"] = float(request.form.get(f"cantidad_trabajo_{i}"))
                locals()[f"unidad_trabajo_{i}"] = request.form.get(f"unidad_trabajo_{i}")
                locals()[f"costo_trabajo_unidad_{i}"] = float(request.form.get(f"costo_trabajo_unidad_{i}"))
                locals()[f"autoempleo_{i}"] = request.form.get(f"autoempleo_{i}")
                locals()[f"costo_total_trabajo_{i}"] = round(locals()[f"cantidad_trabajo_{i}"] * locals()[f"costo_trabajo_unidad_{i}"], 2)
                sublista_trabajo = [
                    locals()["actividad"],
                    locals()[f"trabajo_{i}"],
                    locals()[f"cantidad_trabajo_{i}"],
                    locals()[f"unidad_trabajo_{i}"],
                    locals()[f"costo_trabajo_unidad_{i}"],
                    locals()[f"autoempleo_{i}"],
                    locals()[f"costo_total_trabajo_{i}"]
                ]
                lista_trabajo.append(sublista_trabajo)
            except ValueError:
                pass

        for i in range(1, num_rows_costos + 1):
            try:
                locals()[f"insumo_{i}"] = request.form.get(f"insumo_{i}")
                locals()[f"cantidad_{i}"] = float(request.form.get(f"cantidad_{i}"))
                locals()[f"unidad_{i}"] = request.form.get(f"unidad_{i}")
                locals()[f"costo_unidad_{i}"] = float(request.form.get(f"costo_unidad_{i}"))
                locals()[f"costo_total_{i}"] = round(locals()[f"cantidad_{i}"] * locals()[f"costo_unidad_{i}"], 2)
                sublista_insumos = [
                    locals()["actividad"],
                    locals()[f"insumo_{i}"],
                    locals()[f"cantidad_{i}"],
                    locals()[f"unidad_{i}"],
                    locals()[f"costo_unidad_{i}"],
                    locals()[f"costo_total_{i}"]
                ]
                lista_insumos.append(sublista_insumos)
            except ValueError:
                pass

        # Guardar listas en la sesión poder recuperarlas en "/deshacer"
        session["lista_insumos"] = lista_insumos
        session["lista_trabajo"] = lista_trabajo

        if lista_insumos:
            insumos_actividades.append(lista_insumos)
        else:
            pass

        if lista_trabajo:
            trabajo_actividades.append(lista_trabajo)
        else:
            pass

        session['insumos_actividades'] = insumos_actividades
        session['trabajo_actividades'] = trabajo_actividades

        return render_template(
            "cuestionario_actividades.html",
            producto=producto,
            actividad=actividad,
            cantidad_vendida=cantidad_vendida,
            unidad=unidad,
            nombres_actividades=nombres_actividades,
            lista_insumos=lista_insumos,
            lista_trabajo=lista_trabajo
        )

    else:
        producto = session.get("producto")
        unidad = session.get("unidad")
        cantidad_vendida = session.get("cantidad_vendida")
        nombres_actividades = session.get("nombres_actividades")
        actividad = session.get("actividad")

        return render_template(
            "cuestionario_actividades.html",
            producto=producto,
            nombres_actividades=nombres_actividades,
            cantidad_vendida=cantidad_vendida,
            actividad=actividad,
            unidad=unidad,
        )


@app.route("/borrar")
def borrar():
    insumos_actividades = session.get('insumos_actividades', [])
    trabajo_actividades = session.get('trabajo_actividades', [])
    nombres_actividades = session.get("nombres_actividades")
    actividad = session.get("actividad")

    nombres_actividades.pop()

    if trabajo_actividades:
        for sublist in trabajo_actividades[-1]:
            if sublist[0] == actividad:
                trabajo_actividades.pop()
                break

    if insumos_actividades:
        for sublist in insumos_actividades[-1]:
            if sublist[0] == actividad:
                insumos_actividades.pop()
                break

    session['insumos_actividades'] = insumos_actividades
    session['trabajo_actividades'] = trabajo_actividades
    session['nombres_actividades'] = nombres_actividades

    return redirect(url_for('pregunta_actividades'))

@app.route("/cuestionario_costos_fijos", methods=["GET", "POST"])
def cuestionario_costos_fijos():
    if request.method == "POST":

        num_rows_sueldos = int(request.form.get("rowCounter_trabajo"))
        num_rows_costos = int(request.form.get("rowCounter_insumos"))

        producto = session.get("producto")
        cantidad_vendida = session.get("cantidad_vendida")
        unidad = session.get("unidad")

        sueldos_fijos = []
        costos_fijos = []

        for i in range(1, num_rows_sueldos + 1):
            try:
                locals()[f"trabajo_fijo_{i}"] = request.form.get(f"trabajo_fijo_{i}")
                locals()[f"cantidad_trabajo_fijo_{i}"] = float(request.form.get(f"cantidad_trabajo_fijo_{i}"))
                locals()[f"sueldo_trabajo_fijo_{i}"] = float(request.form.get(f"sueldo_trabajo_fijo_{i}"))
                locals()[f"porcentaje_trabajo_fijo_{i}"] = float(request.form.get(f"porcentaje_trabajo_fijo_{i}"))
                locals()[f"autoempleo_fijo_{i}"] = request.form.get(f"autoempleo_fijo_{i}")
                locals()[f"costo_total_trabajo_fijo_{i}"] = round(locals()[f"cantidad_trabajo_fijo_{i}"] * locals()[f"sueldo_trabajo_fijo_{i}"] * (locals()[f"porcentaje_trabajo_fijo_{i}"] / 100), 2)

                sublista_trabajo = [
                    "(Costo fijo)",
                    locals()[f"trabajo_fijo_{i}"],
                    locals()[f"cantidad_trabajo_fijo_{i}"],
                    locals()[f"sueldo_trabajo_fijo_{i}"],
                    locals()[f"porcentaje_trabajo_fijo_{i}"],
                    locals()[f"autoempleo_fijo_{i}"],
                    locals()[f"costo_total_trabajo_fijo_{i}"]
                ]

                sueldos_fijos.append(sublista_trabajo)

            except ValueError:
                pass

        for i in range(1, num_rows_costos + 1):
            try:
                locals()[f"costo_fijo_{i}"] = request.form.get(f"costo_fijo_{i}")
                locals()[f"cantidad_fijo_{i}"] = float(request.form.get(f"cantidad_fijo_{i}"))
                locals()[f"unidad_fijo_{i}"] = request.form.get(f"unidad_fijo_{i}")
                locals()[f"costo_por_unidad_fijo_{i}"] = float(request.form.get(f"costo_por_unidad_fijo_{i}"))
                locals()[f"porcentaje_costo_fijo_{i}"] = float(request.form.get(f"porcentaje_costo_fijo_{i}"))
                locals()[f"costo_fijo_total_{i}"] = round(
                    locals()[f"cantidad_fijo_{i}"] * locals()[f"costo_por_unidad_fijo_{i}"] * (
                                locals()[f"porcentaje_costo_fijo_{i}"] / 100), 2
                )

                sublista_insumos = [
                    locals()[f"costo_fijo_{i}"],
                    locals()[f"cantidad_fijo_{i}"],
                    locals()[f"unidad_fijo_{i}"],
                    locals()[f"costo_por_unidad_fijo_{i}"],
                    locals()[f"porcentaje_costo_fijo_{i}"],
                    locals()[f"costo_fijo_total_{i}"]
                ]

                costos_fijos.append(sublista_insumos)
            except ValueError:
                pass

        session['sueldos_fijos'] = sueldos_fijos
        session['costos_fijos'] = costos_fijos

        return render_template(
            "cuestionario_costos_fijos.html",
            producto=producto,
            unidad=unidad,
            cantidad_vendida=cantidad_vendida,
            sueldos_fijos=sueldos_fijos,
            costos_fijos=costos_fijos,
        )

    else:
        producto = session.get("producto")
        cantidad_vendida = session.get("cantidad_vendida")
        unidad = session.get("unidad")

        costos_fijos = []
        sueldos_fijos = []

        session["costos_fijos"] = costos_fijos
        session["sueldos_fijos"] = sueldos_fijos

        return render_template(
            "cuestionario_costos_fijos.html",
            producto=producto,
            unidad=unidad,
            cantidad_vendida=cantidad_vendida,
            costos_fijos=costos_fijos,
            sueldos_fijos=sueldos_fijos
        )

@app.route("/pregunta_impuestos_venta")
def pregunta_impuestos_venta():
    return render_template("pregunta_impuestos_venta.html")

@app.route("/pregunta_impuestos_fijos")
def pregunta_impuestos_fijos():
    producto = session.get("producto")
    return render_template("pregunta_impuestos_fijos.html",
                           producto=producto)

@app.route("/pregunta_costos_certificacion")
def pregunta_costos_certificacion():
    producto = session.get("producto")
    return render_template("pregunta_costos_certificacion.html",
                           producto=producto)

@app.route("/pregunta_costos_exportacion")
def pregunta_costos_exportacion():
    producto = session.get("producto")
    return render_template("pregunta_costos_exportacion.html",
                           producto=producto)

@app.route("/cuestionario_impuestos_venta", methods=["GET", "POST"])
def cuestionario_impuestos_venta():
    if request.method == "POST":

        num_rows = int(request.form.get("rowCounter"))

        producto = session.get("producto")

        impuestos_venta = []

        for i in range(1, num_rows + 1):
            locals()[f"impuesto_venta_{i}"] = request.form.get(f"impuesto_venta_{i}")

            try:
                locals()[f"unidades_consideradas_{i}"] = float(request.form.get(f"unidades_consideradas_{i}"))
                locals()[f"porcentaje_{i}"] = float(request.form.get(f"porcentaje_{i}"))

                sublista_impuestos = [
                    locals()[f"impuesto_venta_{i}"],
                    locals()[f"porcentaje_{i}"],
                    locals()[f"unidades_consideradas_{i}"],
                ]

                impuestos_venta.append(sublista_impuestos)

            except ValueError:
                pass

        session['impuestos_venta'] = impuestos_venta

        return render_template(
            "cuestionario_impuestos_venta.html",
            producto=producto,
            impuestos_venta=impuestos_venta
        )

    else:
        producto = session.get("producto")
        cantidad_vendida = session.get("cantidad_vendida")
        unidad = session.get("unidad")

        impuestos_venta = []

        session["impuestos_venta"] = impuestos_venta

        return render_template(
            "cuestionario_impuestos_venta.html",
            producto=producto,
            cantidad_vendida=cantidad_vendida,
            impuestos_venta=impuestos_venta,
            unidad=unidad,
        )

@app.route("/cuestionario_impuestos_fijos", methods=["GET", "POST"])
def cuestionario_impuestos_fijos():
    if request.method == "POST":

        num_rows = int(request.form.get("rowCounter"))

        producto = session.get("producto")

        impuestos_fijos = []

        for i in range(1, num_rows + 1):
            locals()[f"impuesto_fijo_{i}"] = request.form.get(f"impuesto_fijo_{i}")

            try:
                locals()[f"monto_{i}"] = float(request.form.get(f"monto_{i}"))
                locals()[f"porcentaje_{i}"] = float(request.form.get(f"porcentaje_{i}"))
                locals()[f"monto_total_{i}"] = round(locals()[f"monto_{i}"] * (locals()[f"porcentaje_{i}"] / 100), 2)

                sublista_impuestos = [
                    locals()[f"impuesto_fijo_{i}"],
                    locals()[f"monto_{i}"],
                    locals()[f"porcentaje_{i}"],
                    locals()[f"monto_total_{i}"]
                ]

                impuestos_fijos.append(sublista_impuestos)

            except ValueError:
                pass

        session['impuestos_fijos'] = impuestos_fijos

        return render_template(
            "cuestionario_impuestos_fijos.html",
            producto=producto,
            impuestos_fijos=impuestos_fijos
        )

    else:
        producto = session.get("producto")

        impuestos_fijos = []

        session["impuestos_fijos"] = impuestos_fijos

        return render_template(
            "cuestionario_impuestos_fijos.html",
            producto=producto,
            impuestos_fijos=impuestos_fijos,
        )

@app.route("/cuestionario_costos_certificacion", methods=["GET", "POST"])
def cuestionario_costos_certificacion():
    if request.method == "POST":

        num_rows = int(request.form.get("rowCounter"))

        producto = session.get("producto")

        costos_certificacion = []

        for i in range(1, num_rows + 1):
            locals()[f"certificacion_{i}"] = request.form.get(f"certificacion_{i}")

            try:
                locals()[f"costo_{i}"] = float(request.form.get(f"costo_{i}"))
                locals()[f"porcentaje_{i}"] = float(request.form.get(f"porcentaje_{i}"))
                locals()[f"costo_total_{i}"] = round(locals()[f"costo_{i}"] * (locals()[f"porcentaje_{i}"] / 100), 2)

                sublista_certificacion = [
                    locals()[f"certificacion_{i}"],
                    locals()[f"costo_{i}"],
                    locals()[f"porcentaje_{i}"],
                    locals()[f"costo_total_{i}"]
                ]

                costos_certificacion.append(sublista_certificacion)

            except ValueError:
                pass

        session['costos_certificacion'] = costos_certificacion

        return render_template(
            "cuestionario_costos_certificacion.html",
            producto=producto,
            costos_certificacion=costos_certificacion
        )

    else:
        producto = session.get("producto")

        costos_certificacion = []

        session["costos_certificacion"] = costos_certificacion

        return render_template(
            "cuestionario_costos_certificacion.html",
            producto=producto,
            costos_certificacion=costos_certificacion
        )


@app.route("/cuestionario_costos_exportacion", methods=["GET", "POST"])
def cuestionario_costos_exportacion():
    if request.method == "POST":

        num_rows = int(request.form.get("rowCounter"))

        producto = session.get("producto")

        costos_exportacion = []

        for i in range(1, num_rows + 1):
            locals()[f"costo_exportacion_{i}"] = request.form.get(f"costo_exportacion_{i}")
            try:
                locals()[f"costo_unidad_{i}"] = float(request.form.get(f"costo_unidad_{i}"))
                locals()[f"unidades_consideradas_{i}"] = float(request.form.get(f"unidades_consideradas_{i}"))
                locals()[f"costo_total_{i}"] = round(locals()[f"costo_unidad_{i}"] * locals()[f"unidades_consideradas_{i}"], 2)
                sublista_exportacion = [
                    locals()[f"costo_exportacion_{i}"],
                    locals()[f"costo_unidad_{i}"],
                    locals()[f"unidades_consideradas_{i}"],
                    locals()[f"costo_total_{i}"]
                ]
                costos_exportacion.append(sublista_exportacion)
            except ValueError:
                pass

        session['costos_exportacion'] = costos_exportacion

        costos_certificacion = session.get("costos_certificacion")

        return render_template(
            "cuestionario_costos_exportacion.html",
            producto=producto,
            costos_exportacion=costos_exportacion,
        )

    else:
        producto = session.get("producto")
        cantidad_vendida = session.get("cantidad_vendida")

        costos_exportacion = []

        session["costos_exportacion"] = costos_exportacion

        return render_template(
            "cuestionario_costos_exportacion.html",
            producto=producto,
            costos_exportacion=costos_exportacion,
            cantidad_vendida=cantidad_vendida,
        )


@app.route("/analisis_final", methods=["GET"])
def analisis_final():
    session_data = {
        "insumos_actividades": "insumos_actividades",
        "trabajo_actividades": "trabajo_actividades",
        "sueldos_fijos": "sueldos_fijos",
        "costos_fijos": "costos_fijos",
        "impuestos_fijos": "impuestos_fijos",
        "impuestos_venta": "impuestos_venta",
        "costos_certificacion": "costos_certificacion",
        "costos_exportacion": "costos_exportacion"
    }
    data = {key: session.get(value) for key, value in session_data.items()}

    data["costos_totales"] = sys.float_info.epsilon  # El número más pequeño posible, para evitar dividir entre 0
    data["costos_autoempleo_totales"] = sys.float_info.epsilon

    variables_para_data = [
        "costos_laborales_actividades_totales",
        "costos_autoempleo_actividades_totales",
        "costos_empleo_actividades_totales",
        "costos_laborales_totales",
        "costos_laborales_totales_sin_autoempleo",
        "sueldos_fijos_totales",
        "sueldos_fijos_totales_sin_autoempleo",
        "sueldos_fijos_autoempleo",
        "costos_insumos_totales",
        "costos_insumos_actividades_totales",
        "costos_insumos_fijos_totales",
        "impuestos_fijos_totales",
        "costos_certificacion_totales",
        "costos_exportacion_totales"
    ]

    for nombre_variable in variables_para_data:
        data[nombre_variable] = 0

    producto = session.get("producto")
    cantidad_vendida = session.get("cantidad_vendida")
    unidad = session.get("unidad")

    lista_actividades_iteracion = ["insumos_actividades", "trabajo_actividades"]
    lista_costos_iteracion = ["impuestos_fijos", "costos_certificacion", "costos_exportacion"]

    try:
        for lst in lista_actividades_iteracion:
            for sublist in data[lst]:
                for row in sublist:
                    data["costos_totales"] += float(row[-1])
                    if len(row) == 7:
                        data["costos_laborales_actividades_totales"] += float(row[-1])
                        data["costos_laborales_totales"] += float(row[-1])
                        if row[-2] == "Sí":
                            data["costos_autoempleo_actividades_totales"] += float(row[-1])
                            data["costos_autoempleo_totales"] += float(row[-1])
                        else:
                            data["costos_empleo_actividades_totales"] += float(row[-1])
                            data["costos_laborales_totales_sin_autoempleo"] += float(row[-1])
                    else:
                        data["costos_insumos_totales"] += float(row[-1])
                        data["costos_insumos_actividades_totales"] += float(row[-1])
    except TypeError:
        pass

    try:
        for row in data["sueldos_fijos"]:
            data["costos_totales"] += float(row[-1])
            data["costos_laborales_totales"] += float(row[-1])
            data["sueldos_fijos_totales"] += float(row[-1])
            if row[-2] == "Sí":
                data["costos_autoempleo_totales"] += float(row[-1])
                data["sueldos_fijos_autoempleo"] += float(row[-1])
            else:
                data["costos_laborales_totales_sin_autoempleo"] += float(row[-1])
                data["sueldos_fijos_totales_sin_autoempleo"] += float(row[-1])
    except TypeError:
        pass

    try:
        for row in data["costos_fijos"]:
            data["costos_totales"] += float(row[-1])
            data["costos_insumos_totales"] += float(row[-1])
            data["costos_insumos_fijos_totales"] += float(row[-1])
    except TypeError:
        pass

    for nombre_lista in lista_costos_iteracion:
        try:
            for row in data[nombre_lista]:
                data["costos_totales"] += float(row[-1])
                data[nombre_lista + "_totales"] += float(row[-1])
        except TypeError:
            pass

    try:
        for row in data["impuestos_venta"]:
            row[1] = float(row[1]) / 100
    except TypeError:
        pass

    data["costos_totales_por_unidad"] = round(data["costos_totales"] / cantidad_vendida, 2)
    data["costos_totales_sin_autoempleo"] = round(data["costos_totales"] - data["costos_autoempleo_totales"], 2)
    data["costos_totales_por_unidad_sin_autoempleo"] = round(data["costos_totales_sin_autoempleo"] / cantidad_vendida, 2)
    data["costos_fijos_totales"] = round(data["sueldos_fijos_totales"] \
                                   + data["costos_insumos_fijos_totales"] + data["impuestos_fijos_totales"], 2)
    data["costos_fijos_totales_sin_autoempleo"] = round(data["sueldos_fijos_totales_sin_autoempleo"] \
                                   + data["costos_insumos_fijos_totales"] + data["impuestos_fijos_totales"], 2)
    data["costos_variables_totales"] = round(data["costos_laborales_actividades_totales"] + data["costos_insumos_actividades_totales"] \
                                       + data["costos_certificacion_totales"] + data["costos_exportacion_totales"], 2)
    data["costos_variables_totales_sin_autoempleo"] = round(data["costos_empleo_actividades_totales"] \
                                                      + data["costos_insumos_actividades_totales"] \
                                       + data["costos_certificacion_totales"] + data["costos_exportacion_totales"], 2)
    data["costos_variables_totales_por_unidad"] = round(data["costos_variables_totales"] / cantidad_vendida, 2)

    if data["costos_totales_sin_autoempleo"] == 0:
        data["costos_totales_sin_autoempleo"] = sys.float_info.epsilon  # El número más pequeño posible, para evitar dividir entre 0

    def div_entre_costos_totales(resultado_suma):
        return str(round((data[resultado_suma] / data["costos_totales"]) * 100, 2)) + "%"

    def div_entre_costos_totales_sin_autoempleo(resultado_suma):
        return str(round((data[resultado_suma] / data["costos_totales_sin_autoempleo"]) * 100, 2)) + "%"

    variables_para_tablas = {
        "costos_totales_sin_autoempleo_porcent_total": div_entre_costos_totales("costos_totales_sin_autoempleo"),
        "costos_fijos_totales_porcent_total": div_entre_costos_totales("costos_fijos_totales"),
        "costos_fijos_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_fijos_totales"),
        "costos_fijos_totales_sin_autoempleo_porcent_total": div_entre_costos_totales("costos_fijos_totales_sin_autoempleo"),
        "costos_fijos_totales_sin_autoempleo_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_fijos_totales_sin_autoempleo"),
        "costos_variables_totales_porcent_total": div_entre_costos_totales("costos_variables_totales"),
        "costos_variables_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_variables_totales"),
        "costos_variables_totales_sin_autoempleo_porcent_total": div_entre_costos_totales("costos_variables_totales_sin_autoempleo"),
        "costos_variables_totales_sin_autoempleo_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_variables_totales_sin_autoempleo"),
        "costos_laborales_actividades_totales_porcent_total": div_entre_costos_totales("costos_laborales_actividades_totales"),
        "costos_laborales_actividades_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_laborales_actividades_totales"),
        "costos_empleo_actividades_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_empleo_actividades_totales"),
        "costos_empleo_actividades_totales_porcent_total": div_entre_costos_totales("costos_empleo_actividades_totales"),
        "costos_autoempleo_actividades_totales_porcent_total": div_entre_costos_totales("costos_autoempleo_actividades_totales"),
        "costos_autoempleo_actividades_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_autoempleo_actividades_totales"),
        "sueldos_fijos_totales_porcent_total": div_entre_costos_totales("sueldos_fijos_totales"),
        "sueldos_fijos_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("sueldos_fijos_totales_sin_autoempleo"),
        "sueldos_fijos_totales_sin_autoempleo_porcent_total": div_entre_costos_totales("sueldos_fijos_totales_sin_autoempleo"),
        "sueldos_fijos_totales_sin_autoempleo_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("sueldos_fijos_totales_sin_autoempleo"),
        "sueldos_fijos_autoempleo_porcent_total": div_entre_costos_totales("sueldos_fijos_autoempleo"),
        "sueldos_fijos_autoempleo_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("sueldos_fijos_autoempleo"),
        "costos_laborales_totales_porcent_total": div_entre_costos_totales("costos_laborales_totales"),
        "costos_laborales_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_laborales_totales"),
        "costos_laborales_totales_sin_autoempleo_porcent_total": div_entre_costos_totales("costos_laborales_totales_sin_autoempleo"),
        "costos_laborales_totales_sin_autoempleo_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_laborales_totales_sin_autoempleo"),
        "costos_autoempleo_totales_porcent_total": div_entre_costos_totales("costos_autoempleo_totales"),
        "costos_autoempleo_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_autoempleo_totales"),
        "costos_insumos_totales_porcent_total": div_entre_costos_totales("costos_insumos_totales"),
        "costos_insumos_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_insumos_totales"),
        "costos_insumos_fijos_totales_porcent_total": div_entre_costos_totales("costos_insumos_fijos_totales"),
        "costos_insumos_fijos_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_insumos_fijos_totales"),
        "costos_insumos_actividades_totales_porcent_total": div_entre_costos_totales("costos_insumos_actividades_totales"),
        "costos_insumos_actividades_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_insumos_actividades_totales"),
        "impuestos_fijos_totales_porcent_total": div_entre_costos_totales("impuestos_fijos_totales"),
        "impuestos_fijos_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("impuestos_fijos_totales"),
        "costos_certificacion_totales_porcent_total": div_entre_costos_totales("costos_certificacion_totales"),
        "costos_certificacion_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_certificacion_totales"),
        "costos_exportacion_totales_porcent_total": div_entre_costos_totales("costos_exportacion_totales"),
        "costos_exportacion_totales_porcent_total_sin": div_entre_costos_totales_sin_autoempleo("costos_exportacion_totales")
    }

    data["costos_totales"] = round(data["costos_totales"], 2)
    data["costos_autoempleo_totales"] = round(data["costos_autoempleo_totales"], 2)

    return render_template(
        "analisis_final.html",
        producto=producto,
        unidad=unidad,
        cantidad_vendida=cantidad_vendida,
        **data,
        **variables_para_tablas,
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
