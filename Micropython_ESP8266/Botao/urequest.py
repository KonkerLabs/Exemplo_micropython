import usocket
import ubinascii
import json

def urlopen(url, user=None, passwd=None, data=None, method="GET"):
    if data is not None and method == "GET":
        method = "POST"
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)

    token = ''
    if (user is not None and passwd is not None):
        token = ubinascii.b2a_base64(b'%s:%s' % (user, passwd)).strip()
        #print(token)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    #print("HOST:", host, "PORT", port)

    ai = usocket.getaddrinfo(host, port)
    addr = ai[0][4]
    s = usocket.socket()
    s.connect(addr)
    if proto == "https:":
        s = ussl.wrap_socket(s)

    s.write(method)
    s.write(b" /")
    s.write(path)
    s.write(b" HTTP/1.0\r\nHost: ")
    s.write(host)
    s.write(b"\r\n")
    if (token):
        s.write(b"Authorization: Basic ")
        s.write(token)
        s.write(b"\r\n")

    s.write(b"Content-Type: application/json\r\n")

    if data:
        s.write(b"Content-Length: ")
        s.write(str(len(data)))
        s.write(b"\r\n")
    s.write(b"\r\n")

    if data:
        s.write(data)

    rcv_data = ''
    while True:
        newdata = s.recv(100)
        if newdata:
            rcv_data = rcv_data + newdata.decode("utf-8")
        else:
            break

    s.close()
    return rcv_data