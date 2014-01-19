#STD library
import datetime
from datetime import date
from bson.objectid import ObjectId
import imghdr
import random
import string
import os
from PIL import Image

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
			get_db = User.objects.get(email=request.form["email"])
			if get_db.password == request.form["password"]:
				session["user"] = get_db.username
				return redirect(url_for('admin'))
	return render_template("login.html")

@elearning.route('/admin/')	
def admin():
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects.get(username=get_user)
		
	else:
		return redirect(url_for('index'))
		
	return render_template("admin/user-admin.html", user=user)

@elearning.route("/admin/setting-account", methods=["GET", "POST"])
def setting_account():
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects.get(username=get_user)
	else:
		return redirect(url_for('index'))
	
	if request.method == "POST":
		if request.form ["fullname"] and request.form ["email"] and request.form ["password"] and request.form["month"] and request.form["day"] and \
		request.form["year"] and request.form["gender"]:
			try:
				get_db = User.objects.get(username=get_user)
				get_db.fullname = request.form ["fullname"]
				get_db.email = request.form ["email"]
				get_db.password = request.form["password"]
				get_db.gender = request.form["gender"]
				get_db.birthday=date(int(request.form["year"]), int(request.form["month"]),int(request.form["day"]))
				get_db.save()
				print "sukses ganti %s" % (request.form ["fullname"])
				return redirect("/admin/setting-account")
			except NotUniqueError:
				return "Maaf %s sudah digunakan oleh orang lain" % (request.form ["email"])	
	return render_template("admin/user-setting-account.html", user=user)
	
@elearning.route("/admin/setting-profiles", methods=["GET", "POST"])	
def setting_profiles():
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects.get(username=get_user)
		profile = Profile.objects.get(author=user)
	else:
		return redirect(url_for('index'))
		
	if request.method == "POST":
		if request.form["alamat"] and request.form["phone"] and request.form["website"]:
			profile.alamat = request.form["alamat"]
			profile.phone = request.form["phone"]
			profile.website = request.form["website"]
			profile.save()
		
		if request.files["Image-Profile"]:
			img = request.files["Image-Profile"]
			if imghdr.what(request.files["Image-Profile"]) == None:
				return "Please Upload just Image Extension"
			
			try:
				os.remove("/home/fird0s/e-learning/static/uploads/photo_profile/%s" % (profile.profile_images_url)) 		
			except OSError:
				pass	
			
			
			rand = [random.choice(string.letters+string.digits) for x in xrange(35)]
			rand = "".join(rand)							
			
			request.files["Image-Profile"].save("/home/fird0s/e-learning/static/uploads/photo_profile/%s" % (rand) )
			profile.profile_images_url = rand
			profile.save()
			
			if os.stat("/home/fird0s/e-learning/static/uploads/photo_profile/"+profile.profile_images_url).st_size > 7641998:
				try:
					os.remove("/home/fird0s/e-learning/static/uploads/photo_profile/%s" % (profile.profile_images_url)) 		
					profile.profile_images_url = None
					profile.save()
					return "Please Upload less than 8 Mb"
				except OSError:
					return "ok"
			#compress jpg
			
			
		
	return render_template("admin/user-setting-profile.html", user=user, profile=profile)

@elearning.route("/admin/setting-jurnal", methods=["GET", "POST"])
def setting_jurnal():
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects(email=get_user)
	else:
		return redirect(url_for('index'))
	dbref= User.objects.get(email=get_user)
	dbprofile = Profile.objects.get(author=dbref)
	
	if request.method == "POST":
		if request.form["password"]:
			dbprofile.password_jurnal = request.form["password"]
			dbprofile.save()		
	return render_template("/admin/user-setting-journal.html", dbprofile=dbprofile)


@elearning.route("/admin/tambah-jurnal", methods=["GET", "POST"])
def tambah_jurnal():
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects(email=get_user)
	else:
		return redirect(url_for('index'))
	return render_template("/admin/user-tambah-jurnal.html", user=user)

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
