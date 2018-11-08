#!/usr/bin/env python
import rospy
from librarian_msgs.msg import UI #from package import message
#UI is the actual message
class Speech:
    def __init__(self):
        rospy.init_node('speech_node', anonymous=True)
        self.pub = rospy.Publisher('ui_command',UI, queue_size=10) #speechrequest is the name of the topic you publishing on,UI is our custom message

    def callback(self, UI_msg): #message given by the data that is passed in this cadr UI_msg
        #UI_msg is the variable giving the function to the message
        if UI_msg.type == UI.SPEECH_TRIGGER:
            self.publisher()

    def receiver(self):
        self.rec=rospy.Subscriber('ui_command',UI,self.callback) #ui command is the topic and ui is the message
        rospy.spin() #keeps python from exiting until this node is stopped

    def publisher(self):
        msg = UI() #assigneda variable to the imported message object UI
        msg.type = UI.SEARCH_REQUEST
        msg.payload = "{'request':'Cao An book'}"
        self.pub.publish(msg)


if __name__=='__main__':
    speech=Speech()
    speech.receiver()

#topic need to publish on and receive is /ui_command
#message to use ui
#speech reqquest and speech trigger are the types needed to change
