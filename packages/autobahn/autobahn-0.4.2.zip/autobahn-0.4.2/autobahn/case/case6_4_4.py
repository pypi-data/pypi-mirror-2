# coding=utf-8

###############################################################################
##
##  Copyright 2011 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

from case import Case
from case6_3_1 import Case6_3_1
import binascii
from autobahn.websocket import WebSocketProtocol


class Case6_4_4(Case6_3_1):

   DESCRIPTION = """Send invalid UTF-8 text message in 2 fragments. First is valid, then wait, then in 2nd frame, send the octet making the sequence invalid, then wait, then send test rest of 2nd frame.<br><br>MESSAGE:<br>%s<br>%s""" % (Case6_3_1.PAYLOAD, binascii.b2a_hex(Case6_3_1.PAYLOAD))

   EXPECTATION = """The first frame is accepted, we expect to timeout on the first wait. The 2nd frame should be rejected immediately (fail fast on UTF-8) upon receiving the offending octet. If we timeout, we expect the connection is failed at least then, since the payload is not valid UTF-8."""

   def onOpen(self):

      self.expected[Case.OK] = [("timeout", "A"), ("failedByMe", False)]
      self.expected[Case.NON_STRICT] = [("timeout", "A"), ("timeout", "B"), ("failedByMe", False)]

      self.p.beginMessage(opcode = WebSocketProtocol.MESSAGE_TYPE_TEXT)
      self.p.beginMessageFrame(len(self.PAYLOAD))
      self.p.sendMessageFrameData(self.PAYLOAD[:12])
      self.p.continueLater(1, self.part2)

   def part2(self):
      self.received.append(("timeout", "A"))
      self.p.sendMessageFrameData(self.PAYLOAD[12])
      self.p.continueLater(1, self.part3)

   def part3(self):
      self.received.append(("timeout", "B"))
      self.p.sendMessageFrameData(self.PAYLOAD[13:])
      self.p.endMessage()

      self.p.killAfter(1)
