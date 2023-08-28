import socket
import ssl
from bs4 import BeautifulSoup

def parse_url(url): 
    scheme, url = url.split("://", 1) 
    assert scheme in ["http","https"], "Unknown scheme {}".format(scheme)
    if "/" not in url:
        url = url + "/" 
    host, path = url.split("/", 1) 
    return (scheme, host, "/" + path)

def request(url):
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )
    scheme, host, path = parse_url(url)
    port = 80 if (scheme == "http") else 443
    if ':' in host:
        host,port = host.split(':',1)
        port = int(port)

    s.connect((host, port))
    if (scheme == "https"):
        s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
    s.send("GET {} HTTP/1.0\r\n".format(path).encode("utf8") + 
        "Host: {}\r\n\r\n".format(host).encode("utf8"))

    response = s.makefile("r", encoding="utf8", newline="\r\n")

    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)

    headers = {}
    while True:
        line = response.readline()
        if line == "\r\n": break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()

    body = response.read()
    s.close()
    return headers,body
    
def load(url):
    headers, body = request(url)
    print(headers)
    body = BeautifulSoup(body,"html.parser").prettify()
    print(body)

if __name__ == "__main__":
    import sys
    load(sys.argv[1])