#!/usr/bin/env python3

# taken from:
# https://forum.proxmox.com/threads/how-to-get-the-exactly-backup-size-in-proxmox-backup.93901/
# by "masgo" 2023-03-27
#
# this is the original... everything below here is the original:

import os
import sys

datastore = "/mnt/datastore/localHDD/vm/"

vmid = ""
if len(sys.argv) > 1:
    vmid = sys.argv[1]

vm = os.path.join(datastore, vmid)

# Get all .img.fidx file paths for the chosen VM
filearray = []
for root, dirs, files in os.walk(vm, topdown=False):
    for name in files:
        if name.endswith(".img.fidx"):
            filearray.append(os.path.join(root, name))

# sort to obtain filepath sort
# if arg empty then do date sort
if vmid:
    filearray.sort()
else:
    filearray = sorted(filearray, key=lambda x: os.path.relpath(x, vm).split('/',1)[1])

if len(filearray) > 0:
    print("-" * 95)
    print(f"{'| {filename'.ljust(52)} | {'chunks'.ljust(19)} | {'size'.ljust(16)} |")
    print("-" * 95)
    chunkarray = set()
    for filepath in filearray:
        with open(filepath, "rb") as f:
            f.seek(4096)
            data = f.read()
            hex_data = data.hex()
            file_chunks = []
            new_unique_chunks = set()
            for i in range(0, len(hex_data), 64):
                file_chunk = hex_data[i:i+64]
                if file_chunk not in chunkarray :
                    new_unique_chunks.add(file_chunk)
                chunkarray.add(file_chunk)
            if new_unique_chunks:
                new_chunks = len(new_unique_chunks)
                filename = os.path.relpath(filepath, vm)  # Remove the datastore prefix from the file path
                print(f"| {filename.ljust(50)} | {new_chunks:>12} chunks | {new_chunks * 4:>12} MiB |")
    print("-" * 95)

