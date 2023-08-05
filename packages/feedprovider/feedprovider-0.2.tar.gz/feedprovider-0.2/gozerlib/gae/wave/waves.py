# gozerlib/wave/waves.py
#
#

""" class to repesent a wave. """

## gozerlib imports

from gozerlib.channelbase import ChannelBase
from gozerlib.utils.exception import handle_exception
## 

from simplejson import dumps

## google imports

import google

## basic imports

import logging
import copy
import os

cpy = copy.deepcopy

class Wave(ChannelBase):

    """ a wave is seen as a channel. """

    def __init__(self, waveid):
        ChannelBase.__init__(self, 'gozerdata' + os.sep + 'waves' + os.sep + waveid)
        self.data.seenblips = self.data.seenblips or 0
        self.data.threshold = self.data.threshold or -1
        self.data.nrcloned = self.data.nrcloned or 0
        self.data.waveid = waveid
        self.wavelet = None
        self.event = None
        logging.debug("created wave with id: %s" % waveid)

    def parse(self, event, wavelet):

        """ parse event into a Wave. """

        self.data.json_data = event.json
        self.data.title = wavelet._title
        self.data.waveletid = wavelet._wavelet_id
        self.wavelet = wavelet
        self.event = event
        logging.debug("parsed %s (%s) channel" % (self.id, self.data.title))
        return self

    def settitle(self, title):
        self.event.set_title(title)

    def clone(self, bot, event, title=None):
        parts = list(event.root.participants)
        newwave = bot.newwave(event.domain, parts)
        logging.warn("wave - clone - populating wave with %s" % str(parts))
        for id in parts:
            newwave.participants.add(id)
        if title:
            newwave._set_title(title)

        try:
            txt = '\n'.join(event.rootblip.text.split('\n')[2:])
        except IndexError:
            txt = event.rootblip.text

        newwave._root_blip.append(u'%s\n' % txt)

        for element in event.rootblip.elements:
            if element.type == 'GADGET':
                newwave._root_blip.append(element)

        #gadgetblip = newwave.reply()
        #from waveapi.element import Gadget
        #gadgetblip.append(Gadget("http://feedprovider.appspot.com/feedform.xml"))

        blip = newwave.reply()
        blip.append("\nthis wave is cloned from %s\n" % event.url)
        wavelist = bot.submit(newwave)
        logging.warn("wave - clone - %s - submit returned %s" % (list(newwave.participants), str(wavelist)))

        if not wavelist:
            logging.warn("submit of new wave failed")
            return

        try:
            waveid = None
            for item in wavelist:
                try:
                    waveid = item['data']['waveId']
                except (KeyError, ValueError):
                    continue
        
            logging.warn("wave - newwave id is %s" % waveid)
            if waveid and 'sandbox' in waveid:
                url = "https://wave.google.com/a/wavesandbox.com/#restored:wave:%s" % waveid.replace('w+','w%252B')
            else:
                url = "https://wave.google.com/wave/#restored:wave:%s" % waveid.replace('w+','w%252B')
            wave = Wave(waveid)
            wave.parse(event, newwave)
            wave.data.threshold = self.data.threshold or 200
            wave.data.nrcloned = self.data.nrcloned + 1
            wave.data.url = url
            wave.save()

            oldwave = Wave(event.waveid)
            oldwave.data.threshold = -1
            oldwave.save()

        except AttributeError, ex:
            logging.error("wave - no waveid found %s" % str(ex))
            return

        return wave

    def say(self, bot, txt):

        """ output some txt to the wave. """

        if self.data.json_data:
            logging.debug("wave - say - using BLIND - %s" % self.data.json_data) 
            wavelet = bot.blind_wavelet(self.data.json_data)
        else:
            logging.info("did not join channel %s" % self.id)
            return

        if not wavelet:
            logging.error("cant get wavelet")
            return

        logging.warn('wave - out - %s - %s' % (self.data.title, txt))
        wavelet.reply(txt)

        try:
            bot.submit(wavelet)
        except google.appengine.api.urlfetch_errors.DownloadError:
            handle_exception()
            #pass

    def toppost(self, bot, txt):

        """ output some txt to the wave. """

        if self.data.json_data:
            logging.debug("wave - say - using BLIND - %s" % self.data.json_data) 
            wavelet = bot.blind_wavelet(self.data.json_data)
        else:
            logging.info("did not join channel %s" % self.id)
            return

        if not wavelet:
            logging.error("cant get wavelet")
            return

        logging.warn('wave - out - %s - %s' % (self.data.title, txt))

        try:
            blip = wavelet._root_blip.reply()
            blip.append(txt)
            bot.submit(wavelet)
        except google.appengine.api.urlfetch_errors.DownloadError:
            handle_exception()
            #pass
