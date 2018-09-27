# encoding: utf-8
import requests
import yagmail
from system.config import EMAIL_HOST, EMAIL_PASSWORD, EMAIL_USER

# 链接邮箱服务器
yag = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASSWORD, host=EMAIL_HOST)

# 邮箱正文
contents = ["这是一个测试邮件","谢谢大家"]

# 发送邮件
yag.send(["walry666@163.com"], "测试邮件", contents=contents)