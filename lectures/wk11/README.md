# Week 11
## Two-Factor Authentication

Two new packages this week: `pip install pyotp qrcode[pil]`

**Note**: If you're using an alternate shell like `zsh`, square brackets may be reserved.
In that case, install `'qrcode[pil]'`, just with the quotes.

Forunately and unforunately for us, all UMD students use Duo for two-factor authentication
when logging in to their UMD accounts now. 

The CS submit and grades servers were immune to this change until recently...

So today, we're going to learn how to implement Two-Factor auth for our Flask apps!