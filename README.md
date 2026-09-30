# pdf-multitools
A collection of tools to enhance your PDF collection

## Reqired Software

TLDR this is only tested to work on WSL (debian, but that shoudn't matter). You will need to install `qpdf` with the following (or similar) command:
``` shell
sudo apt install qpdf
```

## How to Use
- Probably easiest to drag and drop PDF's into this folder or drag and drop a copy of the python script into the PDF folder
- execute from the linux terminal (or whichever has `qpdf`)
- **This process takes like 4 minutes** -- qpdf is single threaded (to the best of my knowledge). Good news: you can run as many of these as you have threads and it will still only take 4 minutes!
- Here's an example of how to use it from the command line:
``` shell
$ ./remove_watermark.py <input-file-name>.pdf <output-file-name>.pdf
```

## How it Works
TODO

## Upcoming Improvements
Also TODO