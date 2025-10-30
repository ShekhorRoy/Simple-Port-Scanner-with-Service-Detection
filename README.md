# Python Port Scanner v1.0

A simple concurrent TCP port scanner with basic banner-grabbing.
Useful for learning sockets, threading, and simple service detection.

> **Important:** Only scan hosts and networks you own or have explicit permission to test. Unauthorized scanning may be illegal.

---

## Features
- Concurrent TCP port scanning using threads
- Basic banner grabbing for simple service identification
- Colored terminal output via `colorama`
- Simple command-line usage

---

## Requirements
- Python 3.6+
- `colorama`

Install dependency:
```bash
pip install colorama
```

or, if you include `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## Usage
```bash
python port_scanner.py <target> <start_port> <end_port>
```

**Examples**
```bash
python port_scanner.py 127.0.0.1 1 1024
python port_scanner.py scanme.nmap.org 80 443
```

**Notes**
- Port range must be between `0` and `65535`, and `start_port <= end_port`.
- The script resolves hostnames to IP before scanning.
- Banner grabbing attempts a simple HTTP `HEAD` probe; some services may not respond or may log the probe.
- If scanning large ranges, consider reducing concurrency or increasing timeouts to avoid false negatives.

---

## Safety & Legal
- Always obtain explicit permission before scanning third-party targets.
- Use this tool only on systems you own, in lab environments, or with written authorization.
- The author is not responsible for misuse.

---

## Project Structure
```
/python-port-scanner
├── port_scanner.py        # Main scanner script
├── README.md              # This file
└── requirements.txt       # Dependencies
```

---

## Suggested Improvements
- Use `argparse` for better CLI options (timeout, threads, output file).
- Use `concurrent.futures.ThreadPoolExecutor` or `BoundedSemaphore` to limit concurrency.
- Add an option to save results (CSV/JSON).
- Add protocol-specific probes (e.g., HTTP only for common web ports).
- Add a graceful shutdown on `KeyboardInterrupt`.

---

## License
Add an open-source license (e.g., MIT) in a `LICENSE` file if you plan to publish.
