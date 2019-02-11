#!/user/bin/ python
#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, Response, make_response, url_for, render_template, request, session

app = Flask(__name__)
app.debug = True

@app.route("/log")
def IoT_logging_test():
	test_value = 20190211
	app.logger.debug("디버깅 시행중")
	app.logger.warning(str(test_value) + "=====")
	app.logger.error("에러발생")
	return "로거 끝"

@app.route("/user/<uname>")
def IoT_user_name(uname):
	return "User Name : %s" %uname

@app.route("/user/<int:num_id>")
def IoT_user_number_id(num_id):
	return "ID Number : %d" % num_id

@app.route("/get_test", methods=["GET"])
def get_test():
	if request.method == "GET":
		if (request.args.get("uname") == "iot"
				and request.args.get("passwd") == "2019"):
			return request.args.get("uname") + "님 환영합니다."
		else:
			return "로그인 실패"
	else:
		return "다시 시도해 주세용"

@app.route("/board", methods=['GET'])
#def IoT_Board():
def board_list_get():
#	print("IoT_Board")
#	return "<img src=\"https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png\">"
	return "GET"
@app.route("/board", methods=['POST'])
#def IoT_http_prepost_response():
def board_list_post():
#	return "<img src=" + url_for("static", filename = "1.png") + ">"
	return "POST"

@app.route("/login_test")
def login_test():
	session["logged_in"] = False
	return render_template("login.html")

@app.route("/login", methods=["POST","GET"])
def login():
	if request.method == "POST":
		session_cheak = request.form.get("uname", None)
		if None == session_cheak:
			if "logged_in" in session:
				return session["uname"] + "님 환영합니다."
			else:
				return login_test()
		if (request.form["uname"] == "iot"
				and request.form["passwd"] == "2019"):
			session["logged_in"] = True
			session["uname"] = request.form["uname"]
			return request.form["uname"] + "님 환영합니다."
		else:
			return "로그인 실패"
	else:
#return "잘못된 접근"
		try:
			if session["logged_in"] == True:
				return session["uname"] + "님 환영합니다."
			else:
				return login_test() 
		except:
			return login_test()

app.secret_key = "iot_key"

if __name__ == "__main__":
	app.run(host = "192.168.0.201")

