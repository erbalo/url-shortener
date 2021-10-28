#!/usr/bin/env python3
import os

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import core as cdk

from url_shortener.url_shortener_stack import UrlShortenerStack

ACCOUNT= "ACCOUNT"
REGION = "REGION"

app = core.App()
UrlShortenerStack(app, "url-shortener-stack", env=core.Environment(account=ACCOUNT, region=REGION))

app.synth()
