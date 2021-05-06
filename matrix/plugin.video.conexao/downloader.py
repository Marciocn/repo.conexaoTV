import xbmcgui
import xbmc
import time
import os
import urllib.request as urllib

def notify(msg):
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % ('Kodi', msg, 1000, ''))
    

def download(url, name, dest, dp = None):
    global start_time
    start_time=time.time()
    if not dp:
        dp = xbmcgui.DialogProgress()          
        dp.create('Baixando '+name+'...','Por favor aguarde...')            
    dp.update(0)
    try:
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
    except:
        try:
            os.remove(dest)
        except:
            pass
 
def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = int(min((numblocks*blocksize*100)/filesize, 100))
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
        kbps_speed = numblocks * blocksize / (time.time() - start_time)
        if kbps_speed > 0:
            eta = (filesize - numblocks * blocksize) / kbps_speed
        else:
            eta = 0
        kbps_speed = kbps_speed / 1024
        total = float(filesize) / (1024 * 1024)
        msg = '%.02f MB de %.02f MB\n' % (currently_downloaded, total)
        msg += '[COLOR yellow]Velocidade:[/COLOR] %.02d Kb/s ' % kbps_speed
        msg += '[COLOR yellow]Tempo Restante:[/COLOR] %02d:%02d' % divmod(eta, 60)   
        dp.update(percent, msg)
    except:
        percent = 100
        dp.update(percent)
    if percent == 100:
        notify('Download concluído.')
    elif dp.iscanceled(): 
        dp.close()
        raise notify('Download parado.')
#checkintegrity13122019
