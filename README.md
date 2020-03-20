[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://lime-comb.web.app/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/n0npax/lime-comb/branch/master/graph/badge.svg)](https://codecov.io/gh/n0npax/lime-comb)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f46eccc192ce4347b7a6596175c960ee)](https://www.codacy.com/manual/n0npax/lime-comb?utm_source=github.com&utm_medium=referral&utm_content=n0npax/lime-comb&utm_campaign=Badge_Grade)
[![License](https://img.shields.io/:license-mit-blue.svg)](https://badges.mit-license.org)

# Lets treat secrets like we should and don't be to nerdy

## Why

People are often afraid of `gpg` and asymmetric cryptography.
`gpg` key-server doesn't validate a key ownership.

- If you want to share secret with your teammates,
  but your company has no procedures

- If you want to share secrets in secure way and use managed key registry.
  Here we are!

`LIME-COMB` is set of tools and services designed to make sharing secrets easy.
Given solution aims to be an easy,
still safe solution for everyone(including non technical staff)

## How

Lime-comb is basically public key registry and set of the gpg based tools.
Public keys are stored in the database.
End user can easily import existing public key and encrypt message.
No `gpg` nor cryptography knowledge required.

### Public key registry (api/core)

We believe we shouldn't reinvent wheel.
Lime-comb key registry is secured with authorization from google oauth.
We believe smart people provides good solutions and we should utilize them.

### Command line tools (cli)

What was the syntax for `gpg`? Should I use `base64` or `armor mode`?
Can I trust Bob uploaded this particular key?
It's not your problem anymore, we will do it for you.
The only thing you need to know is Bobs(receiver) email.

#### How easy is that?

Just type message and receiver and confirm you are not a machine. Easy like that.

![demo](https://github.com/n0npax/lime-comb/blob/master/images/lime-comb-animation.gif)

#### Smart defaults

We are offering flexible solution with 2 main default profiles.

- Locked (keeps private key just locally)
- Glass-break (store private key and password in registry. This data are accessible just for given user)

Many other configuration option can be adjusted by an user

## Install

Use `pip`. Simple like that!
```zsh
python3 -m pip install lime-comb
```

## Requirements

- `python3.7+`
- `gpg`

## Design

![Design diagram](https://github.com/n0npax/lime-comb/blob/master/images/arch_diagram.svg)

### Infra

Deployment is done via cloud build jobs which are triggered
by GitHub repository event. Infra is managed by pulumi scripts.

## Other

### Contribution

Just raise a pull request on GitHub.

### Feedback

leave a star or raise an issue on GutHub.
