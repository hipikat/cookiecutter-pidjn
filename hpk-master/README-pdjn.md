# Ada's little website

Author: Ada Wright <ada@hpk.io>

This project is based on a Pidjn template, generated with:

Python 3.8.5,
Click 7.1.2,
Django 3.1.3,
Django-CMS 3.8.0,
Node 14.15.1,
Webpack 5.10.1,
Foundation for Sites 6.6.3,
Docker Compose 1.27.4,
ubuntu:focal

---

## Installation

You should have [Docker](https://www.docker.com) and 
[PostgreSQL](https://www.postgresql.org) installed.
Then get the correct versions of Python and Node installed -
I recommend using [Pyenv](https://github.com/pyenv/pyenv) and
[Nodenv](https://github.com/nodenv/nodenv) to manage multiple installs
of each. I'd also suggest
using [Pipenv](https://docs.pipenv.org) to manage your Python virtual
environments.

```
§ nodenv install $(cat .node-version)
§ pyenv install $(cat Pipfile | grep version | cut -d'"' -f 2)
```

Clone the source into a project folder, and `npm run init`. This makes a
virtualenv (with Pyenv), and installs all the Python and Node dependencies
(from [Pipfile](Pipfile) and [package.json](package.json)).

```
hpk-master § npm run init
[...]
Installing dependencies from Pipfile.lock (b48720)...
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 61/61 — 00:00:47
To activate this project's virtualenv, run pipenv shell.
[...]
65 packages are looking for funding
  run `npm fund` for details

found 1 low severity vulnerability
  run `npm audit fix` to fix them, or `npm audit` for details
hpk-master §
```

Inside your virtualenv, `pdjn` is the command-line tool you use
to do things like ...

- start development servers
- build assets, or start a global build-watch process
- run linters, or start a global lint-watch process
- build docker images and compose containers

... with short commands that default to production settings
(whenever that's applicable).
