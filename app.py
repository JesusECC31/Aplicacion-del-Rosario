import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from info.misericordia import CORONILLA

app = Flask(__name__, template_folder="htmls", static_folder="cosas")
app.config["UPLOAD_FOLDER"] = "cosas/uploads"
app.secret_key = "emaus_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

PASSWORD = "Emaus3132"

LOGIN_BG = "fondos/fondo_login.jpg"
GENERAL_BG = "fondos/fondo_general.jpg"
ROSARIO_BG = "fondos/imagen_rosario.jpg"
MISERICORDIA_BG = "fondos/imagen_misericordia.jpg"

CURRENT_BG_FILE = "cosas/uploads/fondo_actual.txt"

def create_tables():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password(PASSWORD)
        db.session.add(admin)
        db.session.commit()

def get_general_background():
    if os.path.exists(CURRENT_BG_FILE):
        with open(CURRENT_BG_FILE, "r") as f:
            ruta = f.read().strip()
            if ruta:
                return ruta
    return GENERAL_BG

def set_general_background(path):
    with open(CURRENT_BG_FILE, "w") as f:
        f.write(path)

REFLEXIONES = [
    "El Señor camina contigo incluso cuando no lo sientes. Su luz guía tus pasos.",
    "Dios te sostiene en silencio y fortalece tu corazón cuando más lo necesitas.",
    "Jesús nunca abandona a quien confía en Él. Su amor es tu refugio seguro.",
    "La paz de Dios supera todo entendimiento. Entrégale tus cargas hoy.",
    "El Espíritu Santo te acompaña y te renueva. Su presencia trae vida.",
    "Dios abre caminos donde tú ves muros. Confía en su poder y su tiempo.",
    "Jesús toca tu corazón cada día. Ábrele y deja que transforme tu vida.",
    "La misericordia de Dios es nueva cada mañana. Hoy es un buen día para volver a Él.",
    "El amor de Dios es más grande que tus miedos. Descansa en su fidelidad.",
    "Dios conoce tus luchas y tus lágrimas. Él nunca te deja solo.",
    "El Señor fortalece tu espíritu cuando te sientes débil. Su gracia te sostiene.",
    "Jesús te llama por tu nombre. Su amor nunca se cansa de buscarte.",
    "Dios ilumina tu camino aun en la noche más oscura. Confía en Él.",
    "El Espíritu Santo te guía suavemente. Escucha su voz en tu corazón.",
    "Dios transforma tu dolor en crecimiento. Nada se pierde en sus manos.",
    "Jesús es tu paz en medio de la tormenta. Su presencia calma tu alma.",
    "El Señor te abraza en tus silencios. Él entiende lo que no puedes decir.",
    "Dios te da fuerzas nuevas cada día. Su amor es tu descanso.",
    "Jesús camina delante de ti abriendo caminos. No temas avanzar.",
    "El Espíritu Santo renueva tu interior. Su luz te hace libre.",
    "Dios nunca llega tarde. Su tiempo es perfecto y lleno de amor.",
    "Jesús sana lo que duele en tu corazón. Déjalo obrar en ti.",
    "El Señor te sostiene cuando sientes que caes. Él es tu roca firme.",
    "Dios escucha incluso tus suspiros. Nada pasa desapercibido para Él.",
    "Jesús te acompaña en cada paso. Su amor es tu refugio seguro.",
    "El Espíritu Santo te da claridad cuando todo parece confuso.",
    "Dios te abraza con ternura en tus momentos de cansancio.",
    "Jesús te invita a descansar en Él. Su paz es verdadera.",
    "El Señor te guía con paciencia. Él sabe lo que necesitas.",
    "Dios transforma tus miedos en valentía. Confía en su fuerza.",
    "Jesús ilumina tu vida con esperanza. Su amor nunca falla.",
    "El Espíritu Santo te inspira a seguir adelante con fe.",
    "Dios te sostiene incluso cuando no lo ves. Él está contigo.",
    "Jesús te ofrece su mano cada día. No caminas solo.",
    "El Señor te da paz cuando tu corazón se inquieta.",
    "Dios te acompaña en cada batalla. Su victoria es tuya.",
    "Jesús te recuerda que eres amado. Su amor es eterno.",
    "El Espíritu Santo te fortalece en tus debilidades.",
    "Dios abre puertas que nadie puede cerrar. Confía en Él.",
    "Jesús te guía con amor y verdad. Síguelo sin miedo.",
    "El Señor te renueva cuando te sientes agotado.",
    "Dios te protege con su amor fiel. Descansa en Él.",
    "Jesús te invita a confiar más y temer menos.",
    "El Espíritu Santo te llena de serenidad y luz.",
    "Dios te sostiene con su mano poderosa.",
    "Jesús te acompaña en cada amanecer.",
    "El Señor te cubre con su misericordia.",
    "Dios te recuerda que nunca estás solo.",
    "Jesús te fortalece con su presencia viva.",
]

