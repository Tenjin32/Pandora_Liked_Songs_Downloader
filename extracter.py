from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import sys
import time
import os.path

#<div class show_more tracklike> is show more
def Parse_Source():
	names = []
	author = []
	with open('source.html','r') as f:
		soup = BeautifulSoup(f,'html.parser')
	
	for link in soup.find_all('a',{'class':'first'}):
		names.append(link.getText())

	for p in soup.find_all('p',{'class':'s-0 line-h-1_4'}):
		try:
			if p.a.has_attr('href') == True:
				if "Radio" not in p.a.getText():
					author.append(p.a.getText())
		except:
			dongle = 1

	for i in range(len(names)):
		if os.isfile('songs.txt'):
			os.remove('songs.txt')

		with open('songs.txt','w') as f:
			f.write(names[i] + " - " + author[i] + "\n")




def Extract_Songs(email="",password=""):
	email = input("Please enter Pandora Email ")
	password = input("Please enter Pandora Password ")
	print("Gathering liked songs, This could take a while \n Please keep your mouse out of the window at all times.")
	driver = webdriver.Firefox()
	driver.set_window_size(100,100)
	try:
		driver.get("http://www.pandora.com/account/sign-in")
		login_Email = driver.find_element_by_name("email")
		login_Password = driver.find_element_by_name("password")
		login_Email.send_keys(email)
		login_Password.send_keys(password)
		login_Password.send_keys(Keys.RETURN)
		time.sleep(2)
		driver.find_element_by_class_name("userNameImage").click()
		driver.find_element_by_class_name("profileMenuItem").click()
		time.sleep(1)
		driver.find_element_by_id("body").send_keys(Keys.SPACE)
		time.sleep(2)
		driver.find_element_by_id("profile_tab_likes").click()
		time.sleep(2)
	except:
		print("An Error has occured")
		driver.close()
	try:
		for i in range(0,50):
			driver.execute_script("document.querySelectorAll('.show_more.tracklike')["+str(i)+"].click()")
			time.sleep(1)
	except:
		if os.path.isfile('source.html'):
			os.remove('source.html')
			with open('source.html','w') as f:
				f.write(driver.page_source)

		else:
			with open('source.html','w') as f:
				f.write(driver.page_source)

	driver.close()
try:
	if str(sys.argv[1]) == "update":
		Extract_Songs()
		Parse_Source()
except:
	print("\n")

if os.path.isfile('source.html') == True:
	print("Please use the argument update to update your song list")
	Parse_Source()
else:
	Extract_Songs()
	Parse_Source('source.html')


