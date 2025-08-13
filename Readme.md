**Overview**



This project demonstrates mutual TLS (mTLS) using Python. It includes:



Server: Server.py



Client: Client.py



Certificate Authority (CA): Used to sign server and client certificates



OpenSSL configurations: To generate keys, CSRs, and certificates



With mTLS, both client and server authenticate each other using certificates during TLS handshake.



**Folder Structure**



mtls/

├── CA/

│   ├── ca.crt

│   ├── ca.key

│   └── openssl.cnf

├── Server/

│   ├── server.key

│   ├── server.crt

│   ├── server.csr

│   └── Server.py

├── Client/

│   ├── client.key

│   ├── client.crt

│   ├── client.csr

│   └── Client.py



**In Server and Client also we had openssl.cnf**



**1. CA Configuration (openssl.cnf)**

**==========================================================================**

**\[ req ]**

**default\_bits       = 2048**

**distinguished\_name = req\_distinguished\_name**

**x509\_extensions    = v3\_ca**

**prompt             = yes**



**\[ req\_distinguished\_name ]**

**CN = MyCA**



**\[ v3\_ca ]**

**subjectKeyIdentifier = hash**

**authorityKeyIdentifier = keyid:always,issuer**

**basicConstraints = critical, CA:true**

**keyUsage = critical, digitalSignature, cRLSign, keyCertSign**



**=============================================================================**

**basicConstraints = CA:true → Marks the certificate as a CA certificate.**



**keyUsage → Allowed operations for this certificate (signing other certs, CRL signing).**





**2.Server Certificate Configuration**



**================================================================================**

**\[ req ]**

**default\_bits       = 2048**

**prompt             = no**

**default\_md         = sha256**

**distinguished\_name = dn**

**req\_extensions     = req\_ext**



**\[ dn ]**

**CN = localhost**



**\[ req\_ext ]**

**subjectAltName = @alt\_names**



**\[ alt\_names ]**

**DNS.1 = localhost**



**=================================================================================**



**CN = localhost → Matches the server hostname (required for TLS).**



**subjectAltName → Used by clients to verify the server hostname.**



**EKU not explicitly set → Python ssl and requests accept it as a valid server certificate.**



**3.client certificate configuration**



**================================================================================**



**\[ req ]**

**default\_bits       = 2048**

**prompt             = no**

**default\_md         = sha256**

**distinguished\_name = dn**

**req\_extensions     = req\_ext**



**\[ dn ]**

**CN = FakeClient**



**\[ req\_ext ]**

**basicConstraints = CA:FALSE**

**keyUsage = digitalSignature, keyEncipherment**

**extendedKeyUsage = clientAuth**

**=================================================================================**



**extendedKeyUsage = clientAuth → Required for client certificates in mTLS. Without it, some libraries may reject the certificate.**





**Here we had Certificate Generation process ,key generation,and csr with help of openssl command and openssl.cnf**









**Why it Works**

**Certificate Type	EKU Required?	                 Reason it may work without EKU**

**Server	                 Optional	                 Python ssl mainly checks hostname (CN/SAN) and trust chain**

**Client	                 Required	                 Some libraries reject client certs without clientAuth EKU**



**Key Points:**



**keyUsage ensures correct cryptographic operations (digital signature, encryption).**



**extendedKeyUsage ensures certificate is used as intended (clientAuth, serverAuth).**



**Hostname (CN/SAN) must match for TLS handshake**





**Server.py**

**=================================================================**

**from http.server import HTTPServer, SimpleHTTPRequestHandler**

**import ssl**



**server\_address = ('localhost', 4443)**

**httpd = HTTPServer(server\_address, SimpleHTTPRequestHandler)**



**context = ssl.create\_default\_context(ssl.Purpose.CLIENT\_AUTH)**

**context.load\_cert\_chain(certfile='server.crt', keyfile='server.key')**

**context.load\_verify\_locations('../CA2/ca2.crt') // for different CA**

**context.load\_verify\_locations('../CA/myCA.crt')// for same CA**

**context.verify\_mode = ssl.CERT\_REQUIRED**



**httpd.socket = context.wrap\_socket(httpd.socket, server\_side=True)**

**print("Server running on https://localhost:4443")**

**httpd.serve\_forever()**

**==========================================================================**



**Client.py**

**=====================================================================================**

**import requests**



**url = 'https://localhost:4443'**

**resp = requests.get(url, cert=('client.crt', 'client.key'), verify='../CA/myCA.crt') //same CA**

**resp = requests.get(url, cert=('client2.crt', 'client2.key'), verify='../CA/myCA.crt') // Different CA**

**print(resp.text)**

**=======================================================================================**



**Diagram: How mTLS Works**



**===================================================**

 **Client                                Server**

   **|                                     |**

   **|---Hello, I am Client---------------->|**

   **|                                     |**

   **|<--Hello, I am Server----------------|**

   **|                                     |**

   **|---Send Client Certificate------------>|**

   **|                                     |**

   **|<--Server verifies client cert--------|**

   **|                                     |**

 **TLS Handshake completes → Secure channel**

**=========================================================**

**Notes:**



**Both server and client verify each other using CA-signed certificates.**



**If EKU or CN/SAN mismatches, handshake fails.**









