import json
import urllib2
import subprocess
import os

def github_latest_release(user,repo):
	SUPPORTED_TYPES=['dmg','zip','gz']
	DEST=str(u'https://api.github.com/repos/%s/%s/releases' % (user,repo))
	data = json.load(urllib2.urlopen(DEST))
	try:
		latest_release = data[0]['assets'][0]['browser_download_url']
		for t in SUPPORTED_TYPES:
			if latest_release.lower().endswith(t):
				return latest_release
	except:
		pass	
	return None

def get_dsa_signature(file,private_key):
    p1 = subprocess.Popen(['openssl','dgst','-sha1','-binary',file], stdout=subprocess.PIPE)
    if p1.wait() != 0:
        return None

    p2 = subprocess.Popen(['openssl','dgst','-dss1' ,'-sign', private_key], stdin=p1.stdout, stdout=subprocess.PIPE)
    if p1.wait() != 0:
        return None

    p3 = subprocess.Popen(['openssl','enc','-base64'], stdin=p2.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p2.stdout.close()

    output = p3.communicate()[0].strip()

    if p3.returncode != 0:
        return None
    
    return output

def delete_file_on_change(sender,instance,attr):
    try:
        pre_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False

    old_file = getattr(pre_instance, attr,None)
    new_file = getattr(instance, attr,None)

    if old_file and not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

def delete_file_on_delete(instance,attr):
    file = getattr(instance, attr,None)
    if file and os.path.isfile(file.path):
        os.remove(file.path)


