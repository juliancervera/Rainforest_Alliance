#ToDo: Mantener separadas las variables de costos por categoría hasta sumarlas al último
#ToDo: Add a character limit to every input cell.

# La app va a funcionar con un número finito de actividades que formen parte del proceso productivo.


from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/ventas", methods=["GET", "POST"])
def ventas():
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


@app.route("/info_donativos")
def info_donativos():
    # Process the request or perform any other necessary actions
    return "You chose 'Yes' for receiving donativos."


@app.route("/pregunta_primera_actividad", methods=["GET", "POST"])
def pregunta_primera_actividad():
    if request.method == "POST":
        actividad = request.form.get("actividad")
        session["actividad_1"] = actividad
        return redirect("/info_actividades")
    else:
        producto = session.get("producto")
        return render_template("pregunta_primera_actividad.html", producto=producto)



@app.route("/info_actividades")
def info_actividades():
    actividad_1 = session.get("actividad_1")
    return f"The first activity is: {actividad_1}"


if __name__ == "__main__":
    app.run(port=5000, debug=True)