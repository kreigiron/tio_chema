from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
import logging
import db_mgr

class PluginPing(BaseActionPlugin):

  # This constructor is optional
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.threshold = 3
    self.counter = 0
    self.last_user = ""
    self.synchronous = True
    self.db = db_mgr.Factoider()

  def execute(self, ircMsg, userRole, *args, **kwargs):
    user = ircMsg.user
    if user == self.last_user:
      self.counter += 1
    else:
      self.counter = 0
      self.last_user = user

    self.db.put_ping(unicode(user), ircMsg.t)
    m = IRCMessage()
    if self.counter > self.threshold:
      #TODO: localize
      m.msg = "yarr, it's the {0} time you've called me!".format(self.counter)
    else:
      m.msg = "pong"
    m.channel = ircMsg.channel
    m.user = user
    m.directed = True
    logging.debug("User: {0} pinged".format(user))
    return m
