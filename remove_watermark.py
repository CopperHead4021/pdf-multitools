#!/usr/bin/env python3

import sys
import subprocess
import tempfile
from pathlib import Path
import re

WATERMARK_PATTERN = "q[\\s\\S]{1,80}?(?:<|\\[)[<>0-9a-f]+(?:>|\\])T(?:j|J)\\s[\\s\\S]{1,20}Q"

ENCODING_PATTERN = ("(?<=\\d\\d\\d\\s\\d\\sobj\\s)<<\\s{1,3}\\/BaseEncoding\\s\\/\\w{15}\\s{3}\\/\\w{11}\\s\\[\\s"
                    "(\\s+?\\d\\s(?:\\s{4}\\/\\w\\s){1,20}(?:\\s*\\/space\\s)(?:\\s{4}\\/\\w\\s){1,20}\\s*\\/parenleft"
                    "\\s(?:\\s{4}\\/\\w+\\s){1,20}?\\s*\\/parenright[\\s\\S]*?)\\s\\s\\][\\s\\S]*?>>\\s(?=endobj\\s)")

# OLD_ENCODING_PATTERN  = ("(?<=\\d\\d\\d\\s\\d\\sobj\\s)<<\\s{1,3}\\/BaseEncoding\\s\\/\\w{15}\\s{3}\\/\\w{11}\\s\\[\\s+?\\d\\s"
#                      "(?:\\s{4}\\/\\w\\s){1,20}(?:\\s*\\/space\\s)(?:\\s{4}\\/\\w\\s){1,20}\\s*\\/parenleft\\s(?:\\s{4}"
#                      "\\/\\w+\\s){1,20}?\\s*\\/parenright[\\s\\S]*?>>\\s(?=endobj\\s)")

w = re.compile(WATERMARK_PATTERN)
e = re.compile(ENCODING_PATTERN)

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} input.pdf output.pdf")
    sys.exit(1)

input_pdf = Path(sys.argv[1])
output_pdf = Path(sys.argv[2])

if not input_pdf.exists():
    print(f"Error: {input_pdf} not found")
    sys.exit(1)

# with tempfile.TemporaryDirectory() as tmp:
qdf = Path("input.qdf.pdf")

# Convert PDF to QDF
subprocess.run([
    "qpdf",
    "--qdf",
    "--object-streams=disable",
    str(input_pdf),
    str(qdf)
], check=True)

# Safety Checks
numPages = int(subprocess.check_output(
    ["qpdf", "--show-npages", str(qdf)],
    text=True
))
text = qdf.read_bytes().decode("latin-1")
numMatches = len(re.findall(WATERMARK_PATTERN, text))
numEncodings = len(re.findall(ENCODING_PATTERN, text))

print(numMatches)
print(numEncodings)

ret = None

# Edit QDF
if numMatches == numPages:
    ret = w.subn("", text)
    print(f"Removed {ret[1]} watermark occurrence(s).")
else:
    print("Watermark sequence not found.")
    sys.exit(1)

if not (ret is None) and numEncodings == 1:
    ret = e.subn("", ret[0])
    print(f"Removed watermark encodings.")
else:
    print("Watermark encoding sequence not found...")
    print("Personal information may still be hidden in file!")

qdf.write_bytes(ret[0].encode("latin-1"))

# Rebuild normal PDF
subprocess.run([
    "qpdf",

    # "--no-warn",
    str(qdf),
    str(output_pdf)
])

print(f"Created: {output_pdf}")