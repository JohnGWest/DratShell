# DratShell

### How do I get started?

First, download this project your preferred method.

This project uses the poetry python package manager. If you have poetry, just run `poetry init` in this project, then `poetry run [python interpreter] [python file]`.

example:
```
you@example.com:~/DratShell$ poetry init
you@example.com:~/DratShell$ poetry run python3 drat/dratd.py
```

### How does it work?

To get this shell to work, you will have to run the host first with `drat/dratd.py`.

Then you will need to connect with a client with `drat/drat.py`.

Then you will be connected with the DratShell. It will display whatever you send from the client onto the host. You can even run one line bash commands!

### What is it?

This project is a very simple remote shell. Emphasis on *very*.

This was something I worked on for a couple hours to practice using sockets. If you are looking at this expecting a tool to rival ssh, then you may want to look elsewhere.

While I was doing this project, I decided I might as well try out some other libraries that I've heard of. `Click` is a pretty fun python module that makes command line options easier to handle. The `cmd` module, on the other hand, did not have enough documentation. It was definitely weird to work with.
