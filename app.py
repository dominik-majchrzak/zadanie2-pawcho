from flask import Flask, request, render_template_string
import datetime
import requests
import os

app = Flask(__name__)

AUTHOR = "Dominik Majchrzak"
PORT = int(os.environ.get("PORT", 5000))
API_KEY = os.environ.get("WEATHER_API_KEY", "demo") 

TEMPLATE = """
<!doctype html>
<title>Weather App</title>
<h2>Wybierz kraj i miasto</h2>
<form method="POST">
  <select name="city">
    <option value="Warsaw">Polska - Warszawa</option>
    <option value="London">Wielka Brytania - Londyn</option>
    <option value="Berlin">Niemcy - Berlin</option>
    <option value="Tokyo">Japonia - Tokio</option>
  </select>
  <input type="submit" value="Pokaż pogodę">
</form>
{% if weather %}
  <h3>Pogoda w {{ city }}:</h3>
  <p>Temperatura: {{ weather["main"]["temp"] }}°C</p>
  <p>Opis: {{ weather["weather"][0]["description"] }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    city = None
    if request.method == "POST":
        city = request.form["city"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=pl"
        response = requests.get(url)
        if response.ok:
            weather = response.json()
    return render_template_string(TEMPLATE, weather=weather, city=city)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    print(f"[{datetime.datetime.now()}] Aplikacja uruchomiona przez {AUTHOR} na porcie {PORT}", flush=True)
    app.run(host="0.0.0.0", port=PORT)
