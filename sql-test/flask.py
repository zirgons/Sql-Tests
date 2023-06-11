from flask import Flask, render_template, redirect, request, url_for
import mysql.connector

app = Flask(__name__)
com = []
men = ["Janvārī", "Februārī", "Martā", "Aprīlī", "Maijā", "Jūnijā", "Jūlijā", "Augustā", "Septembrī", "Oktobrī", "Novembrī", "Decembrī"];



@app.route('/', methods=["GET", "POST"])
def index():
    db = mysql.connector.connect(
      host="Zirgons.mysql.pythonanywhere-services.com",
      user="Zirgons",
      passwd="Laja2323",
      database="Zirgons$Viesi"
    )
    cur = db.cursor()

    if request.method == "GET":
        cur.execute("SELECT Autors, Komentars, Datums FROM Viesi")
        rez=cur.fetchall();
        com = [];
        for i in range(len(rez)):
            cur.execute(f"SELECT Menesis, Diena FROM Vardi WHERE Vards = '{rez[i][0].capitalize()}';")
            vd=cur.fetchall();
            if(vd):
                menesis = men[vd[0][0]-1];
                com.append(rez[i]+(menesis, vd[0][1]));
            else:
                com.append(rez[i]);
        db.close()
        return render_template("main.html", comments=com)

    values = (request.form["autors"], request.form["komentars"])
    sql = "INSERT INTO Viesi (Autors, Komentars) VALUES (%s,%s)"
    cur.execute(sql,values)
    db.commit()
    db.close()
    return redirect(url_for('index'))