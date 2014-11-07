Sugar Pull Files
Plugin for Sublime Text 2

--

Plugin to connect out to GitHub based on a Pull Request Number or a Commit SHA, retrieves the files modified, and opens them relative to the current project open in Sublime. 

--

Install:

Take the contents of this repo, ZIP them up and rename to SugarPullFiles.sublime-package. Place this file in the following location:

/Users/{username}/Library/Application Support/Sublime Text 2/Installed Packages/

and restart Sublime Text 2.

--

Usage:

Navigate to Goto > Sugar Pull Files > Open Files from Pull Request/Commit

This will generate the Settings file, and prompt you to fill in the GitHub access key. Navigate to your GitHub profile page to generate a Personal Access Token:

https://github.com/settings/applications

Copy the Token and navigate in Sublime Text to Goto > Sugar Pull Files > Settings - User. Populate the gh_user value with the token, save and close the settings file.

Command - Shift - o will run the code, prompting for a Pull Request Number or Commit SHA, and opens the files modified in the pull/commit.

