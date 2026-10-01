"""VulnShop: tienda de ejemplo con vulnerabilidades intencionales (OWASP Top 10)."""
import hashlib
import os
import pickle
import sqlite3
import subprocess

import requests
import yaml
from flask import Flask, redirect, render_template_string, request

from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

DB_PATH = os.path.join(os.path.dirname(__file__), "shop.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    return conn


@app.route("/")
def index():
    return "<h1>VulnShop</h1><a href='/search?q=mouse'>Buscar</a>"


# A03 Injection: SQL armado con f-string
@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = get_db()
    rows = conn.execute(f"SELECT name, price FROM products WHERE name LIKE '%{q}%'").fetchall()
    return {"results": rows}


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + hash_password(password) + "'"
    cursor.execute(query)
    return "ok" if cursor.fetchone() else ("credenciales inválidas", 401)


# A02 Cryptographic Failures: MD5 sin sal
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# A03 Injection: command injection
@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    output = subprocess.check_output("ping -c 1 " + host, shell=True)
    return output


@app.route("/disk")
def disk():
    path = request.args.get("path", "/")
    return os.popen("du -sh " + path).read()


# Ejecución de código arbitrario
@app.route("/calc")
def calc():
    expr = request.args.get("expr", "1+1")
    return str(eval(expr))


# A08 Insecure Deserialization
@app.route("/cart/import", methods=["POST"])
def import_cart():
    cart = pickle.loads(request.data)
    return {"items": len(cart)}


@app.route("/config/import", methods=["POST"])
def import_config():
    cfg = yaml.load(request.data, Loader=yaml.Loader)
    return {"keys": list(cfg.keys())}


# A10 SSRF
@app.route("/preview")
def preview():
    url = request.args.get("url")
    resp = requests.get(url, verify=False)
    return resp.text


# A03 XSS / SSTI
@app.route("/hello")
def hello():
    name = request.args.get("name", "invitado")
    return render_template_string("<h2>Hola " + name + "</h2>")


# A01 Open redirect
@app.route("/go")
def go():
    return redirect(request.args.get("next", "/"))


if __name__ == "__main__":
    # A05 Security Misconfiguration
    app.run(host="0.0.0.0", port=5000, debug=True)
