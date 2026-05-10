# from flask import (Flask,
#                    render_template,
#                    request)
# import os
#
# app = Flask(__name__)
#
# @app.route("/", methods=["GET", "POST"])
# def index():
#     result = None
#     selected_app = None
#     message = None
#     if request.method == "POST":
#
#         selected_app = request.form.get('app_name')
#         if selected_app:
#             message = f"вы выбрали: {selected_app} Доступ ограничен"
#
#         user_input = request.form.get("input")
#         result = f"Ты ввёл: {user_input}"
#     return render_template(
#         "index.html",
#         result=result, message=message)
#
#
# # if request.method == "POST":
# #     selected_app = request.form.get("app_name")
# #     if selected_app:
# #         message = f'вы выбрали: {selected_app}, доступ ограничен'
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lock')
def lock():
    return render_template('lock.html')

@app.route('/unlock', methods=['POST'])
def unlock():
    text = request.form.get('task')
    file = request.files.get('photo')

    if not text or not file:
        return "Заполни всё!", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
