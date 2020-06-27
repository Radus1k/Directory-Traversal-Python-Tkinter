import sys

sys.path.append('D:\\Licenta Proiect Practic')
sys.path.append('D:\\Licenta Proiect Practic\\main')
sys.path.append('D:\\Licenta Proiect Practic\\Py_Environment\\Lib\\site-packages')
sys.path.append('D:\\Licenta Proiect Practic\\Images')
sys.path.append('D:\\Licenta Proiect Practic\\Proxy-list')

from argparse import ArgumentParser
import argparse
import socket
from main.gui import run



def menu():# using GUI Tkinter now, but keep it just in case
    parser = ArgumentParser(description="Choose option for fuzzing test", formatter_class=argparse.RawTextHelpFormatter,
                            epilog="For more details use the README file", add_help=True)

    parser.add_argument('-m', "--module", type=str, default='http', choices=['http', 'https', 'localhost']
                        , help="Specify the module. Available options:"
                               "Http / Https / FTP / payload / tftp/ localhost",
                        metavar='', required=False)

    parser.add_argument('-p', "--port", type=str, default=80, help="Specify the target port",
                        metavar='', required=False)

    parser.add_argument('-u', "--url", type=str, default=None, help="Specify the site name",
                        metavar='', required=False)

    parser.add_argument('-i', "--ip", type=str, default=None, help="Specify the target IP or type 'lh' for 127.0.0.1",
                        metavar='', required=False)

    parser.add_argument('-g', "--method", choices=['GET', 'POST'],
                        help="Specify request type ('GET' or 'POST')",
                        default='GET', metavar='', required=False)

    parser.add_argument('-f', "--file", type=str, default=None, help="Specify file containing urls",
                        metavar='', required=False)

    parser.add_argument('-c', '--cookie', type=str,
                        default=None, help="Add Cookie within the request"
                                           "Example of correct input: key1:value1 key2:value2")

    parser.add_argument('-o', "--output", type=str, default=None, help="Output the fuzz process test in console")

    parser.add_argument('-ua', '--useragent',
                        default=None, help='Adding fake user agents')

    parser.add_argument('-q', '--randproxy',
                        default=False, type=bool, choices=[True, False], help='Add random proxy (ip/port/code')

    parser.add_argument('-pp', '--proxy',
                        default=None, type=str, help='Add specific proxy (ip/port/code')

    ''' If no arguments, print help again  '''
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        "here"
        parser.print_usage()
        parser.exit()
    args = parser.parse_args()
    return args


def get_url():
    args = menu()
    return args.url


def _setRealAddress(self, address):
    if len(address) == 4:
        # Izv6, make sure we have the scopeID associated
        hostname = socket.getnameinfo(
            address, socket.NI_NUMERICHOST | socket.NI_NUMERICSERV)[0]
        self.realAddress = tuple([hostname] + list(address[1:]))
    else:
        self.realAddress = address
    self.doConnect()


def main():
	run()
    #gui.run()
    #examples.write_to_pdf()
    #print(crawl_links.getAllUrl("https://www.emag.ro/"))
    #print(socket.gethostbyname("www.google.ro"))
    #addr = (216, 217, 18, 163)
    #print(_setRealAddress(addr, obj))


if __name__ == "main":
    main()

