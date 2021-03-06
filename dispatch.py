#!/user/bin/ python
#-*=coding:utf-8-*-
import sys
from subprocess import PIPE, Popen 
import psutil
import requests
import RPi.GPIO as GPIO
reload(sys)
from camera import Camera
sys.setdefaultencoding('utf8')
from flask import Flask, Response, make_response, url_for, render_template, request, session, redirect 
from bs4 import BeautifulSoup

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

@app.route("/logout")
def logout():
	session["logged_in"] = False
	session.pop("uname", None)
	return "로그아웃 되셨습니다."

@app.route("/login_test")
def login_test():
	return render_template("login.html")

@app.route("/login", methods=["POST","GET"])
def login():
	if request.method == "POST":
		session_cheak = request.form.get("uname", None)
		if None == session_cheak:
			if "logged_in" in session:
				if True == session["logged_in"]:
					return session["uname"] + "님 환영합니다."
			return login_test()
		if (request.form["uname"] == "iot"
				and request.form["passwd"] == "2019"):
			session["logged_in"] = True
			session["uname"] = request.form["uname"]
			return request.form["uname"] + "님 환영합니다."
		return "로그인 실패"
	else:
#return "잘못된 접근"
		if "logged_in" in session:
			if True == session["logged_in"]:
				return session["uname"] + "님 환영합니다."
		return login_test()

@app.route("/template")
@app.route("/template/")
@app.route("/template/<iot_number>")
def template_test(iot_number=None):
	iot_members = ["최성주", "주수홍", "최재원","kangin"]
	return render_template("template_test.html", iot_number=iot_number, iot_members=iot_members)

@app.route("/iot")
@app.route("/iot/")
def iot():
#	result_req		= requests.get("http://busanit.ac.kr/p/?j=41")
#	result_req		= requests.get("https://media.daum.net/")
#	result_req		= requests.get("https://media.daum.net/ranking/bestreply/")
	result_req		= requests.get("https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=105")
	result_txt		= result_req.text
	result_head		= result_req.headers
	result_status	= result_req.status_code
	if True == result_req.ok:
		obj_soup	= BeautifulSoup(result_txt, "html.parser")
#		iot_data	= obj_soup.select("table.ej-tbl>tbody>tr>td>a")
#	iot_data	= obj_soup.select("div.box_headline>ul.list_headline>li>strong.tit_g>a")
#		iot_data	= obj_soup.select("div.cont_thumb>strong.tit_thumb>a")
		iot_data	= obj_soup.select("div.cluster_body>ul.cluster_list>li.cluster_item>div.cluster_text>a")
		return render_template("main.html", iot_data = iot_data)
	else:
		return "가져오기 실패"

@app.route("/gugu")
@app.route("/gugu/")
@app.route("/gugu/<int:iot_num>")
def iot_gugu(iot_num=None):
	return render_template("gugu.html", iot_num = iot_num)

@app.route("/calcul", methods=["POST"])
def calcul(iot_num=None):
	if request.method == "POST":
		if "" == request.form["iot_num"]:
			cal_num = None
		else:
			cal_num = request.form["iot_num"]
	else:
		cal_num = None
	return redirect(url_for("iot_gugu", iot_num = cal_num))

@app.route("/test_temp")
def iot_test_temp():
	iot_string = "파이썬ㄷㄷㄷㄷㄷ"
	iot_list = (1000, 1324, 5745, 2458, 3456)
	return render_template('template.html', my_string = iot_string, my_list = iot_list)

def iot_measure_temp():
	process = Popen(["vcgencmd", "measure_temp"], stdout=PIPE) 
	output, _error = process.communicate() 
	return float(output[output.index("=") + 1:output.rindex("'")])

@app.route("/info")
def iot_sys_info():
#=====================================================
	cpu_temp			= iot_measure_temp()
	cpu_percent         = psutil.cpu_percent() 
	cpu_count           = psutil.cpu_count()
#=====================================================
	memory				= psutil.virtual_memory()
	mem_total			= memory.total
	mem_percent			= memory.percent
#=====================================================
	hd_disk				= psutil.disk_usage("/")
	disk_percent		= hd_disk.percent
#=====================================================

	iot_sys_info_dict	= {
						    "CPU 온도"		:cpu_temp
							,"CPU 사용율"	:cpu_percent
							,"CPU 갯수"		:cpu_count
							,"전체메모리"	:mem_total
							,"메모리사용율"	:mem_percent
							,"하드디스크"	:disk_percent}

	return render_template("hw_info.html", hw_info = iot_sys_info_dict)

LedPin = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(LedPin,GPIO.OUT)

@app.route("/led/<iot_state>")
def Led_OnOff(iot_state):
	if "on"		== iot_state:
		GPIO.output(LedPin, GPIO.HIGH)
	if "off"	== iot_state:
		GPIO.output(LedPin, GPIO.LOW)
	if "toggle" == iot_state:
		GPIO.output(LedPin, not GPIO.input(LedPin))
	return iot_sys_info()

@app.route("/camera")
def iot_camera():
	return render_template("camera.html")

def iot_camera_start(camera): 
	while True: 
		frame = camera.get_frame() 
		yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n") 
		    
@app.route("/camera_run") 
def iot_camera_run(): 
	return Response(iot_camera_start(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")

app.secret_key = "iot_key"

if __name__ == "__main__":
	app.run(host = "192.168.0.201")

