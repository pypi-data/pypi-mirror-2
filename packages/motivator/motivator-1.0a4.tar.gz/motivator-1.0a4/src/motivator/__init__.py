import sys
import time
from datetime import datetime
import random
from abc import abstractproperty, abstractmethod
from contextlib import contextmanager

import pyttsx


class Motivator(object):
  
    def __init__(self, music_player):
        self.music_player = music_player
        # XXX: the above (EnsureDispath on win) will prevent iTunes from closing
    
    @abstractproperty
    def gap(self):
        """Return the gap in seconds"""
        
    @abstractproperty
    def prelude(self):
        """Return the prelude text"""
        
    @abstractproperty
    def text(self):
        """Actual text to speak"""
        
    @contextmanager
    def faded_volume(self):
        """Reduce volume, run context code, and increase it back again"""
        if not self.music_player.is_playing():
            yield
            return
          
        orig = self.music_player.get_volume()
        for vol in range(orig, 0, -5) + [0]:
            time.sleep(0.1)
            self.music_player.set_volume(vol)
            
        yield
        
        for vol in range(5, orig, 5) + [orig]:
            time.sleep(0.1)
            self.music_player.set_volume(vol)
        
    def run(self):
        engine = pyttsx.init()
        
        while True:
            try:
                random.seed()
                with self.faded_volume():
                    engine.say(random.choice(self.prelude))
                    engine.runAndWait()
                    time.sleep(1)
                    engine.say(self.text)
                    engine.runAndWait()
                    print datetime.now()
                    
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


class iTunes(object):
  
    @abstractmethod
    def get_volume(self):
        """Return sound volume 0..100"""
        
    @abstractmethod
    def set_volume(self, volume):
        """Set sound volume 0..100"""
        
    @abstractmethod
    def is_playing(self):
        """Return True if music is playing"""
        
        
class iTunesOnWindows(iTunes):
  
    def __init__(self):
        import win32com.client
        self.o = win32com.client.gencache.EnsureDispatch('iTunes.Application')
        
    def get_volume(self):
        return self.o.SoundVolume
      
    def set_volume(self, v):
        assert 0 <= v <= 100
        self.o.SoundVolume = v
        
    def is_playing(self):
        return self.o.GetPlayerButtonsState()[1] == 2
        
        
class iTunesOnMac(iTunes):
    
    def __init__(self):
        from appscript import app
        self.o = app('iTunes')
        
    def get_volume(self):
        return self.o.sound_volume.get()
        
    def set_volume(self, v):
        assert 0 <= v <= 100
        self.o.sound_volume.set(v)
        
    def is_playing(self):
        return True # XXX: TODO
        
        
        
def create_itunes():
    if sys.platform.startswith('win'):
        return iTunesOnWindows()
    elif sys.platform.startswith('darwin'):
        return iTunesOnMac()
    else:
        raise NotImplementedError, 'need to write iTunes adapter on Unix'
      
  
def main():
    m = HAIETMOBAMotivator(create_itunes())
    m.run()
    
