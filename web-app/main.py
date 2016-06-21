#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import betting
from google.appengine.ext import ndb
from models import *

ipAddressKey = 'ipAddress'


class MainHandler(webapp2.RequestHandler):
    def handleRequest(self):
        if self.request.get("action") == "updateData":
            key = self.request.get("key")
            data = MiscData.query(MiscData.key == key).fetch(1)
            if len(data) == 0:
                data = MiscData(key=key, value=self.request.get("value"))
                data.put()
            else:
                data = data[0]
                data.value = self.request.get("value")
                data.put()
        elif self.request.get("action") == "cleanup":
            ndb.delete_multi(
                MiscData.query().fetch(keys_only=True)
            )
            self.response.write('Data cleaned successfully!')
            self.response.headers["Content-Type"] = "text/plain"
        elif self.request.get("action") == "getData":
            key = self.request.get("key")
            data = MiscData.query(MiscData.key == key).fetch(1)
            if len(data) != 0:
                self.response.headers["Content-Type"] = "text/plain"
                self.response.write(data[0].value)
            else:
                self.error(404)
                self.write("<h1>The key was not found!</h1>")
        else:
            data = MiscData.query().fetch()
            self.response.write('<html><head><title>Horatiu Misc Stuff</title></head><body>')
            self.response.write('<h1>Welcome to horatiu misc stuff!</h1> <h2>Available data:</h2><ul>')
            for d in data:
                self.response.write('<li><b>' + d.key + '</b> - ' + str(d.date if d.date is not None else 'none') + '<br><pre>' + d.value + '</pre></li>')
            self.response.write('</body></html>')

    def get(self):
        self.handleRequest()

    def post(self):
        self.handleRequest()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/betting', betting.BettingHandler)
], debug=True)
