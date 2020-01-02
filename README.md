# Lets treat secrets like we should and don't be to nerdy

## Why ?
People are often afraid of GPG and asymetric cryptograpy.
If you want to share secret with your teammates, but your company has no procedures? Here we are!
LIME-COMB is set of tools and services designed to make sharing secrets easy for everone.
We want to offer easy, still safe solution for everyone( including non technical staff)

## How ?

Lime-comb is basicly public key registy and set of the tools. Public keys are stored in the database. End user can easily import existing public key and encrypt message. No gpg nor cryptography knowledge required.

### public key registry

We believe we shouldn't reinvent wheel. Public key registry is secured with authorization from google(firebase auth).
User is able to modify just his own key and read keys from all not premium users. We believe smart people provides good solutions and we should utilize them.

### cmd line tools

What was the syntax for gpg? Sould I use `base64` or armour mode? It's not you problem anymore, we will do it for you.
The only thing you need to know is receiver email and message itself.

### GUI - TODO
