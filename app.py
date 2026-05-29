from flask import Flask, render_template, request, redirect, url_for
from waitress import serve
import mariadb, sys, os, dotenv

WAITRESS = False

dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("KEY")

envuser = os.getenv("DB_USER")
envpassword = os.getenv("DB_PASSWORD")
envhost = os.getenv("DB_HOST")

def get_db_connection():
    try:
        conn = mariadb.connect(
            user=envuser,
            password=envpassword,
            host=envhost,
            port=3306,
            database="lab_db"
        )
        return conn
    except mariadb.Error as e:
        print(f"Feil ved tilkobling til MariaDB: {e}")
        sys.exit(1)

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, navn, epost FROM brukere")
    brukere = cursor.fetchall()
    conn.close()
    return render_template("index.html", brukere=brukere)


@app.route("/bruker/<navn>")
def bruker(navn):
    return render_template("bruker.html", navn=navn)


@app.route("/legg-til", methods=["GET", "POST"])
def legg_til():
    if request.method == "POST":
        navn = request.form["navn"]
        epost = request.form["epost"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO brukere (navn, epost) VALUES (?, ?)",
            (navn, epost)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("legg_til.html")

if __name__ == "__main__":
    if not WAITRESS:
        app.run(debug=True, host="0.0.0.0", port=5000)
    else:
        serve(app, host="0.0.0.0", port=8080)