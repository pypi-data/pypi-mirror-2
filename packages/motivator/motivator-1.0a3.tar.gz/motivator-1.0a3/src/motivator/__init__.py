import pyttsx
import time
import random
from abc import abstractproperty


class Motivator(object):
    
    @abstractproperty
    def gap(self):
        """Return the gap in seconds"""
        
    @abstractproperty
    def prelude(self):
        """Return the prelude text"""
        
    @abstractproperty
    def text(self):
        """Actual text to speak"""
        
    def run(self):
        engine = pyttsx.init()
        
        while True:
            try:
                random.seed()
                engine.say(random.choice(self.prelude))
                engine.runAndWait()
                time.sleep(1)
                engine.say(self.text)
                engine.runAndWait()
                time.sleep(self.gap)
            except KeyboardInterrupt:
                return
        
        
class HAIETMOBAMotivator(Motivator):

    @property
    def gap(self):
        return 60*5 # every 5 minutes recommended by srid
      
    @property
    def prelude(self):
        return ['Ask yourself', 'Ask yourself this now']
      
    @property
    def text(self):
        return 'How am I experiencing this moment of being alive?'

  
def main():
    m = HAIETMOBAMotivator()
    m.run()
    
