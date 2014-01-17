#STD library
import datetime
from datetime import date
from bson.objectid import ObjectId

#Flask library
from flask import *
elearning = Flask(__name__)

#MongoEngine library
from models import *


@elearning.route("/")
def index():
	return render_template("index.html")

@elearning.route('/contributor')
def contributor():
	return render_template("contributor.html")
	
@elearning.route('/register', methods=["GET", "POST"])
def register():
	if "user" in session:
		return redirect("admin")
	if request.method == "POST":
		if request.form["fullname"] and request.form["username"] and request.form["email"] and request.form["password"] and request.form["confirm_password"] \
		and request.form["birth-month"] and request.form["birth-day"] and request.form["birth-year"] and request.form["gender"] :
			if request.form["password"] != request.form["confirm_password"]:
				return "Your Password Does Not Match"
			
			#save to database
			try:
				user = User(_id = str(ObjectId()), username=request.form["username"], fullname=request.form["fullname"], email=request.form["email"], \
				password=request.form["password"], birthday=date(int(request.form["birth-year"]), int(request.form["birth-month"]), \
			         int(request.form["birth-day"])), gender=request.form["gender"], date_joined=datetime.datetime.now()) 
				
				user.save()
				
				profile = Profile(author=user, alamat="None", phone="0852", website="www.fe.unsyiah.ac.id", date_added=datetime.datetime.now())
				profile.save()
				
				return "Thanks %s for register, please  <a href='/login'>login here</a>" % (request.form["fullname"])			
			except NotUniqueError:
				return "Maaf Email/Username anda sudah teregister"	
			
			except ValidationError:
				return "Maaf Ada kesalahan"	
			
			
					
				
	return render_template("register.html")	
	
	
@elearning.route('/login', methods=["GET", "POST"])
def login():
	if "user" in session:
		return redirect(url_for('admin'))
	if request.method == "POST":
		if request.form["email"] and request.form["password"]:
			checklogin = User.objects(email=request.form["email"])
			for checklogin in checklogin:
				if checklogin.password != request.form["password"]:
					return "Error Username atau Password"
				else:
					session["user"] = request.form["email"]
					print "success"
					return redirect(url_for('admin')) 
			
	return render_template("login.html")

@elearning.route('/admin/')	
def admin():
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects(email=get_user)
	else:
		return redirect(url_for('index'))
		
	return render_template("admin/user-admin.html", user=user)

@elearning.route("/admin/setting-account", methods=["GET", "POST"])
def setting_account():
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects(email=get_user)
	else:
		return redirect(url_for('index'))
	
	if request.method == "POST":
		if request.form ["fullname"] and request.form ["email"] and request.form ["password"] and request.form["month"] and request.form["day"] and \
		request.form["year"] and request.form["gender"]:
			ganti = User.objects(email=get_user)
			for ganti in ganti:
				ganti.fullname = request.form ["fullname"]
				ganti.email = request.form ["email"]
				ganti.password = request.form ["password"]
				ganti.gender = request.form["gender"]
				ganti.birthday=date(int(request.form["year"]), int(request.form["month"]),int(request.form["day"]))
				session.pop("user", None)				
				session["user"] = request.form["email"]
				ganti.save()
				print "sukses ganti %s" % (request.form ["fullname"])
				return redirect("/admin/setting-account")
				
				
	
	return render_template("admin/user-setting-account.html", user=user)
	
@elearning.route("/admin/setting-profiles", methods=["GET", "POST"])	
def setting_profiles():
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects(email=get_user)
		for check in user:
			data = Profile(author=check._id)
	else:
		return redirect(url_for('index'))
		
	if request.method == "POST":
		if request.form["alamat"] and request.form["phone"] and request.form["website"]:
			return "ok"		
	return render_template("admin/user-setting-profile.html", user=user, data=data)

@elearning.route("/admin/logout")
def admin_logout():	
	session.pop("user", None)				
	return redirect(url_for('index'))
	
@elearning.route('/user/<email>')
def user(email):
	return render_template("user.html")		
	
@elearning.route('/about')
def about():
	return render_template("about.html")		
		

if __name__ == "__main__":
	elearning.secret_key = '_Wx0ksck~\[p99923@#@!#!@#423raakleas'
	elearning.run(debug=True)
	elearning.run()
