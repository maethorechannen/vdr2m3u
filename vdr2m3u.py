import csv
import re

ip_address = '192.168.1.107'
fe = '1'
sys = 'dvbs'

def extract_param_int(c, params):
    re1='.*?'	# Non-greedy match on filler
    re2='(' + c +')'	# Any Single Word Character (Not Whitespace) 1
    re3='(\\d+)'	# Integer Number 1
    rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
    m = rg.search(params)
    if m:
        w1=m.group(1)
        int1=m.group(2)
        return int1
    return

def extract_fec(params):
    return extract_param_int('C', params)

def extract_roll_off(params):
    v = extract_param_int('O', params)
    if v == None:
        return
    return "0." + v

def extract_mtype(params):
    v = extract_param_int('M', params)
    return {
        '2': 'qpsk',
        '5': '8psk'
    }.get(v, None)

def extract_pol(params):
    ps = params.lower()
    if 'h' in ps:
        return 'h'
    if 'v' in ps:
        return 'v'
    if 'l' in ps:
        return 'l'
    if 'r' in ps:
        return 'r'

def extract_msys(params):
    v = extract_param_int('S', params)
    if '1' in v:
        return sys + '2'
    return sys

def extract_pids(row):
    pids = "0,17,18"
    vid  = row[5].split("=")[0]
    if vid != '0' and vid != '1':
        pids = pids + "," + vid.replace("+", ",")
    apids = row[6].split(';')
    for apid in apids:
        aapid = apid.split("=")[0]
        pids = pids + "," + aapid
    pmt = row[13]
    pids = pids + "," + pmt
    return pids


with open('channels.conf', 'rb') as f:
    reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
    for row in reader:
        service, network  = row[0].split(';')
        freq = row[1]
        params = row[2]
        fec = extract_fec(params)
        ro = extract_roll_off(params)
        mtype = extract_mtype(params)
        pol = extract_pol(params)
        msys = extract_msys(params)
        mtype = extract_mtype(params)
        sr = row[4]
        pids = extract_pids(row)
        url = "rtsp://" + ip_address + "/?fe=" + fe + "&freq=" + freq + "&pol=" + pol + "&ro=" + ro + '&msys=' + msys + '&mytpe=' + mtype + '&sr=' + sr + '&fec=' + fec
        print "#EXTINF:0,116. " + service
        print url + '&pids=' + pids
