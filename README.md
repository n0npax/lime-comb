# WORK in PROGRESS - Code here won't work so far

[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://lime-comb.web.app/)
[![codecov](https://codecov.io/gh/n0npax/lime-comb/branch/master/graph/badge.svg)](https://codecov.io/gh/n0npax/lime-comb)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


# Lets treat secrets like we should and don't be to nerdy

## Why ?
People are often afraid of `GPG` and asymetric cryptograpy.
If you want to share secret with your teammates, but your company has no procedures? Here we are!
LIME-COMB is set of tools and services designed to make sharing secrets easy for everone.
We want to offer easy, still safe solution for everyone( including non technical staff)

## How ?

Lime-comb is basicly public key registy and set of the tools. Public keys are stored in the database. End user can easily import existing public key and encrypt message. No gpg nor cryptography knowledge required.

### Public key registry (WEB)

We believe we shouldn't reinvent wheel. Public key registry is secured with authorization from google(`firebase auth`).
User is able to modify just his own key and read keys from all not premium users. We believe smart people provides good solutions and we should utilize them.

### CMD line tools

What was the syntax for gpg? Sould I use `base64` or armour mode? It's not you problem anymore, we will do it for you.
The only thing you need to know is receiver email and message itself.

### GUI - TODO

# Install

## key registry
it's [here](https://lime-comb.web.app/). Please register yourself directly or via cmdline tool.

## cmdline tools

### requirements
* python

# Design

![Design diagram](https://github.com/n0npax/lime-comb/blob/master/images/arch_diagram.svg)

## Flow

All clients are connecting to firestore database using oauth2. By default unauth user is allowed to read any key, and auth user is allowed to modify just his own key.

## infra

Deployment is done via cloud build jobs which are triggered by github.
