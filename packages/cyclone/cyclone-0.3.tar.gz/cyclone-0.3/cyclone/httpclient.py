#!/usr/bin/env python
# coding: utf-8
#
# Copyright 2010 Alexandre Fiori
# based on the original Tornado by Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from cyclone.web import _O
from twisted.web import client

class Page(_O):
    pass

class HTTPClientFactory(client.HTTPClientFactory):
    def page(self, page):
        if self.waiting:
            self.waiting = 0
            self.deferred.callback(Page(
                body=page,
                headers=self.response_headers,
                cookies=self.cookies,
            ))

def fetch(url, contextFactory=None, *args, **kwargs):
    def wrapper(error):
        return Page(error=error.getErrorMessage())

    d = client._makeGetterFactory(url, HTTPClientFactory,
        contextFactory=contextFactory, *args, **kwargs).deferred
    d.addErrback(wrapper)
    return d
