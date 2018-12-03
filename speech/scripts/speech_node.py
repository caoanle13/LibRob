#!/usr/bin/env python
import rospy
import json
from librarian_msgs.msg import UI, UI_feedback  # from package import message
import speech_recognition as sr
import NLP


# UI is the actual message
class Speech:
    def __init__(self):
        rospy.init_node('speech_node', anonymous=True)
        self.pub_command = rospy.Publisher('ui_command', UI, queue_size=10)
        self.pub_feedback = rospy.Publisher('ui_feedback', UI_feedback, queue_size=10)

        self.r = sr.Recognizer()
        self.mic = sr.Microphone(device_index = 2, sample_rate = 44100, chunk_size = 512)
        self.r.dynamic_energy_threshold = True
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)
        self.nlp = NLP()

        print('Speech node ready')

    def recognize(self, source, language):
        print('Speech starts listening')
        try:
            audio = self.r.listen(source, timeout=2.0, phrase_time_limit=8.0)

            print('Speech starts recognition')
            text = self.r.recognize_google(audio, language=language)
            print('Speech stops recognition')
            return True, text
        except Exception as e:
            return False, e

    # function to publish a given message on a given topic
    def publish(self, topic, msg_type, msg_payload):
        if topic == 'ui_command':
            msg = UI()
            msg.type = msg_type
            msg.payload = msg_payload
            self.pub_command.publish(msg)
        elif topic == 'ui_feedback':
            msg = UI_feedback()
            msg.type = msg_type
            msg.payload = msg_payload
            self.pub_feedback.publish(msg)
        else:
            print('Speech error: attempt to publish on unknown topic.')

    # ui_command listener calback
    def sub_command_callback(self, UI_msg): 

        if UI_msg.type == UI.SPEECH_TRIGGER:

            language = str(json.loads(UI_msg.payload)['language'])

            # speech recognition
            with self.mic as source:
                self.publish('ui_feedback', UI_feedback.LISTENING, json.dumps(True))
                recognised, recog_txt = self.recognize(source, language)
                self.publish('ui_feedback', UI_feedback.LISTENING, json.dumps(False))

                if recognised:
                    
                    print('You said: ', recog_txt)
                    # natural language processing
                    understood, nlp_txt = self.nlp.parse(recog_txt)

                    if understood:
                        print('Information extracted from NLP: ', nlp_txt)
                        self.publish('ui_command', UI.SEARCH_REQUEST, json.dumps({'request': nlp_txt}))
                    else:
                        self.publish('ui_command', UI.NOT_UNDERSTOOD, '')
                        print('Natural Language Processing error: ', nlp_txt)

                else:
                    self.publish('ui_command', UI.NOT_UNDERSTOOD, '')
                    print('Speech recognition error:', recog_txt)

    def startNode(self):
        self.sub_command = rospy.Subscriber('ui_command', UI, self.sub_command_callback)
        rospy.spin()


if __name__ == '__main__':
    speech = Speech()
    speech.startNode()
