from selenium import webdriver
from sys import version_info
import time, selenium
#a selenium based webscraper for the iihs's car crash videos
#made for Centree
#by Austin Spalding
#Python 2.7.9
#Selenium 3.4.1
#Firefox 53.0.2
#Geckodriver 0.16.1

#check Python version > 2
py3 = version_info[0] > 2

#credentials
authEmail = ''
authPass = ''
dest = ''
if py3:
	authEmail = input("email: ")
	authPass = input("password: ")
	dest = input("target folder's full filepath: ")
else:
	authEmail = raw_input("email: ")
	authPass = raw_input("password: ")
	dest = raw_input("target folder's full filepath: ")

#profile setup for downloading
firefoxProfile = webdriver.FirefoxProfile()
firefoxProfile.set_preference("browser.download.panel.shown", False)
firefoxProfile.set_preference("browser.download.folderList", 2)
firefoxProfile.set_preference("browser.download.manager.showWhenStarting", False)
firefoxProfile.set_preference("browser.download.dir", dest)
firefoxProfile.set_preference("browser.helperApps.neverAsk.saveToDisk", "video/mpeg, application/avi, application/wmv")

#entry
browser = webdriver.Firefox(firefox_profile = firefoxProfile)
browser.get('https://techdata.iihs.org')
sleepCount = 2
loginButton = None
while not loginButton:
	try:
		loginButton = browser.find_element_by_link_text('login')
	except:
		time.sleep(sleepCount)
		sleepCount = sleepCount * 2
loginButton.click()

#login
sleepCount = 2
emailBox = None
while not emailBox:
	try:
		emailBox = browser.find_element_by_xpath("/html/body/form/div[@id='mainContent']/div/fieldset/div/div[@class='AspNet-Login-UserPanel']/input")
		passBox = browser.find_element_by_xpath("/html/body/form/div[@id='mainContent']/div/fieldset/div/div[@class='AspNet-Login-PasswordPanel']/input")
		loginButton = browser.find_element_by_xpath("/html/body/form/div[@id='mainContent']/div/fieldset/div/div[@class='AspNet-Login-SubmitPanel']/input")
	except:
		time.sleep(sleepCount)
		sleepCount = sleepCount * 2
emailBox.send_keys(authEmail)
passBox.send_keys(authPass)
loginButton.click()

#newPageGodDAMMIT
sleepCount = 2
downloadsButton = None
while not downloadsButton:
	try:
		downloadsButton = browser.find_element_by_link_text('downloads')
	except:
		time.sleep(sleepCount)
		sleepCount = sleepCount * 2
downloadsButton.click()

#filePage
sleepCount = 2
crashList = None
while not crashList:
	try:
		crashList = browser.find_elements_by_class_name('testinfo')
	except:
		time.sleep(sleepCount)
		sleepCount = sleepCount * 2
notDone = True
count = 0
while notDone:
	subCount = 0
	for i in range(len(crashList)):
		for x in range(count):
			sleepCount = 2
			nextButton = None
			while not nextButton:
				try:
					nextButton = browser.find_element_by_xpath("html/body/form/div[@id='mainContent']/div/div/span/div/table[@class='pager']/tbody/tr/td[5]/input")
				except:
					time.sleep(sleepCount)
					sleepCount = sleepCount * 2
			nextButton.click()
		print str(count) + ": " + str(subCount)
		sleepCount = 2
		crashList = None
		while not crashList:
			try:
				crashList = browser.find_elements_by_class_name('testinfo')
			except:
				time.sleep(sleepCount)
				sleepCount = sleepCount * 2
		if len(crashList) < 25:
			notDone = False
		crashTest = None
		sleepCount = 2
		while not crashTest:
			try:
				crashTest = crashList[subCount]
			except:
				crashList = browser.find_elements_by_class_name('testinfo')
				time.sleep(sleepCount)
				sleepCount = sleepCount * 2
		crashTest.click()
		videoPresent = False
		triedAll = False
		sleepCount = 2
		pageLoad = None
		while not videoPresent and not pageLoad:
			try:
				pageLoad = browser.find_element_by_class_name('folder-List')
				#print "folders found"
			except:
				pageLoad = None
				#print "folders not found"
			try:
				videoButton = browser.find_element_by_link_text('Video')
				videoPresent = True
				videoButton.click()
				#print "Video found"
			except selenium.common.exceptions.NoSuchElementException:
				videoPresent = videoPresent or False
				#print "Video not found"
			try:
				videosButton = browser.find_element_by_link_text('Videos')
				videoPresent = True
				videosButton.click()
				#print "Videos found"
			except selenium.common.exceptions.NoSuchElementException:
				videoPresent = videoPresent or False
				#print "Videos not found"
			try:
				videoCapButton = browser.find_element_by_link_text('VIDEO')
				videoPresent = True
				videoCapButton.click()
				#print "VIDEO found"
			except selenium.common.exceptions.NoSuchElementException:
				videoPresent = videoPresent or False
				#print "VIDEO not found"
			time.sleep(sleepCount)
			if sleepCount < 32:
				sleepCount = sleepCount * 2
		if videoPresent:
			sleepCount = 2
			crashVids = None
			while not crashVids:
				try:
					crashVids = browser.find_elements_by_class_name('filename')
				except:
					time.sleep(sleepCount)
					sleepCount = sleepCount * 2
			for video in crashVids:
				video.click()
		downloadsButton = None
		sleepCount = 2
		while not downloadsButton:
			try:
				downloadsButton = browser.find_element_by_link_text('downloads')
			except:
				time.sleep(sleepCount)
				sleepCount = sleepCount * 2
		downloadsButton.click()
		subCount +=1
	count += 1
browser.quit()