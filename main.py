from flask import *
elearning = Flask(__name__)

@elearning.route("/")
def index():
	return render_template("index.html")

@elearning.route('/contributor')
def contributor():
	return render_template("contributor.html")
	
@elearning.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		if request.form["fullname"] and request.form["email"] and request.form["password"] and request.form["confirm_password"] \
		and request.form["birth-month"] and request.form["birth-day"] and request.form["birth-year"] and request.form["gender"] :
			if request.form["password"] != request.form["confirm_password"]:
				return "Your Password Does Not Match"
			return "ok"	
	return render_template("register.html")	
	
@elearning.route('/login', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		if request.form["email"] and request.form["password"]:
			return "OK"
	return render_template("login.html")
	
@elearning.route('/user')
def user():
	return render_template("user.html")		
	
@elearning.route('/about')
def about():
	return render_template("about.html")		
		

if __name__ == "__main__":
	elearning.run()
