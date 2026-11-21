#!/usr/bin/env python3
"""Is an IP "native" or "broadcast"? Compares three countries:
registration (the prefix's RIR record), geolocation (ipinfo.io) and the
announcing network's (ASN) registration country.

usage: python3 native_check.py 8.8.8.8 [1.1.1.1 ...]
       python3 native_check.py --proxy http://USER:PASS@HOST:PORT   (checks the proxy's exit IP)
No third-party packages. Needs the `whois` command (macOS and most Linux have it).
"""
import json, subprocess, sys, urllib.request

def cymru(query):
    out = subprocess.run(['whois', '-h', 'whois.cymru.com', f' -v {query}'],
                         capture_output=True, text=True, timeout=30).stdout
    rows = [l for l in out.splitlines() if '|' in l and not l.startswith('AS ')]
    return [c.strip() for c in rows[-1].split('|')] if rows else None

def ipinfo(ip='', proxy=None):
    handlers = [urllib.request.ProxyHandler({'http': proxy, 'https': proxy})] if proxy else []
    opener = urllib.request.build_opener(*handlers)
    url = f'https://ipinfo.io/{ip + "/" if ip else ""}json'
    with opener.open(urllib.request.Request(url, headers={'Accept': 'application/json'}), timeout=20) as r:
        return json.load(r)

def check(ip='', proxy=None):
    geo = ipinfo(ip, proxy)
    ip = geo['ip']
    pfx = cymru(ip)            # AS | IP | BGP Prefix | CC | Registry | Allocated | AS Name
    if not pfx:
        print(f'{ip}: no routing data (private or unannounced address?)'); return
    asn = cymru(f'AS{pfx[0]}')  # AS | CC | Registry | Allocated | AS Name
    reg, geo_cc, as_cc = pfx[3], geo.get('country', '?'), asn[1] if asn else '?'
    verdict = 'native' if reg == geo_cc == as_cc else 'broadcast' if reg != as_cc else 'mixed'
    print(f'IP               {ip}  ({pfx[2]})')
    print(f'Registered in    {reg}  ({pfx[4]})')
    print(f'Geolocated to    {geo_cc}  {geo.get("city", "")}')
    print(f'Announced by     AS{pfx[0]} {pfx[6]}  (ASN registered in {as_cc})')
    print(f'Verdict          {verdict}')
    if verdict == 'mixed':
        print('                 registration and ASN agree, geolocation differs: the databases may lag, recheck in a few days')
    print()

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == '--proxy':
        check(proxy=args[1])
    else:
        for a in args:
            check(a)
