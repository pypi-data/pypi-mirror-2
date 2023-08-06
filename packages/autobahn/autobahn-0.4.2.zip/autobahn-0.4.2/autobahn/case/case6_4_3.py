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
from zope.interface import implements
from twisted.internet import reactor, interfaces


class StarFrameProducer:

   implements(interfaces.IPushProducer)

   def __init__(self, proto):
      self.proto = proto
      self.paused = False
      self.stopped = False

   def pauseProducing(self):
      self.paused = True

   def resumeProducing(self):
      if self.stopped:
         return
      self.paused = False
      while not self.paused:
         self.proto.sendFrame(opcode = 0, fin = False, payload = "*"*16, payload_len = 2**16/16)

   def stopProducing(self):
      self.stopped = True


class Case6_4_3(Case6_3_1):

   DESCRIPTION = """Send invalid UTF-8 text message in 3 fragments plus more. First is valid, then wait, then 2nd which contains the octet making the sequence invalid, then wait, then 3rd with rest. Then we send 64k frames forever.<br><br>MESSAGE:<br>%s<br>%s""" % (Case6_3_1.PAYLOAD, binascii.b2a_hex(Case6_3_1.PAYLOAD))

   EXPECTATION = """The first frame is accepted, we expect to timeout on the first wait. The 2nd frame should be rejected immediately (fail fast on UTF-8). If we timeout, we expect the connection is failed at least then, since the payload is not valid UTF-8."""

   def onOpen(self):

      self.expected[Case.OK] = [("timeout", "A"), ("failedByMe", False)]
      self.expected[Case.NON_STRICT] = [("timeout", "A"), ("timeout", "B"), ("failedByMe", False)]

      self.producer = StarFrameProducer(self.p)

      self.p.sendFrame(opcode = 1, fin = False, payload = self.PAYLOAD[:12])
      self.p.continueLater(1, self.part2)

   def part2(self):
      self.received.append(("timeout", "A"))
      self.p.sendFrame(opcode = 0, fin = False, payload = self.PAYLOAD[12])
      self.p.continueLater(1, self.part3)

   def part3(self):
      self.received.append(("timeout", "B"))
      self.p.sendFrame(opcode = 0, fin = False, payload = self.PAYLOAD[13:])

      self.p.createWirelog = False
      self.p.registerProducer(self.producer, True)
      self.producer.resumeProducing()

   def onConnectionLost(self, failedByMe):
      self.producer.stopProducing()
      Case6_3_1.onConnectionLost(self, failedByMe)
