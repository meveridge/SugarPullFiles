import sublime
import sublime_plugin
import urllib2
from base64 import encodestring
import json

def RepresentsInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

class SugarPullFilesCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global proj_folder_path, gh_user

		window = sublime.active_window()
		proj_folder_path = window.folders()[0]

		gh_user = ""

		try:
			ocf_settings = sublime.load_settings("Preferences.SugarPullFiles-settings")
			gh_user = ocf_settings.get("gh_user","")
			ocf_settings.set("gh_user",gh_user)
			sublime.save_settings("Preferences.SugarPullFiles-settings")
			
			if gh_user == "":
				print 'No settings'
				sublime.error_message("GitHub Access Key not set. Please check settings in GoTo > Sugar Pull Files")
				self.result = False
			else:
				window.show_input_panel("Pull Request Number or Commit SHA:", "", self.on_done, None, None)
		except NameError:
			print 'No settings'
			sublime.error_message("GitHub Access Key not set. Please check settings in GoTo > Sugar Pull Files")
			self.result = False

	def on_done(self, input):

		#if integer, its a pull number
		if RepresentsInt(input):
			self.getFilesFromPull(input)
		else:
			#else try commit sha
			self.getFilesFromCommitSHA(input)

	def getFilesFromPull(self, pullNumber):
		# Retreive modified files list from GitHub
		# Based on Pull Request Number

		request_url = "https://api.github.com/repos/sugarcrm/Mango/pulls/"+pullNumber+"/files"
		response_data = self.apiRequestToGitHub(request_url)
		self.openFiles(response_data)

	def getFilesFromCommitSHA(self, commitSHA):
		# Retreive modified files list from GitHub
		# Based on Comitt SHA

		request_url = "https://api.github.com/repos/sugarcrm/Mango/commits/"+commitSHA
		response_data = self.apiRequestToGitHub(request_url)
		self.openFiles(response_data["files"])

	def apiRequestToGitHub(self,url):
		# Perform REST call to GitHub
		# To retreive file list

		try:
			request = urllib2.Request(url)
			base64string = encodestring('%s:%s' % (gh_user, '')).replace('\n', '')
			request.add_header('Authorization', 'Basic %s' % base64string)
			r = urllib2.urlopen(request)
			rJSON = r.read()
			request_data = json.loads(rJSON)

			return request_data
		except (urllib2.HTTPError) as (e):
			err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
		except (urllib2.URLError) as (e):
			err = '%s: URL error %s contacting API' % (__name__, str(e.reason))

		sublime.error_message(err)
		self.result = False

	def openFiles(self,response_data):
		# Open each modified file relative to current project

		for changed_file in response_data:
			file_path = changed_file["filename"][9:]
			sublime.active_window().open_file(proj_folder_path +'/'+ file_path)
			print 'Opening file: ' + file_path

