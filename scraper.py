import urllib.request
from tropes import TropeDef
from bs4 import BeautifulSoup
import re

if __name__ == "__main__":
	# Jumping The Shark defines its media examples in Folders. TODO we have not yet accounted
	# for trope pages whose examples are split into separate pages of the site, i.e. Tsundere
	raw_html = urllib.request.urlopen('http://tvtropes.org/pmwiki/pmwiki.php/Main/JumpingTheShark').read()
	soup = BeautifulSoup(raw_html, 'html.parser')

	trope_def = TropeDef(soup.title.string)

	# TODO extract related tropes (But how do we scope control that?)
	all_folder_elements = soup.find_all("div", ["folderlabel", "folder"])

	# This defines types of media that are listed on TVTropes. The key is
	# the user-facing folder label, and the value is the prefix for URLs
	media_types = {
		"Film": "Film",
		"Comic Books": "ComicBook",
		"Fan Fics": "Fanfic",
		"Literature": "Literature",
		"Live-Action TV": "Series",
		"Anime": "Anime"
		# TODO not all types may have a public-facing folder name, some will appear inside broader categories
		# i.e. Manga inside Anime & Manga
		# TODO consider making the values lists to account for multiple media types appearing in the same folder
	}



	# Filter out folders that aren't for Media types
	media_folders = {}
	i = 0
	while i < len(all_folder_elements):
		element = all_folder_elements[i]

		folder_name = element.contents[0].strip()
		if element["class"][0] == "folderlabel":
			if folder_name in media_types.keys():
				# contents[0] for "folder" class is empty; text is stored in 1st element
				media_folders[folder_name] = all_folder_elements[i+1].contents[1]

				# TODO in some cases malformed HTML might leave a label without a folder after it
				i += 1
			else:
				print('Found a folder with unknown label: ' + folder_name)

		i += 1

	for folder, element in media_folders.items():
		# Links will use a different prefix than the user-facing folders
		link_prefix = media_types[folder]
		media_links = element.find_all("a", href=re.compile("^.*" + link_prefix + "/.*$"))


	print(trope_def)
