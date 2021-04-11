from bs4 import BeautifulSoup
import requests as req
import hashlib

def get_beautifulsoup(url):
	resp = req.get(url, 
					headers={"User-Agent":"Chrome/80.0.3987.163"}, 
					proxies={"http":"127.0.0.1:8080"}
					)
	return BeautifulSoup(resp.content, 'html.parser')

def main():
	app_url = 'https://scopely.com'
	used_plugins = ['backwpup', 'auto-terms-of-service-and-privacy-policy', 'rocket-lazy-load', 'cookiebot']
	
	# # Get all used plugins
	for i in range(1, 50):
		print('-----------------------')
		url = 'https://wordpress.org/plugins/browse/popular/page/' + str(i) +  '/'
		print(url)
		doc = get_beautifulsoup(url)
		
		plugin_links = doc.select("#main > article > div.entry > header > h3 > a") # get all plugins
		for a_link in plugin_links:
			plugin = a_link['href'].split('/')[-2]
			print('Plugin ' + plugin, end='')
			resp = req.get(app_url + '/wp-content/plugins/' + plugin + '/')
			if resp.status_code != 500:
				print('\t\t\t\t: used!')
				used_plugins.append(plugin)
			else:
				print('\t\t\t\t: [x]')

	print(used_plugins)

	# plug = '|'.join(sorted(used_plugins))
	# print('Password: Flag{' + hashlib.md5(plug.encode()).hexdigest() + "}")


if __name__ == '__main__':
	main()