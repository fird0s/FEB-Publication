#STD library
import datetime
from datetime import date
from bson.objectid import ObjectId
import imghdr
import random
import string
import os
from PIL import Image
from time import gmtime, strftime


#Flask library
from flask import *
elearning = Flask(__name__)

#MongoEngine library
from models import *


@elearning.route("/")
def index():
	get_all_user = User.objects
	get_all_profile = Profile.objects
	get_all_jurnal = Jurnal.objects[:10]
	return render_template("index.html", get_all_user=get_all_user, get_all_jurnal=get_all_jurnal, get_all_profile=get_all_profile)

@elearning.route('/contributor')
def contributor():
	get_db_user = User.objects
	get_db_profile = Profile.objects
	return render_template("contributor.html", get_db_user=get_db_user, get_db_profile=get_db_profile)
	
@elearning.route('/contributor/search-contributor')	
def search_contributor():
	data = request.args.get("name", "")
	if request.method == "GET":
		if request.args.get("name", ""):
			get_db_user =  User.objects(fullname__icontains = request.args.get("name", ""))
			get_db_profile = Profile.objects
		else:
			return redirect(url_for('contributor'))
			error = "Maaf tidak ada nama %s" % (data)
	return render_template("contributor-search.html", get_db_user=get_db_user, get_db_profile=get_db_profile, data=data)	
	

@elearning.route("/jurnal/")	
def search_jurnal():
	jurnal = request.args.get("jurnal", "no")
	if request.method == "GET":
		if request.args.get("jurnal", ""):
			get_all_user = User.objects
			get_all_profile = Profile.objects
			get_all_jurnal = Jurnal.objects(jurnal_name__icontains = request.args.get("jurnal", ""))
			
		else:
			return redirect(url_for('index'))
			error = "Maaf tidak ada jurnal %s" % (jurnal)
	return render_template("jurnal-search.html", get_all_user=get_all_user, get_all_jurnal=get_all_jurnal, get_all_profile=get_all_profile, jurnal=jurnal)
	
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
			
			if len(request.form["username"]) < 7:
				return "please fill username > 8 character"
			
			if len(request.form["password"]) < 7:		
				return "please fill your password > 8 character"
			try:
				user = User(_id = str(ObjectId()), username=request.form["username"], fullname=request.form["fullname"], email=request.form["email"], \
				password=request.form["password"], birthday=date(int(request.form["birth-year"]), int(request.form["birth-month"]), \
			         int(request.form["birth-day"])), gender=request.form["gender"], date_joined=datetime.datetime.now()) 
				
				user.save()
				
				profile = Profile(author=user, website="www.fe.unsyiah.ac.id", date_added=datetime.datetime.now())
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
			try:
				get_db = User.objects.get(email=request.form["email"])
				if get_db.password == request.form["password"]:
					session["user"] = get_db.username
					return redirect(url_for('admin'))
				else:
					return "Maaf Password/Email anda salah"	
			except DoesNotExist:	
				return "Maaf Email anda belum terdaftar"
	return render_template("login.html")

@elearning.route('/admin/')	
def admin():
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects.get(username=get_user)
		
	else:
		return redirect(url_for('login'))
	myjurnal = list(Jurnal.objects(author = user).limit(10))
	myjurnal.reverse()
	return render_template("admin/user-admin.html", user=user, myjurnal=myjurnal)

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
		if request.form["alamat"] and request.form["phone"] and request.form["website"] and request.form["emergency-call"] and request.form["about-my-self"]:
			profile.alamat = request.form["alamat"]
			profile.phone = request.form["phone"]
			profile.emergency_call = request.form["emergency-call"]
			profile.website = request.form["website"]
			profile.about = request.form["about-my-self"]
			profile.save()
		
		if request.files["Image-Profile"]:
			img = request.files["Image-Profile"]
			if imghdr.what(request.files["Image-Profile"]) == None:
				return "Please Upload just Image Extension"
			
			try:
				os.remove("/home/fird0s/e-learning/static/uploads/photo_profile/%s" % (profile.profile_images_url)) 		
			except OSError:
				pass	
			
			
			rand = [random.choice(string.letters+string.digits) for x in xrange(25)]
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
		user = User.objects.get(username=get_user)
	else:
		return redirect(url_for('index'))
	get_db = Profile.objects.get(author=user)	
	if request.method == "POST":
		if request.form["password"]:
			
			get_db.password_jurnal = request.form["password"]
			get_db.save()		
	return render_template("/admin/user-setting-journal.html", user=get_db, nama=user)


