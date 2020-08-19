[![CodeFactor](https://www.codefactor.io/repository/github/lanlords/cli/badge)](https://www.codefactor.io/repository/github/lanlords/cli)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

# Lanlords CLI

CLI to easily and quickly manage the Lanlords infrastructure from your trusted
terminal. Beware that this CLI is extremely specific to Lanlords and communicates
with internal systems which may not public.

## Development

When developing locally it's recommended to use a virtual environment. You can
create one like this:
```
python3 -m venv .venv
```
And then activate the virtual environment:
```
source .venv/bin/activate
```

### Mock API Server

The [tests/mock](tests/mock) directory contains configuration to easily run an
API server that mocks the Lanlords admin API. The software to run this mock api
is the tool [mock-server](http://tomashanacek.github.io/mock-server/).

You can run the mock api yourself by installing and running the tool locally:
```
pip install mock-server
mock-server --dir=tests/mock/api
```
The easiest way is to use the Docker Compose method.

## License

[MIT license](LICENSE)
