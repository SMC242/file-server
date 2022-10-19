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
