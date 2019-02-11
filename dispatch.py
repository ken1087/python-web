#!/user/bin/ python
#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, Response, make_response, url_for

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
if __name__ == "__main__":
	app.run(host = "192.168.0.201")

