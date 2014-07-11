import json
import urllib2

def github_latest_release(user,repo):
    DEST=str(u'https://api.github.com/repos/%s/%s/releases' % (user,repo))
    data = json.load(urllib2.urlopen(DEST))
    try:
    	latest_release = data[0]['assets'][0]['browser_download_url']
    	return latest_release
    except:
    	return None
