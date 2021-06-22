# -*- coding: utf-8 -*-

import urllib, urllib2, sys, re, os, unicodedata,urlparse
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser
h = HTMLParser()		
##############################################################################################
plugin_handle = int(sys.argv[1])
mysettings = xbmcaddon.Addon(id = 'plugin.video.Meuguia.Tv')
addon_name = 'Meuguia.Tv'
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanarts = xbmc.translatePath(os.path.join(home, 'fanart2.jpg'))
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
base = 'https://www.meuguia.tv/'
dialog = xbmcgui.Dialog()    
#############################################################################################
def contar_acessos():
	try:
		req = urllib2.Request('https://goo.gl/sb9b22')
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
	except:
		pass
	#return link
	
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def add_link(name,url,mode,iconimage,fanart,description):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
		cmItems = []
		if mode==4:
			cmItems.append(('[COLOR gold]Próximos Programas[/COLOR]',  'XBMC.RunPlugin(%s?url=%s&mode=3&name=%s&iconimage=%s&description=%s)'%(sys.argv[0],urllib.quote_plus(url),urllib.quote_plus(name),urllib.quote_plus(iconimage),urllib.quote_plus(description))))
		liz.addContextMenuItems(cmItems, replaceItems=False)
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok
#############################################################################################	
params = dict(urlparse.parse_qsl(sys.argv[2].replace('/?','/&')))
url = params.get("url")
name = params.get("name")
mode = int(params.get("mode",'0'))
iconimage = params.get("iconimage")
description = params.get("description")

if mode==0:
	contar_acessos()
	link = abrir_url(base)
	fas = BeautifulSoup(link,convertEntities=BeautifulSoup.HTML_ENTITIES)
	add_link(fas.h1.text.encode('utf-8'),base,4,icon, fanarts,'-')
	match = fas.findAll('li')
	for a in match:
		names = '[COLOR white]'+a.h2.text.encode('utf-8')+':[/COLOR]\n[COLOR darkseagreen]'+h.unescape(a.h3.text.encode('utf-8'))+'[/COLOR]'
		urls = base+a.a['href']
		add_link(names,urls,1,icon, fanarts,'d')
		
elif mode == 1:
	fa = abrir_url(url)
	fas = BeautifulSoup(fa)
	match = fas.findAll('li')
	for a in match:
			description = '%s' % a.findAll('h3')
			try:
				names = '[COLOR white]'+h.unescape(a.h2.string.encode('utf-8'))+'[/COLOR]'+'\n[COLOR darkseagreen]%s[/COLOR]' % h.unescape(a.findAll('h3')[0].text.encode('utf-8').replace('&nbsp;',' ').replace('    ',': '))
			except: pass
			try:
				urls = base + a.a.get('href')
			except: urls = ''
			add_link(names,urls,4,icon,fanarts,description)
elif mode==3:
	soup = BeautifulSoup(description)
	items = name+'\n\n'
	ad = []
	for a in soup.findAll('h3'):
		arq = a.text.encode('utf-8').replace('&nbsp;',' ').replace('    ','  ')
		try:
			arqs = h.unescape(arq)
		except:
			arqs = arq
		ad.append(arqs)
	cont = len(ad)	
	for b in range(0,int(cont)):
		try:
			items += '\n'+ad[b]
		except: pass
	dialog.textviewer(addon_name,items)
	sys.exit()	
	
elif mode==4:	
	fa = abrir_url(url)
	fas = fa.replace('\t','')
	match = re.compile('(<li.*?</a></li>)').findall(fas.split('<ul class="mw">')[1].replace('\n',''))
	for i in match:
		ad = re.compile("""<li(.*)class="devicepadding" href="(.*?)">.*?>(.*?)<.*?<h2>(.*?)<.h2><h3>(.*?)<.h3>(.*?</a></li>)""").findall(i)
		for a1,a2,a3,a4,a5,a6 in ad:
			try:
				add_link('[COLOR aquamarine]%s[/COLOR]' % a1.split('devicepadding">')[1].split('</li>')[0],base,100,icon, fanart,'-')
			except:
				pass
			if '<div class="noar">' in a6:
				agora = '  [COLOR red]%s[/COLOR]' % re.compile('<div class="noar">(.*?)</div>').findall(a6)[0]
			else:
				agora = ''#white
			add_link('[COLOR white]%s[/COLOR]\n[COLOR lime]%s[/COLOR] | [COLOR darkseagreen]%s[/COLOR]' % (a4+agora,a3,a5),base+a2,5,icon, fanarts,'-')
elif mode==5:	
	link = abrir_url(url)
	soup = BeautifulSoup(link, convertEntities=BeautifulSoup.HTML_ENTITIES)
	programa = soup.title.text.encode('utf-8').replace('| meuguia.TV','')
	add_link('[COLOR lime]%s[/COLOR]' % programa,base,100,icon, fanart,'-')
	fas = link.replace('\t','')
	match = re.compile('(<li.*?</a></li>)').findall(fas.split('<li class="subheader devicepadding">')[1].replace('\n',''))
	for a in match:
			for b in re.compile('<h2>(.*?)<.h2>\s*<h3>(.*?)<.h3>(.*?<.a>\s*<.li>)').findall(a):
				dia = b[0].replace('Dom','Domingo').replace('Seg','Segunda-feira').replace('Ter','Terça-feira').replace('Qua','Quarta-feira').replace('Qui','Quinta-feira').replace('Sex','Sexta-feira').replace('Sáb','Sábado').replace(',',' , ')
				emisora =  b[1]
				if '<div class="noar">' in b[2]:
					agora = '  [COLOR red]%s[/COLOR]' % re.compile('<div class="noar">(.*?)</div>').findall(b[2])[0]
				else:
					agora = ''
				add_link('[COLOR white]%s[/COLOR]\n[COLOR darkseagreen]%s[/COLOR]' % (emisora,dia+agora),url,100,icon, fanarts,'-')
elif mode==100:
	sys.exit()
	
	
	
	
	
	
	
	
xbmcplugin.endOfDirectory(plugin_handle)