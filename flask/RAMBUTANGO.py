#ToDo: Mantener separadas las variables de costos por categoría hasta sumarlas al último

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
        session['precio_venta'] = precio_venta
        session['ingreso_ventas'] = ingreso_ventas

        return render_template("ventas.html", producto=producto, cantidad_vendida=cantidad_vendida,
                               unidad=unidad, precio_venta=precio_venta, ingreso_ventas=ingreso_ventas)
    else:
        return render_template("ventas.html")


@app.route("/next_page")
def next_page():
    # Logic for the next page goes here
    return "Next Page"


if __name__ == "__main__":
    app.run(port=5000, debug=True)