@elearning.route("/admin/tambah-jurnal", methods=["GET", "POST"])
def tambah_jurnal():
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects.get(username=get_user)
	else:
		return redirect(url_for('index'))
	get_all_cat = Kategori.objects
	
	if request.method == "POST":
		if request.form["jurnal-category"] == "Economic":
			return "Maaf Anda Belum Memilih Kategori"		
		if not request.files["jurnal-files"]:	
			return "Maaf anda belum memilih jurnal untuk diupload"
		
		
		if request.form["jurnal-category"] and request.form["jurnal-name"] and request.form["jurnal-summary"]:
			get_db = Jurnal(author=user, jurnal_name=request.form["jurnal-name"], date_added=datetime.datetime.now(), kategori=request.form["jurnal-category"], summary=request.form["jurnal-summary"])
			get_db.save()
		
		rand = [random.choice(string.letters+string.digits) for x in xrange(10)]
		rand = "".join(rand)
		
		if request.files["jurnal-files"]:
			try:
				os.makedirs("/home/fird0s/e-learning/static/uploads/jurnal/"+get_user)
				namefile = request.files["jurnal-files"].filename
				namefile = namefile.replace(" ", "-") + strftime("#%a%d%b%H:%M:%S", gmtime())
				request.files["jurnal-files"].save("/home/fird0s/e-learning/static/uploads/jurnal/"+get_user+"/"+namefile)
				get_db.jurnal_location = namefile
				get_db.save()
				return "thanks for upload new jurnal, see your jurnal <a href='%s'>here</a>" % ( url_for('admin') )
			except OSError:
				namefile = request.files["jurnal-files"].filename
				namefile = namefile.replace(" ", "-") + strftime("#%a%d%b%H:%M:%S", gmtime())
				request.files["jurnal-files"].save("/home/fird0s/e-learning/static/uploads/jurnal/"+get_user+"/"+namefile)
				get_db.jurnal_location = namefile
				get_db.save()
				return "thanks for upload new jurnal, see your jurnal <a href='%s'>here</a>" % ( url_for('admin') )
					
				
	return render_template("/admin/user-tambah-jurnal.html", user=user, get_all_cat=get_all_cat)

@elearning.route('/admin/edit_jurnal/<route>', methods=["GET", "POST"])
def edit_jurnal(route):
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects.get(username=get_user)
	else:
		return redirect(url_for('index'))
	get_all_cat = Kategori.objects
	get_db = Jurnal.objects.get(pk = ObjectId(route))
	get_userr = User.objects.get(username = get_user)
	if get_user != get_userr.username:
		return "You have not permission to edit this"
	
	if request.method == "POST":
		if request.form["jurnal-name"] and request.form["jurnal-category"] and request.form["jurnal-summary"]:
			get_db.jurnal_name = request.form["jurnal-name"]
			get_db.kategori = request.form["jurnal-category"]
			get_db.summary = request.form["jurnal-summary"]
			get_db.save()
				
		if request.files["jurnal-files"]:
			os.remove("/home/fird0s/e-learning/static/uploads/jurnal/"+get_user+"/"+get_db.jurnal_location) 
			namefile = request.files["jurnal-files"].filename
			namefile = namefile.replace(" ", "-") + strftime("#%a%d%b%H:%M:%S", gmtime())
			request.files["jurnal-files"].save("/home/fird0s/e-learning/static/uploads/jurnal/"+get_user+"/"+namefile)
			get_db.jurnal_location = namefile
			get_db.save()
		
		
	return render_template("admin/user-edit-jurnal.html", user=user, get_db=get_db, get_all_cat=get_all_cat)

@elearning.route("/admin/hapus/jurnal/<route>")
def hapus_jurnal(route):
	if "user" in session:
		get_user = session.get("user", None)
		user = User.objects.get(username=get_user)
	else:
		return redirect(url_for('index'))	
		
	get_db = Jurnal.objects.get(pk = ObjectId(route))
	os.remove("/home/fird0s/e-learning/static/uploads/jurnal/"+get_user+"/"+get_db.jurnal_location)
	get_db.delete()
	return redirect(url_for('admin'))


@elearning.route("/view/jurnal/<route>")
def view_jurnal(route):
	return render_template("view-jurnal.html")
	
@elearning.route("/admin/logout")
def admin_logout():	
	session.pop("user", None)				
	return redirect(url_for('index'))
	
	
@elearning.route('/user/<username>')
def user(username):
	get_username = User.objects.get(username=username)
	get_profile = Profile.objects.get(author = get_username)
	return render_template("user.html", get_username=get_username, get_profile=get_profile)		
	
@elearning.route('/user/<username>/recent-post')	
def user_recent_post(username):	
	get_username = User.objects.get(username=username)
	get_profile = Profile.objects.get(author = get_username)
	get_user = User.objects.get(username=username)
	get_jurnal = Jurnal.objects(author=get_user)
	return render_template("user-recent-post.html", get_username=get_username, get_profile=get_profile, get_jurnal=get_jurnal)
	
@elearning.route('/about')
def about():
	return render_template("about.html")		
		

if __name__ == "__main__":
	elearning.secret_key = '_Wx0ksck~\[p99923@#@!#!@#423raakleas'
	elearning.run(debug=True)
	elearning.run()