def obtener_reflexion_del_dia():
    hoy = datetime.now()
    dia = hoy.timetuple().tm_yday
    return REFLEXIONES[dia % len(REFLEXIONES)] if REFLEXIONES else ""

# ⭐⭐⭐ LOGIN CORREGIDO (ÚNICO CAMBIO)
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")

        if password == PASSWORD:
            session["logueado"] = True
            return redirect(url_for("home"))

        flash("Contraseña incorrecta", "error")
        return redirect(url_for("login"))

    return render_template("login.html", fondo=LOGIN_BG)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if not username or not password or not confirm_password:
            flash("Complete todos los campos", "error")
        elif password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
        elif User.query.filter_by(username=username).first():
            flash("El usuario ya existe", "error")
        else:
            nuevo_usuario = User(username=username)
            nuevo_usuario.set_password(password)
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash("Registro exitoso. Ingresa con tu nueva cuenta", "success")
            return redirect(url_for("login"))
    return render_template("register.html", fondo=GENERAL_BG)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if not session.get("logueado"):
        return redirect(url_for("login"))
    fondo = get_general_background()
    reflexion = obtener_reflexion_del_dia()
    return render_template("home.html", fondo=fondo, reflexion_del_dia=reflexion)

@app.route("/rosario_completo")
def rosario_completo():
    if not session.get("logueado"):
        return redirect(url_for("login"))
    return render_template("rosario_completo.html", fondo=ROSARIO_BG)

@app.route("/divina_misericordia")
def divina_misericordia():
    if not session.get("logueado"):
        return redirect(url_for("login"))
    return render_template("divina_misericordia.html", fondo=MISERICORDIA_BG, coronilla=CORONILLA)

@app.route("/cambiar_fondo", methods=["GET", "POST"])
def cambiar_fondo():
    if not session.get("logueado"):
        return redirect(url_for("login"))
    if request.method == "POST":
        if "imagen" in request.files:
            archivo = request.files["imagen"]
            if archivo and archivo.filename:
                ruta = os.path.join(app.config["UPLOAD_FOLDER"], "fondo_personal.jpg")
                archivo.save(ruta)
                set_general_background("uploads/fondo_personal.jpg")
                flash("Fondo actualizado correctamente")
        if "quitar" in request.form:
            set_general_background("")
            flash("Fondo restablecido al predeterminado")
    return render_template("cambiar_fondo.html", fondo=get_general_background())

@app.route("/oraciones_del_rosario")
def oraciones_del_rosario():
    if not session.get("logueado"):
        return redirect(url_for("login"))
    return render_template("oraciones_del_rosario.html", fondo=MISERICORDIA_BG)

@app.route("/cambiar_contraseña", methods=["GET", "POST"])
def cambiar_contraseña():
    if not session.get("logueado"):
        return redirect(url_for("login"))
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        username = session.get("username")
        user = User.query.filter_by(username=username).first() if username else None
        if not user:
            flash("No se encontró el usuario de sesión", "error")
        elif not user.check_password(current_password):
            flash("Contraseña actual incorrecta", "error")
        elif new_password != confirm_password:
            flash("Las nuevas contraseñas no coinciden", "error")
        else:
            user.set_password(new_password)
            db.session.commit()
            flash("¡Contraseña cambiada exitosamente!", "success")
    fondo = get_general_background()
    return render_template("cambiar_contraseña.html", fondo=fondo)

if __name__ == "__main__":
    os.makedirs("cosas/uploads", exist_ok=True)
    with app.app_context():
        create_tables()
    app.run(host="0.0.0.0", port=5000, debug=True)
