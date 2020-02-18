[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://lime-comb.web.app/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/n0npax/lime-comb/branch/master/graph/badge.svg)](https://codecov.io/gh/n0npax/lime-comb)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f46eccc192ce4347b7a6596175c960ee)](https://www.codacy.com/manual/n0npax/lime-comb?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=n0npax/lime-comb&amp;utm_campaign=Badge_Grade)

# Lets treat secrets like we should and don't be to nerdy

## Why?
People are often afraid of `gpg` and asymmetric cryptography. `gpg` key-server doesn't validate a key ownership.
- If you want to share secret with your teammates, but your company has no procedures
- If storing secret in external system like `1password` is not an option
- If you want to share secrets in secure way and use managed key registry
Here we are!

`LIME-COMB` is set of tools and services designed to make sharing secrets easy.
Given solution aims to be an easy, still safe solution for everyone( including non technical staff)

## How?

Lime-comb is basically public key registry and set of the tools. Public keys are stored in the database. End user can easily import existing public key and encrypt message. No `gpg` nor cryptography knowledge required.

### Public key registry (WEB)

We believe we shouldn't reinvent wheel. Lime-comb key registry is secured with authorization from google(`firebase auth`).
We believe smart people provides good solutions and we should utilize them.

### Command line tools

What was the syntax for `gpg`? Should I use `base64` or `armour mode`? It's not your problem anymore, we will do it for you.
The only thing you need to know is receiver email and message itself.

#### Smart defaults

We are offering flexible solution with 2 main default profiles
- locked (keeps private key just locally)
- glass-break (store prov key in `db` with access just for given user)

Many other configuration option can be adjusted by an user

### GUI - TODO

## Install

### Key registry
it's [here](https://lime-comb.web.app/). Please register yourself directly or via cmdline tool.

### Command line tools

#### Requirements
- python
- installed gpg

## Design

![Design diagram](https://github.com/n0npax/lime-comb/blob/master/images/arch_diagram.svg)

### Flow

All clients are connecting to `firestore` database using `oauth2`. By default unauthorized user is allowed to read any key, and authenticated user is allowed to modify just his own key.

### infra

Deployment is done via cloud build jobs which are triggered by GitHub repository event.