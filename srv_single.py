#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_single.py
# Single-threaded server that serves one client at a time; others must wait.

import zen_utils
import argparse
import ssl

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('cafile', help='Path to a CA certificate file')
    parser.add_argument('certificate', help='Path to crt file')
    parser.add_argument('keyfile', help='Path to a certificate key/pem file')
    parser.add_argument('-e', action='store_true', help='cause an error')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)

    listener = zen_utils.create_srv_socket(address)
    purpose = ssl.Purpose.CLIENT_AUTH
    context = ssl.create_default_context(purpose, cafile=args.cafile)
    context.load_cert_chain(args.certificate, args.keyfile)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False
    zen_utils.accept_connections_forever(listener, context)
