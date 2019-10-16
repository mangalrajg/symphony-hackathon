import xml.etree.ElementTree as ET
from sym_api_client_python.processors.sym_message_parser import SymMessageParser
import logging
import re
import config


class BloombergProcessor:
    def get_response(self):
        return """
<div data-format="PresentationML" data-version="2.0">
  <br/>
  <h2>Late Price updated for following commodities</h2>
  <form id="update_price">
  <table>
     <tr>
      <th>Comodity</th>
      <th>Curency</th>
      <th>Code</th>
      <th>Price</th>
   </tr>
     <tr>
      <th>Orange Juice</th>
      <th>USD</th>
      <th>OJX20</th>
      <th><text-field name="id1x" placeholder="price" required="true">1.15</text-field></th>
   </tr>
  </table>
  <button name="update-button" type="action">Update Price</button> 
  </form>
  
</div>

"""


class MessageProcessor:
    def __init__(self, bot_client):
        self.bot_client = bot_client
        self.message_parser = SymMessageParser()

    def process(self, msg):
        logging.debug('insdie of process')
        msg_text = self.message_parser.get_text(msg)
        if not msg_text:
            return

        if re.match("Holding", msg_text[0]):
            f = BloombergProcessor()
            reply = f.get_response()
            stream_id = self.message_parser.get_stream_id(msg)
            config.global_stream_id = stream_id
            msg_to_send = dict(
                message=reply
            )
            self.bot_client.get_message_client(). \
                    send_msg(stream_id, msg_to_send)

        #else:
            #msg_to_send = dict(
            #    message='<messageML>Hello {}, hope you are doing well! "{}"</messageML>'.format(
            #        self.message_parser.get_im_first_name(msg), msg_text)
            #)
            #self.bot_client.get_message_client(). \
            #        send_msg(stream_id, msg_to_send)
