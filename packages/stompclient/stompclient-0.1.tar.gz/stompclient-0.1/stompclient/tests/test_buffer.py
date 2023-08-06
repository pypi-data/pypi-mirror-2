"""
Test the FrameBuffer utility class.
"""
import unittest
import uuid

from stompclient.frame import Frame
from stompclient.util import FrameBuffer

__authors__ = ['"Hans Lellelid" <hans@xmpl.org>']
__copyright__ = "Copyright 2009 Hans Lellelid"
__license__ = """Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 
  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

class TestFrameBuffer(unittest.TestCase):
    """
    Test the L{coilmq.utils.buffer.FrameBuffer} class.
    """
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def createMessage(self, cmd, headers, body):
        """ Creates a package STOMP message. """
        frame = Frame()
        frame.command = cmd
        frame.headers = headers
        frame.body = body
        return frame.pack()
    
    def test_extract_frame(self):
        """ Test extracting a single frame. """
        sb = FrameBuffer()
        m1 = self.createMessage('connect', {'session': uuid.uuid4()}, 'This is the body')
        sb.append(m1)
        msg = sb.extract_frame()
        assert isinstance(msg, Frame)
        assert m1 == msg.pack()
    
    def test_extract_frame_binary(self):
        """ Test extracting a binary frame. """
        sb = FrameBuffer()
        binmsg = "\x00\x00HELLO\x00\x00DONKEY\x00\x00"
        m1 = self.createMessage('send', {'content-length': len(binmsg)}, binmsg)
        sb.append(m1)
        msg = sb.extract_frame()
        assert isinstance(msg, Frame)
        assert msg.pack() == m1
     
        m2 = self.createMessage('send', {'content-length': len(binmsg), 'x-other-header': 'value'}, binmsg)
        sb.append(m2)
        msg = sb.extract_frame()
        assert isinstance(msg, Frame)
        assert msg.pack() == m2
       
    def test_extract_frame_multi(self):
        """ Test the handling of multiple concatenated messages by the buffer. """
        
        m1 = 'CONNECT\nsession:207567f3-cce7-4a0a-930b-46fc394dd53d\n\n0123456789\x00\n'
        m2 = 'SUBSCRIBE\nack:auto\ndestination:/queue/test\n\n\x00SEND\ndestination:/queue/test\n\n\x00'
        
        sb = FrameBuffer()
        sb.append(m1)
        f1 = sb.extract_frame()
        assert f1.command == 'CONNECT'
        assert f1.body == '0123456789'
        
        assert sb.extract_frame() is None
        
        sb.append(m2)
        f2 = sb.extract_frame()
        f3 = sb.extract_frame()
        
        assert f2.command == 'SUBSCRIBE'
        assert f2.body == ''
        assert f3.command == 'SEND'
        assert f3.destination == '/queue/test'
        assert f3.body == ''
        
        assert sb.extract_frame() is None
        
        
    def test_extract_frame_fragmented(self):
        """ Test the handling of fragmented frame data. """
        
        m1_1  = 'CONNECT\nsession:207567f3-cce7-4a0a-930b-'
        m1_2 = '46fc394dd53d\n\n0123456789\x00\nSUBSCRIBE\nack:a'
        
        m1_3 = 'uto\ndestination:/queue/test\n\n\x00SE'
        m1_4 = 'ND\ndestination:/queue/test\n\n0123456789\x00'
        
        sb = FrameBuffer()
        sb.append(m1_1)
        
        assert sb.extract_frame() is None
        
        sb.append(m1_2)
        
        f1 = sb.extract_frame()
        assert f1.command == 'CONNECT'
        assert f1.body == '0123456789'
        assert sb.extract_frame() is None
        
        sb.append(m1_3)
        f2 = sb.extract_frame()
        assert f2.command == 'SUBSCRIBE'        
        assert sb.extract_frame() is None
        
        sb.append(m1_4)
        f3 = sb.extract_frame()
        assert f3.command == 'SEND'
        assert f3.destination == '/queue/test'
        assert f3.body == '0123456789'
        
    def test_iteration(self):
        """ Test the iteration feature of our buffer."""
        sb = FrameBuffer()
        m1 = self.createMessage('connect', {'session': uuid.uuid4()}, 'This is the body')
        m2 = self.createMessage('send', {'destination': '/queue/sample'}, 'This is the body-2')
        print '%r' % m1
        print '%r' % m2
        sb.append(m1)
        sb.append(m2)
        
        assert sb is iter(sb)
        
        idx = 0
        expected = (m1, m2)
        for frame in sb:
            assert isinstance(frame, Frame)
            assert expected[idx] == frame.pack()
            idx += 1
        
        assert idx == 2
    
    