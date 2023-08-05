#! /usr/bin/env python
#coding=utf-8


WHITE_SPACE = "\r\n \t"

def cnenlen(s):
    return (len(s.decode("utf-8", "ignore").encode("gb18030", "ignore"))+1)//2

EMAIL_DICT = {
        "msn.com":("MSN", "http://login.live.com/"),
        "2008.sina.com":("新浪", "http://mail.2008.sina.com.cn/index.html"),
        "sina.com.cn":("新浪", "http://mail.sina.com.cn/index.html"),
        "vip.163.com":("163", "http://vip.163.com/"),
        "hongkong.com":("中华邮", "http://mail.china.com"),
        "sohu.com":("搜狐", "http://mail.sohu.com"),
        "live.com":("Live", "http://login.live.com/"),
        "eyou.com":("亿邮", "http://mail.eyou.com/"),
        "citiz.net":("Citiz", "http://citiz.online.sh.cn/citiz_index.htm"),
        "yeah.net":("Yeah", "http://mail.yeah.net/"),
        "vip.tom.com":("Tom", "http://vip.tom.com/"),
        "vip.qq.com":("QQ", "http://mail.qq.com/cgi-bin/loginpage?t=loginpage_vip&f=html"),
        "yahoo.com.hk":("雅虎", "http://mail.yahoo.com.hk"),
        "yahoo.cn":("雅虎", "http://mail.cn.yahoo.com/"),
        "188.com":("188", "http://www.188.com/"),
        "2008.china.com":("中华邮", "http://mail.china.com"),
        "vip.sohu.com":("搜狐", "http://mail.sohu.com"),
        "163.com":("163", "http://mail.163.com"),
        "126.com":("126", "http://www.126.com/"),
        "chinaren.com":("chinaren", "http://mail.chinaren.com"),
        "tom.com":("Tom", "http://mail.tom.com/"),
        "china.com":("中华邮", "http://mail.china.com"),
        "139.com":("139", "http://mail.139.com/"),
        "hotmail.com":("Hotmail", "http://www.hotmail.com"),
        "21cn.com":("21cn", "http://mail.21cn.com/"),
        "gmail.com":("Gmail", "http://mail.google.com"),
        "my3ia.sina.com":("新浪", "http://vip.sina.com.cn/index.html"),
        "yahoo.com.tw":("雅虎", "http://mail.yahoo.com.tw"),
        "vip.sina.com":("新浪", "http://vip.sina.com.cn/index.html"),
        "mail.china.com":("中华邮", "http://mail.china.com"),
        "263.net":("263", "http://mail.263.net/"),
        "yahoo.com":("雅虎", "https://login.yahoo.com/"),
        "foxmail.com":("Foxmail", "http://www.foxmail.com/"),
        "qq.com":("QQ", "http://mail.qq.com"),
        "sina.cn":("新浪", "http://vip.sina.com.cn/index.html"),
        "yahoo.com.cn":("雅虎", "http://mail.cn.yahoo.com/"),
        "sogou.com":("搜狗", "http://mail.sogou.com/"),
        "sina.com":("新浪", "http://mail.sina.com.cn/index.html"),
        "live.cn":("Live", "http://login.live.com/"),
}

import cgi
def email2link(email):
    if email:
        email = cgi.escape(email)
        e_domain = email.split(str('@'))[1]
        link = EMAIL_DICT.get(e_domain, None)
        if link:
            return """<a href="%s" target="_blank">%s</a>"""%(link[1], email)
    return email
