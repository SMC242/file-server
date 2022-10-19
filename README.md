# file-server

This is a unviersity project for NOSE. We have to make a file serving service

# Requirements

## General

- Server should take in port
- Client should take in server IP and port
- After executing a function, print a report to the terminal on both ends
  - IP and port of client
  - Request type, file name, and sucess/failure
  - Failures should have a one-line error message

## Funtions

Here are the valid requests a client can make from its CLI

- Download files from the server ("get")
  - Don't overwrite files
  - Download in exclusive binary mode ("xb" mode in Python)
    - Prevents overwriting files
- List the available files ("list")
- Upload files to the server ("put")
  - Needs a file path
  - Open in binary mode
- These are called from the client CLI

# Message formats

These are the valid messages used in our protocol.

- Packet size: 1KiB[^1]

## Initial request

`type={0,1,2} name={<str>} n={<int>}`

### Definitions

<dl>
  <dt>type</dt>
  <dd>0 = get, 1 = put, 2 = list</dd>

  <dt>name</dt>
  <dd>The file name. Will be the empty string if type = 2</dd>

  <dt>n</dt>
  <dd>The number of packets required to upload the file. 0 unless type = 1</dd>
</dl>

## Request acknowledgement:

`status={0,1} msg={<str>} n={<int>}`

### Definitions

<dl>
  <dt>status</dt>
  <dd>0 = success, 1 = error</dd>

  <dt>msg</dt>
  <dd>The error message. Will be the empty string if type = 0</dd>

  <dt>n</dt>
  <dd>The number of packets that the file will be sent in. 0 unless type = 0</dd>
</dl>

## File packets

- The file encoded in binary format
- Likely split into packets. Use the `n` header to determine how many packets to listen for

## List response

`name1 name2 name3` etc

[^1]: Kibibytes (KiB) are 1024 bits
