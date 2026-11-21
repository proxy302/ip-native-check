# ip-native-check: is an IP native or broadcast?

An IP is **native** when three countries agree: the country its address block is registered in (the regional internet registry record), the country IP databases geolocate it to, and the country of the network (ASN) that announces it. It is **broadcast** when the block is registered in one country but announced by a network registered in another; such an IP can still geolocate correctly and still be classified as ISP. `native_check.py` looks up all three for any IP, or for the exit IP of a proxy, with no API key and no third-party packages. Proxy302 maintains this tool and sells static ISP IPs; the check works the same on anyone's addresses.

> Maintained by [Proxy302](https://proxy302.com). MIT licensed.

## Usage

```bash
python3 native_check.py 8.8.8.8 1.1.1.1
python3 native_check.py --proxy "http://USER:PASS@HOST:PORT"
```

USER, PASS, HOST and PORT are placeholders. Percent-encode `@ # : /` in the password. Needs Python 3.8+ and the `whois` command (present on macOS and most Linux distributions).

## Example

```text
IP               8.8.8.8  (8.8.8.0/24)
Registered in    US  (arin)
Geolocated to    US  Mountain View
Announced by     AS15169 GOOGLE - Google LLC, US  (ASN registered in US)
Verdict          native

IP               1.1.1.1  (1.1.1.0/24)
Registered in    AU  (apnic)
Geolocated to    AU  Brisbane
Announced by     AS13335 CLOUDFLARENET - Cloudflare, Inc., US  (ASN registered in US)
Verdict          broadcast
```

1.1.1.1 is a good illustration: the block is an APNIC (Australian) registration, it geolocates to Brisbane, and it is announced by a US-registered network, so tools that show a native/broadcast label call it broadcast.

## Where the three countries come from

| Country | Source used here |
|---|---|
| Registration | Team Cymru's IP-to-ASN whois (`whois -h whois.cymru.com " -v <ip>"`), which reports the RIR country of the routed prefix |
| Geolocation | `https://ipinfo.io/<ip>/json`, field `country` (free tier, rate-limited) |
| ASN registration | Team Cymru again, queried by AS number |

A third verdict, **mixed**, means registration and ASN agree but geolocation differs. Geolocation databases update on their own schedules, so recheck after a few days before drawing conclusions.

## What native / broadcast does and does not tell you

- It is about where a block is registered and announced. It says nothing on its own about whether the network is a broadband ISP or a data center; for that, look at the IP type in IP databases (IPinfo's ASN type, IP2Location's usage type). When both databases say ISP, the IP is often called "dual ISP".
- Whether broadcast matters depends on who looks. Some IP checkers display the label; most websites use the geolocation country and the network type.
- No label makes an IP safe for every platform. Platforms apply their own rules and checks.

## Related

- [What is a dual ISP IP, and how do I check one myself?](https://github.com/proxy302/proxy-guides/blob/main/what-is-dual-isp-ip/README.md)
- [Native IP vs broadcast IP](https://github.com/proxy302/proxy-guides/blob/main/native-vs-broadcast-ip/README.md)
- [proxy-ip-check](https://github.com/proxy302/proxy-ip-check): exit IP, country, network owner and timezone in one command

*Checked 21 November 2026.*
