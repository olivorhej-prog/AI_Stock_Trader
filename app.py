
from flask import Flask, render_template_string
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Stock Trader</title>
    <style>
        body {
            margin: 0;
            padding: 25px;
            background: #101827;
            color: white;
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 850px;
            margin: auto;
        }
        .card {
            background: #1e293b;
            padding: 22px;
            border-radius: 14px;
            margin-bottom: 18px;
        }
        h1 { color: #34d399; }
        .value {
            font-size: 35px;
            font-weight: bold;
        }
        .stock {
            display: flex;
            justify-content: space-between;
            padding: 14px 0;
            border-bottom: 1px solid #334155;
        }
        .green { color: #34d399; }
    </style>
</head>
<body>
<div class="container">
    <h1>AI STOCK TRADER</h1>
    <p class="green">● VIRTUEL HANDEL</p>

    <div class="card">
        <p>Samlet porteføljeværdi</p>
        <div class="value">{{ total }} kr.</div>
    </div>

    <div class="card">
        <h2>Min økonomi</h2>
        <p>Kontanter: {{ saldo }} kr.</p>
        <p>Aktieværdi: {{ aktievaerdi }} kr.</p>
        <p>Gevinst/tab: {{ gevinst }} kr.</p>
    </div>

    <div class="card">
        <h2>Mine aktier</h2>
        {% for navn, aktie in aktier.items() %}
        <div class="stock">
            <span>{{ navn }}</span>
            <strong>{{ aktie.antal }} stk.</strong>
        </div>
        {% endfor %}
    </div>

    <div class="card">
        <h2>Robotstatus</h2>
        <p class="green">Dashboard online</p>
        <p>Automatisk analyse: Planlagt kl. 23.00</p>
    </div>
</div>
</body>
</html>
"""

@app.route("/")
def dashboard():
    with open("portfolio.json", "r", encoding="utf-8") as fil:
        data = json.load(fil)

    saldo = data["saldo"]
    aktier = data["aktier"]

    total = saldo
    aktievaerdi = 0

    for navn, aktie in aktier.items():
        vaerdi = aktie["antal"] * aktie["koebspris"]
        aktievaerdi += vaerdi

    total += aktievaerdi
    gevinst = total - data["startkapital"]

    return render_template_string(
        HTML,
        saldo=round(saldo, 2),
        aktievaerdi=round(aktievaerdi, 2),
        total=round(total, 2),
        gevinst=round(gevinst, 2),
        aktier=aktier
    )

if __name__ == "__main__":
    app.run(debug=True)
