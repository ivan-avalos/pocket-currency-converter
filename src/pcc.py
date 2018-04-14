#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2018 Ivan Avalos <ivan.avalos.diaz@hotmail.com>
# 
# pocket-currency-converter is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# pocket-currency-converter is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from http import client
from urllib import parse
from htmldom import htmldom

# Stupid stuff
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	
	def print_msg (color, tag, msg):
		print ('[' + bcolors.BOLD + color + tag + bcolors.ENDC + '] ' + msg)

# Help
help = """Pocket Currency Converter 0.1 (alpha)

Usage: pcc.py --help
Or   : pcc.py -h
Or   : pcc.py <amount> <from> to <to>

Example:
\tpcc.py 500 USD to MXN
"""

if sys.argv[1] == '--help' or sys.argv[1] == '-h':
	print(help)
	sys.exit ()

# HTTP connection
url = 'www.xe.com'
crawler = client.HTTPSConnection (url)

# HTTP request
args = {
	'Amount': sys.argv[1],
	'From': sys.argv[2].upper(),
	'To': sys.argv[4].upper()
}
request_url = '/currencyconverter/convert/?' + parse.urlencode (args)
bcolors.print_msg (bcolors.OKGREEN, 'request', 'https://' + url + request_url)

crawler.request ('GET', request_url)
response = crawler.getresponse()
bcolors.print_msg (bcolors.OKGREEN, 'status', str(response.status) + ' ' + str(response.reason))
response_data = str(response.read()).replace("\'", '"').replace('\\', '')

# HTML DOM
dom = htmldom.HtmlDom().createDom(response_data)

def currency_from_el_text (text):
	output = []
	for i in list(text):
		if i.isupper(): output.append (i)
	return ''.join(output)

# Left currency (from)
left_amount = dom.find ('span.amount')[0].attr('data-amount')
left_currency = currency_from_el_text (dom.find ('span.uccFromResultAmount')[0].text ())

# Right currency (to)
right_amount = dom.find ('span.uccResultAmount')[0].text ()
right_currency = currency_from_el_text (dom.find ('span.uccToCurrencyCode')[0].text ())

# Check if currencies exist
exist = True

if (left_currency != args['From']):
	bcolors.print_msg (bcolors.FAIL, 'error', args['From'] + ' currency does not exist.')
	exist = False
if (right_currency != args['To']):
	bcolors.print_msg (bcolors.FAIL, 'error', args['To'] + ' currency does not exist.')
	exist = False

# If exist, show them to the user
if exist:
	bcolors.print_msg (bcolors.OKGREEN, 'result', left_amount + ' ' + left_currency + ' => ' +
		right_amount + ' ' + right_currency)
