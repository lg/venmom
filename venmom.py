# Venmom 0.01 by Larry Gadea <trivex@gmail.com>.

USERNAME = "" #can also be your phone number
PASSWORD = ""

MINIMUM = 20.00 #can be anything though venmo will ask questions if < $1.00
MAXIMUM = 500.00 #currently venmo enforces a maximum of $500.00/day

#########################################

import urllib2
import re
import sys
from urllib2 import HTTPRedirectHandler, build_opener
from datetime import timedelta, datetime

sessionid = ""
class SwipeCookieHandler(HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        global sessionid
        sessionid = re.search("sessionid=(.*?); expires", headers["Set-Cookie"]).group(1)
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
        result.status = code
        return result

if USERNAME == "" or PASSWORD == "":
    print "You havent edited the script to specify your username and password"
    sys.exit()

req = urllib2.Request("https://venmo.com")
res = urllib2.urlopen(req).read()

csrf = re.search("name='csrfmiddlewaretoken' value='(.*?)'", res).group(1)

opener = build_opener(SwipeCookieHandler)
opener.addheaders = [
    ("Referer", "https://venmo.com/"),
    ('Cookie', "csrftoken=%s" % csrf),
]
opener.open("https://venmo.com/account/login", "csrfmiddlewaretoken=%s&next=%%2F&username=%s&password=%s&login_button=Login" % (csrf, USERNAME, PASSWORD))

if not sessionid:
    print "Failed to log in"
    sys.exit()

#########################################

req = urllib2.Request("https://venmo.com/account/settings/withdraw-money", headers={
    "Referer": "https://venmo.com/",
    "Cookie": "sessionid=%s; csrftoken=%s" % (sessionid, csrf)
})
res = urllib2.urlopen(req).read()

balance = float(re.search("\<td\>\$(.*?)\<\/td\>", res).group(1))
balance = min(balance, MAXIMUM)

if balance < MINIMUM:
    print "Your balance ($%.2f) is less than the minimum required to continue as specified in this script ($%.2f)." % (balance, MINIMUM)
    sys.exit()

balance = "%.2f" % balance

csrf = re.search("name='csrfmiddlewaretoken' value='(.*?)'", res).group(1)

#########################################

req = urllib2.Request("https://venmo.com/account/settings/confirm-withdrawal", 
    "csrfmiddlewaretoken=%s&amount=%s&ip_address=%s&stage=pre-confirm" % (csrf, balance, ip_address),
    {
        "Referer": "https://venmo.com/account/settings/withdraw-money",
        "Cookie": "sessionid=%s; csrftoken=%s" % (sessionid, csrf)
    }
)
res = urllib2.urlopen(req).read()

csrf = re.search("name='csrfmiddlewaretoken' value='(.*?)'", res).group(1)

#########################################

# the implementation of venmo's auditing is questionable at best. until they fix it,
# the time/ip is passed in from the clientside.
req = urllib2.Request("http://whatismyip.org")
ip_address = urllib2.urlopen(req).read()

est_time = (datetime.now() + timedelta(hours=3))
timestamp = est_time.strftime("%Y-%m-%d+%H%%3A%M%%3A%S.") + str(est_time.microsecond)

req = urllib2.Request("https://venmo.com/account/settings/confirm-withdrawal", 
    "csrfmiddlewaretoken=%s&ip_address=%s&amt=%s&stage=confirmed&timestamp=%s" % (csrf, ip_address, balance, timestamp),
    {
        "Referer": "https://venmo.com/account/settings/withdraw-money",
        "Cookie": "sessionid=%s; csrftoken=%s" % (sessionid, csrf)
    }
)
res = urllib2.urlopen(req).read()

if "Details of your confirmed withdrawal request" not in res:
    print "Failed to do the transfer"
else:
    print "Success -- Transferred $%s!" % balance