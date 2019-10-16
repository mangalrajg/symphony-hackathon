import xml.etree.ElementTree as ET
from sym_api_client_python.processors.sym_message_parser import SymMessageParser
import logging
import re
import config


class FlagDealsProcessor:
    def get_response(self):
        return """
<div data-format="PresentationML" data-version="2.0">
       
  <br/>
       
  <h2>Deals impacted by the market disruptive event</h2>
       
       
  <br/>
       
  <form id="deals">
             
    <table>
    
       <tr>
      <th>Deal ID</th>
      <th>Underlying</th>
      <th>Client</th>
      <th>Notional</th>
      <th>To Flag</th>
   </tr>
   <tr>
      <td>#1</td>
      <td>SS1</td>
      <td>CITI</td>
      <td>$20,000,000</td>
          <td>
            <input name="tablesel-row-1" type="checkbox" value="on"/>
          </td>
   </tr>
   <tr>
      <td>#2</td>
      <td>SS2</td>
      <td>CITI</td>
      <td>$17,500,000</td>
          <td>
            <input name="tablesel-row-2" type="checkbox" value="on"/>
          </td>
   </tr>

   <tr>
      <td>#3</td>
      <td>CC1</td>
      <td>CITI</td>
      <td>$4,500,000</td>
          <td>
            <input name="tablesel-row-3" type="checkbox" value="on"/>
          </td>
   </tr>

   <tr>
      <td>#4</td>
      <td>SS1</td>
      <td>Client X</td>
      <td>$1,500,000</td>
          <td>
            <input name="tablesel-row-4" type="checkbox" value="on"/>
          </td>
   </tr>

   <tr>
      <td>#5</td>
      <td>SS1</td>
      <td>Client Y</td>
      <td>$1,500,000</td>
          <td>
            <input name="tablesel-row-5" type="checkbox" value="on"/>
          </td>
   </tr>

   <tr>
      <td>#6</td>
      <td>SS1</td>
      <td>Symphony</td>
      <td>$10,000</td>
          <td>
            <input name="tablesel-row-6" type="checkbox" value="on"/>
          </td>
   </tr>

    </table>
    <text-field name="id1" placeholder="Type OK" required="true"></text-field>
    <button type="reset">Reset</button>             
    <button name="select-options" type="action">Confirm</button>
         
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
        if re.match("flagdeals", msg_text[0]):
            f = FlagDealsProcessor()
            reply = f.get_response()
            stream_id = self.message_parser.get_stream_id(msg)
            config.global_stream_id = stream_id
            msg_to_send = dict(
                message=reply
            )
            self.bot_client.get_message_client(). \
                    send_msg(stream_id, msg_to_send)

        #else:
            msg_to_send = dict(
                message='<messageML>Hello {}, hope you are doing well! "{}"</messageML>'.format(
                    self.message_parser.get_im_first_name(msg), msg_text)
            )
            #self.bot_client.get_message_client(). \
            #        send_msg(stream_id, msg_to_send)
