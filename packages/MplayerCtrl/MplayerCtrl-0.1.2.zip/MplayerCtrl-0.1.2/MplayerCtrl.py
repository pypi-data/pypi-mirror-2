#!/usr/bin/env python
# -*- coding: utf -*-

'''
The MplayerCtrl is a wx.Panel with a special feature: you've access to a
Mplayer-process and the video-output is shown on the MplayerCtrl.


Dokumentation:
    - Mplayer-Documentation (args etc.)
    - Commands: http://www.mplayerhq.hu/DOCS/tech/slave.txt (similiar to the MplayerCtrl
        e.g. get_property changed to GetProperty and gamma to Gamma
    - http://mplayerctrl.dav1d.de


Licence (MIT):

    Copyright (c) 2010, David Herberth.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    
Example:

    import wx
    import MplayerCtrl as mpc
    
    class Frame(wx.Frame):
        def __init__(self, parent, id):
            wx.Frame.__init__(self, parent, id)
            
            self.mpc = mpc.MplayerCtrl(self, -1, 'mplayer.exe', media_file='testmovie.mpg')
            
            self.Bind(mpc.EVT_MEDIA_STARTED, self.on_media_started)
            self.Bind(mpc.EVT_MEDIA_FINISHED, self.on_media_finished)
            self.Bind(mpc.EVT_PROCESS_STARTED, self.on_process_started)
            self.Bind(mpc.EVT_PROCESS_STOPPED, self.on_process_stopped)
                    
            self.Show()
        
        def on_media_started(self, evt):
            print 'Media started!'
        def on_media_finished(self, evt):
            print 'Media finished!'
            self.mpc.Quit()
        def on_process_started(self, evt):
            print 'Process started!'
        def on_process_stopped(self, evt):
            print 'Process stopped!'
    
    if __name__ == '__main__':
        app = wx.App(redirect=False)
        f = Frame(None, -1)
        app.MainLoop()
'''

from subprocess import Popen, PIPE, STDOUT
from Queue import Queue
import threading
import wx
import wx.lib.newevent
import sys

__author__ = 'David Herberth'
__version_info__ = (0, 1, 2)
__version__ = '0.1.2'
__license__ = 'MIT'

MediaFinished, EVT_MEDIA_FINISHED = wx.lib.newevent.NewEvent()
MediaStarted, EVT_MEDIA_STARTED = wx.lib.newevent.NewEvent()
ProcessStopped, EVT_PROCESS_STOPPED = wx.lib.newevent.NewEvent() 
ProcessStarted, EVT_PROCESS_STARTED = wx.lib.newevent.NewEvent() 
Stderr, EVT_STDERR = wx.lib.newevent.NewEvent()

# -slave http://www.mplayerhq.hu/DOCS/tech/slave.txt

class BaseMplayerCtrlException(Exception):
    '''
    The exception is used as base for all other exceptions,
    useful to catch all exception thrown by the MplayerCtrl
    '''
    def __init__(self, *args):
        self.args = [repr(a).strip('\'') for a in args]
    def __str__(self):
        return ', '.join(self.args)

class AnsError(BaseMplayerCtrlException):
    '''
    The Exception is raised, if an ANS_ERROR is returned by the
    mplayer process.
    Reasons can be:
        * wrong value
        * unknown property
        * property is unavailable, e.g. the chapter property used while playing a stream
    '''
    pass

class BuildProcessError(BaseMplayerCtrlException):
    '''
    The Exception is raised, if the path to the mplayer(.exe) is incorrect
    or another error occurs while building the mplayer path
    '''
    pass


class MplayerStdoutEvents(threading.Thread):
    '''
    Class to handle the Stdout of a (Mplayer)process
        
    Some Events are posted, using wx.PostEvent
    * EVT_STDOUT_DATA_ARRIVED changed to self.queue.put
    * EVT_MEDIA_STARTED
    * EVT_MEDIA_FINISHED
    * EVT_PROCESS_STOPPED
    ''' 
    def __init__(self, win, stdout, queue):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.win = win
        self.stdout = stdout
        self.queue = queue
    def run(self):
        wx.PostEvent(self.win.GetEventHandler(), ProcessStarted()) # Really needed?
        s = False
        while True:
            evt = None
            line = self.stdout.readline()
            #if not line.upper().startswith('ANS_') and not '=' in line:
            #print line.encode('string-escape')
            if not line:
                evt = ProcessStopped()
            elif line == '\n': # universal_newlines = True (subprocess)!
                if s:
                    evt = MediaFinished()
                    s = False
            elif line.lower() == 'starting playback...\n':
                evt = MediaStarted()
                s = True
            try:
                if not evt is None:
                    wx.PostEvent(self.win.GetEventHandler(), evt)
                else:
                    if line.upper().startswith('ANS_') and '=' in line:
                        self.queue.put_nowait(line)
            except wx.PyDeadObjectError:
                break
            if isinstance(evt, ProcessStopped):
                break        

class MplayerStderrEvents(threading.Thread):
    '''
    Class to handle the Stderr of a (Mplayer)process
    
    Some Events are posted, using wx.PostEvent
    * EVT_STDERR_DATA_ARRIVED
    ''' 
    def __init__(self, win, stderr, stdout_event_thread):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.win = win
        self.stderr = stderr
        self._stdout_event_thread = stdout_event_thread
    def run(self):
        while self._stdout_event_thread.isAlive():
            line = self.stderr.readline().strip()
            #.strip() is important! A line, which just contain a line separator is unimportant
            #print 'STDERR ->->->', line
            if not line:
                break
            else:
                evt = Stderr(data=line)
            try:
                wx.PostEvent(self.win.GetEventHandler(), evt)
            except wx.PyDeadObjectError:
                break
            
class MplayerCtrl(wx.Panel):
    '''
    The MplayerCtrl, wraps the Mplayer into a wx.Panel
    it can be used as a Panel, but it also handles the mplayer process,
    using the subprocess-module
    '''
    #: All allowed properties for StepProperty
    step_properties = ('osdlevel', 'speed', 'chapter', 'angle', 'percent_pos',
                      'time_pos', 'volume', 'balance', 'mute', 'audio_delay', 'switch_audio',
                      'switch_angle', 'switch_title', 'fullscreen', 'deinterlace', 'ontop',
                      'rootwin', 'border', 'framedropping', 'gamma', 'brightness', 'contrast',
                      'saturation', 'hue', 'panscan', 'vsync', 'switch_video', 'switch_program',
                      'sub', 'sub_source', 'sub_file', 'sub_vob', 'sub_demux', 'sub_delay',
                      'sub_pos', 'sub_alignment', 'sub_visibility', 'sub_forced_only', 'sub_scale',
                      'tv_brightness', 'tv_contrast', 'tv_saturation', 'tv_hue', 'teletext_page',
                      'teletext_subpage', 'teletext_mode', 'teletext_format', 'teletext_half_page')
    #: All allowed properties for SetProperty
    set_properties = step_properties + ('stream_pos',)
    #: All allowed properties for GetProperty
    get_properties = set_properties  + \
                    ('pause', 'filename', 'path', 'demuxer', 'stream_start', 'stream_end',
                     'stream_length', 'chapters', 'length', 'metadata', 'audio_format',
                     'audio_codec', 'audio_bitrate', 'samplerate', 'channels', 'video_format',
                     'video_codec', 'video_bitrate', 'width', 'height', 'fps', 'aspect')
    
    def __init__(self, parent, id, mplayer_path, media_file=None, *args, **kwargs):
        '''Builds the "Panel", *args are arguments for the mplayer process
        just use it, if you know what you're doing.
        media_file can be a URL, a file (path), stream, everything the mplayer is able to play to
        Look at the kwargs! wid=True, slave=True, idle=True, noconsolecontrols=True, nofontconfig=True,
        vo=True (vo, gl), 
        these option are automatically added, except they are False or are already in "args"!
        => IMPORTANT <=
        Never add -msglevel to args!'''
        wx.Panel.__init__(self, parent, id)
        
        self._stdout_queue = Queue()
        self.mplayer_path = mplayer_path
        
        self.args = []
        self._process = None
        self._stdout = None
        self._stderr = None
        self._stdin = None
        
        self.Bind(EVT_MEDIA_STARTED, lambda x: self.post_event(MediaStarted()))
        self.Bind(EVT_MEDIA_FINISHED, lambda x: self.post_event(MediaFinished()))
        self.Bind(EVT_PROCESS_STARTED, lambda x: self.post_event(ProcessStarted()))
        self.Bind(EVT_PROCESS_STOPPED, lambda x: self.post_event(ProcessStopped()))
        self.Bind(EVT_STDERR, lambda x: self.post_event(Stderr(data=x.data)))
        
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_window_destroy)
                
        self.Start(media_file=media_file, *args, **kwargs)
    
    def _start_process(self, media_file, *args, **kwargs):
        args = list(args)
        if not args:
            args = [self.mplayer_path]
# -nofontconfig, -slave, -vf, spp,scale, -slave,
# -nosound, -msglevel, all=4, -noconsolecontrols, -nofontconfig,
# -fixed-vo, -vo, gl, -wid, str(self.GetHandle()), -idle'
        for option, value in [('wid',str(self.GetHandle())), ('slave',None),
                              ('noconsolecontrols',None),('nofontconfig',None),
                              ('vo','gl'), ('idle', None)]:
            if not '-%s'%option in args and not kwargs.get(option, False):
                add = ['-%s'%option]
                if not value is None:
                    add.append(value)
                args.extend(add)
        if '-msglevel' in args:
            mindex = args.index('-msglevel')
            if len(args) > mindex+1:
                args[mindex+1] = 'all=4'
            else:
                args.append('all=4') 
        else:
            args.extend(['-msglevel', 'all=4'])          
        if not media_file is None:
            args.append('%s'%media_file)
        if self._process is None:
            self.args = args
            try:
                self._process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            except Exception, e:
                raise BuildProcessError(str(e))
            self._stdin = self._process.stdin
            self._stdout = self._process.stdout
            self._stderr = self._process.stderr
            mse = MplayerStdoutEvents(self, self._stdout, self._stdout_queue)
            mse.start()
            MplayerStderrEvents(self, self._stderr, mse).start()
    
    def Start(self, media_file=None, *args, **kwargs):
        '''Builds a new process, if the old process got killed by Quit().
        Returns True if the process is created successfully, otherwise False'''
        if self._process is None:
            if not args:
                args = self.args
            self._start_process(media_file, *args, **kwargs)
        return self.is_alive()
    
    def post_event(self, evt):
        try:
            wx.PostEvent(self.Parent.GetEventHandler(), evt)
        except wx.PyDeadObjectError:
            pass
    
    def _get_from_queue(self):
        ret = self._stdout_queue.get(True)
        parsed_ret = parse_stdout(ret)
        self._stdout_queue.task_done()
        if parsed_ret[0] == 'ANS_ERROR':
            raise AnsError(parsed_ret[1])
        return parsed_ret[1]
    
   
    def is_alive(self):
        '''Returns True if the process is still alive otherwise False'''
        if not self._process is None:
            return (self._process.poll() is None)
        else:
            return False

    def AltSrcStep(self, value):
        '''(ASX playlist only)
        When more than one source is available it selects the next/previous one.'''
        self._stdin.write('alt_src_step %s\n' % (value))
    def AudioDelay(self, value, abs=None):
        '''Set/adjust the audio delay.
        If [abs] is not given or is zero, adjust the delay by <value> seconds.
        If [abs] is nonzero, set the delay to <value> seconds.'''
        self._stdin.write(build_cmd('audio_delay', value, abs))
    def Brightness(self, value, abs=None):
        '''Set/adjust video brightness.
        If [abs] is not given or is zero, modifies parameter by <value>.
        If [abs] is non-zero, parameter is set to <v        alue>.
        <value> is in the range [-100, 100].'''
        self._stdin.write(build_cmd('brightness', value, abs))
    def Contrast(self, value, abs=None):
        '''Set/adjust video contrast.
        If [abs] is not given or is zero, modifies parameter by <value>.
        If [abs] is non-zero, parameter is set to <value>.
        <value> is in the range [-100, 100].'''
        self._stdin.write(build_cmd('contrast', value, abs))
    def Gamma(self, value, abs=None):
        '''Set/adjust video gamma.
        If [abs] is not given or is zero, modifies parameter by <value>.
        If [abs] is non-zero, parameter is set to <value>.
        <value> is in the range [-100, 100].'''
        self._stdin.write(build_cmd('gamma', value, abs))
    def Hue(self, value, abs=None):
        '''Set/adjust video hue.
        If [abs] is not given or is zero, modifies parameter by <value>.
        If [abs] is non-zero, parameter is set to <value>.
        <value> is in the range [-100, 100].'''
        self._stdin.write(build_cmd('hue', value, abs))
    def Saturation(self, value, abs=None):
        '''Set/adjust video saturation.
        If [abs] is not given or is zero, modifies parameter by <value>.
        If [abs] is non-zero, parameter is set to <value>.
        <value> is in the range [-100, 100].'''
        self._stdin.write(build_cmd('saturation', value, abs))
    def ChangeRectangele(self, val1, val2):
        '''Change the position of the rectangle filter rectangle.
        
            <val1> Must be one of the following:
                   * 0 = width
                   * 1 = height
                   * 2 = x position
                   * 3 = y position
            <val2>
                * If <val1> is 0 or 1:
                   * Integer amount to add/subtract from the width/height.
                     Positive values add to width/height and negative values
                     subtract from it.
                * If <val1> is 2 or 3:
                   * Relative integer amount by which to move the upper left
                     rectangle corner. Positive values move the rectangle
                     right/down and negative values move the rectangle left/up.'''
        self._stdin.write('change_rectangle %s %s\n' % (val1, val2))
    def DvbSetChannel(self, channel_number, card_number):
        '''Set DVB channel'''
        self._stdin.write('dvb_set_channel %s %s\n' % (channel_number, card_number))
    def Dvdnav(self, button_name):
        '''Press the given dvdnav button.
            up
            down
            left
            right
            menu
            select
            prev
            mouse'''
        self._stdin.write('dvdnav %s\n' (button_name))
    def Edlmark(self):
        '''Write the current position into the EDL file.'''
        self._stdin.write('edl_mark\n')
    def FrameDrop(self, value):
        '''Toggle/set frame dropping mode.'''
        self._stdin.write('frame_drop %s\n' % (value))
    def GetAudioBitrate(self):
        '''Returns the audio bitrate of the current file.'''
        self._stdin.write('get_audio_bitrate\n')
        return self._get_from_queue()
    def GetAudioCodec(self):
        '''Returns the audio codec name of the current file.'''
        self._stdin.write('get_audio_codec\n')
        return self._get_from_queue()
    def GetAudioSamples(self):
        '''Returns the audio frequency and number of channels of the current file.'''
        self._stdin.write('get_audio_samples\n')
        return self._get_from_queue()
    def GetFileName(self):
        '''Retruns the name of the current file.'''
        self._stdin.write('get_file_name\n')
        return self._get_from_queue()
    def GetMetaAlbum(self):
        '''Returns the "Album" metadata of the current file.'''
        self._stdin.write('get_meta_album\n')
        return self._get_from_queue()
    def GetMetaArtist(self):
        '''Returns the "Artist" metadata of the current file.'''
        self._stdin.write('get_meta_artist\n')
        return self._get_from_queue()
    def GetMetaComment(self):
        '''Returns the "Comment" metadata of the current file.'''
        self._stdin.write('get_meta_comment\n')
        return self._get_from_queue()
    def GetMetaGenre(self):
        '''Returns the "Genre" metadata of the current file.'''
        self._stdin.write('get_meta_genre\n')
        return self._get_from_queue()
    def GetMetaTitle(self):
        '''Returns the "Title" metadata of the current file.'''
        self._stdin.write('get_meta_title\n')
        return self._get_from_queue()
    def GetMetaTrack(self):
        '''Returns the "Track" metadata of the current file.'''
        self._stdin.write('get_meta_track\n')
        return self._get_from_queue()
    def GetMetaYear(self):
        '''Returns the "Year" metadata of the current file.'''
        self._stdin.write('get_meta_year\n')
        return self._get_from_queue()
    def GetPercentPos(self):
        '''Returns the current position in the file, as integer percentage [0-100].'''
        self._stdin.write('get_percent_pos\n')
        return self._get_from_queue()
    # get_proprty
    def GetProperty(self, property):
        '''Returns the current value of a property.
        All possible properties => :attr:`~MplayerCtrl.get_properties` (a tuple)
        If property isn't a "get-property", raises :exc:`~MplayerCtrl.AnsError`'''
        property = property.lower()
        if property in self.get_properties:
            self._stdin.write('get_property %s\n' % (property))
            ret = self._get_from_queue()
            if property == 'metadata':
                # metadata looks like that: key1,value1,key2,value2,key3,value3 ...
                # let's make a dict out of it!
                key, value = ret.split(',')[::2], ret.split(',')[1::2]
                ret = dict(zip(key, map(get_type, value)))
            return ret
        else:
            raise AnsError('PROPERTY_UNKNOWN')
    def GetSubVisibility(self):
        '''Returns subtitle visibility (1 == on, 0 == off).'''
        self._stdin.write('get_sub_visibility\n')
        return self._get_from_queue()
    def GetTimeLength(self):
        '''Returns the length of the current file in seconds.'''
        self._stdin.write('get_time_length\n')
        return self._get_from_queue()
    def GetTimePos(self):
        '''Returns the current position in the file in seconds, as float.'''
        self._stdin.write('get_time_pos\n')
        return self._get_from_queue()
    def GetVoFullscreen(self):
        '''Returns fullscreen status (1 == fullscreened, 0 == windowed).'''
        self._stdin.write('get_vo_fullscreen\n')
        return self._get_from_queue()
    def GetVideoBitrate(self):
        '''Returns the video bitrate of the current file.'''
        self._stdin.write('get_video_bitrate\n')
        return self._get_from_queue()
    def GetVideoCodec(self):
        '''Returns out the video codec name of the current file.'''
        self._stdin.write('get_video_codec\n')
        return self._get_from_queue()
    def GetVideoResoloution(self):
        '''Returns the video resolution of the current file.'''
        self._stdin.write('get_video_resoloution\n')
        return self._get_from_queue()
    def Screenshot(self, value):
        '''Take a screenshot. Requires the screenshot filter to be loaded.
            0 Take a single screenshot.
            1 Start/stop taking screenshot of each frame.'''
        self._stdin.write('screenshot %s\n' % (value))
    # gui_[about|loadfile|loadsubtitle|play|playlist|preferences|skinbrowser|stop]    
    def KeyDownEvent(self, value):
        '''Inject <value> key code event into MPlayer.'''
        self._stdin.write('key_down_event %s\n' % (value))
    def Loadfile(self, file_url, append=None):
        '''Load the given file/URL, stopping playback of the current file/URL.
        If <append> is nonzero playback continues and the file/URL is
        appended to the current playlist instead.'''
        self._stdin.write(build_cmd('loadfile', file_url, append))
    def Loadlist(self, file_, append=None):
        '''Load the given playlist file, stopping playback of the current file.
        If <append> is nonzero playback continues and the playlist file is
        appended to the current playlist instead.'''
        self._stdin.write(build_cmd('loadlist %', file_, append))
    def Loop(self, value, abs=None):
        '''Adjust/set how many times the movie should be looped. -1 means no loop,
        and 0 forever.'''
        self._stdin.write(build_cmd('loop', value, abs))
    def Menu(self, command):
        '''Execute an OSD menu command.
            * up     Move cursor up.
            * down   Move cursor down.
            * ok     Accept selection.
            * cancel Cancel selection.
            * hide   Hide the OSD menu.'''
        self._stdin.write('menu %s\n' % (command))
    def SetMenu(self, menu_name):
        '''Display the menu named <menu_name>.'''
        self._stdin.write('set_menu %s\n' % (menu_name))
    def Mute(self, value=None):
        '''Toggle sound output muting or set it to [value] when [value] >= 0
        (1 == on, 0 == off).'''
        self._stdin.write(build_cmd('mute', value))
    def Osd(self, level=None):
        '''Toggle OSD mode or set it to [level] when [level] >= 0.'''
        self._stdin.write(build_cmd('osd', level))
    def OsdShowPropertyText(self, string, duration=None, level=None):
        '''Show an expanded property string on the OSD, see -playing-msg for a
        description of the available expansions. If [duration] is >= 0 the text
        is shown for [duration] ms. [level] sets the minimum OSD level needed
        for the message to be visible (default: 0 - always show).'''
        self._stdin.write(build_cmd('osd_show_property_text', string, level))
    def OsdShowText(self, string, duration=None, level=None):
        '''Show <string> on the OSD.'''
        self._stdin.write(build_cmd('osd_show_property_text', string, level))
    def Panscan(self, value, abs):
        '''Increase or decrease the pan-and-scan range by <value>, 1.0 is the maximum.
        Negative values decrease the pan-and-scan range.
        If <abs> is != 0, then the pan-and scan range is interpreted as an
        absolute range.'''
        self._stdin.write('panscan %s %s\n' % (value, abs))
    def Pause(self):
        '''Pause/unpause the playback.'''
        self._stdin.write('pause\n')
    def FrameStep(self):
        '''Play one frame, then pause again.'''
        self._stdin.write('frame_step\n')
    def PtStep(self, value, force=None):
        '''Go to the next/previous entry in the playtree. The sign of <value> tells
            the direction.  If no entry is available in the given direction it will do
            nothing unless [force] is non-zero.'''
        self._stdin.write(build_cmd('pt_step', value, force))
    def PtUpStep(self, value, force=None):
        '''Similar to pt_step but jumps to the next/previous entry in the parent list.
        Useful to break out of the inner loop in the playtree.'''
        self._stdin.write(build_cmd('pt_up_step', value, force))
    def Quit(self):
        '''Sends a quit to the mplayer process, if the mplayer is still alive,
        process will terminated, if that doesn't work process will be killed.
        The panel will not be destroyed!
        Returns True, if the process got terminated successfully, otherwise False''' 
        if self.is_alive():
            self._stdin.write('quit\n')
            self._stdin.flush()
            if sys.version_info[:2] > (2, 5):
                self._process.terminate()
                if self.is_alive():
                    self._process.kill()
            self._process, self._stderr, self._stdin, self._stdout = [None]*4
        return not self.is_alive()    
    def RadioSetChannel(self, channel):
        '''Switch to <channel>. The 'channels' radio parameter needs to be set.'''
        self._stdin.write('radio_set_channel %s\n' % (channel))
    def RadioSetFreq(self, freq):
        '''Set the radio tuner frequency.
            freq in Mhz'''
        self._stdin.write('radio_set_freq %s\n' % (freq))
    def RadioStepChannel(self, value):
        '''Step forwards (1) or backwards (-1) in channel list. Works only when the
        'channels' radio parameter was set.'''
        self._stdin.write('radio_step_channel %s' % (value))
    def RadioStepFreq(self, value):
        '''Tune frequency by the <value> (positive - up, negative - down).'''
        self._stdin.write('radio_step_freq %s\n' % (value))
    def Seek(self, value, type_=None):
        '''Seek to some place in the movie.
            0 is a relative seek of +/- <value> seconds (default).
            1 is a seek to <value> % in the movie.
            2 is a seek to an absolute position of <value> seconds.'''
        self._stdin.write(build_cmd('seek', value, type_))
    def SeekChapter(self, value, type_=None):
        '''Seek to the start of a chapter.
            0 is a relative seek of +/- <value> chapters (default).
            1 is a seek to chapter <value>.'''
        self._stdin.write(build_cmd('seek_chapter', value, type_))
    def SwitchAngle(self, value):
        '''Switch to the angle with the ID [value]. Cycle through the
        available angles if [value] is omitted or negative.'''
        self._stdin.write('switch_angle %s\n' % (value))
    def SetMousePos(self, x, y):
        '''Tells MPlayer the coordinates of the mouse in the window.
        This command doesn't move the mouse!'''
        self._stdin.write('set_mouse_pos %s %s\n' % (x, y))
    # set_property
    def SetProperty(self, property, value):
        '''Sets a property.
        All possible properties => :attr:`~MplayerCtrl.set_properties` (a tuple)
        If property isn't a "set-property", raises :exc:`~MplayerCtrl.AnsError`'''
        if not property in self.set_properties:
            raise AnsError('PROPERTY_UNKNOWN')
        else:
            self._stdin.write('set_property %s %s\n' % (property, value))
    def SpeedIncr(self, value):
        '''Add <value> to the current playback speed.'''
        self._stdin.write('speed_incr %s\n' % (value))
    def SpeedMult(self, value):
        '''Multiply the current speed by <value>.'''
        self._stdin.write('speed_mult %s\n' % (value))
    def SpeedSet(self, value):
        '''Set the speed to <value>.'''
        self._stdin.write('speed_set %s\n' % (value))
    # step_property
    def StepProperty(self, property, value=None, direction=None):
        '''Change a property by value, or increase by a default if value is
        not given or zero. The direction is reversed if direction is less
        than zero.
        All possible properties => :attr:`~MplayerCtrl.step_properties` (a tuple)
        If property isn't a "step-property", raises :exc:`~MplayerCtrl.AnsError`'''
        if property in self.step_properties:
            self._stdin.write(build_cmd('step_property', property, value, direction))
        else:
            raise AnsError('PROPERTY_UNKNOWN')
    def Stop(self):
        '''Stop playback.'''
        self._stdin.write('stop')
    def SubAlignment(self, value=None):
        '''Toggle/set subtitle alignment.
            0 top alignment
            1 center alignment
            2 bottom alignment'''
        self._stdin.write(build_cmd('sub_alignment', value))
    def SubDelay(self, value, abs=None):
        '''Adjust the subtitle delay by +/- <value> seconds or set it to <value>
        seconds when [abs] is nonzero.'''
        self._stdin.write(build_cmd('sub_delay', value, abs))
    def SubLoad(self, subtitle_file):
        '''Loads subtitles from <subtitle_file>.'''
        self._stdin.write('sub_load %s\n' % (subtitle_file))
    def SubLog(self):
        '''Logs the current or last displayed subtitle together with filename
        and time information to ~/.mplayer/subtitle_log. Intended purpose
        is to allow convenient marking of bogus subtitles which need to be
        fixed while watching the movie.'''
        self._stdin.write('sub_log\n')
    def SubPos(self, value, abs=None):
        '''Adjust/set subtitle position.'''
        self._stdin.write(build_cmd('sub_pos', value, abs))
    def SubRemove(self, value):
        '''If the [value] argument is present and non-negative, removes the subtitle
        file with index [value]. If the argument is omitted or negative, removes
        all subtitle files.'''
        self._stdin.write('sub_remove %s\n' % (value))
    def SubSelect(self, value):
        '''Display subtitle with index [value]. Turn subtitle display off if
        [value] is -1 or greater than the highest available subtitle index.
        Cycle through the available subtitles if [value] is omitted or less
        than -1. Supported subtitle sources are -sub options on the command
        line, VOBsubs, DVD subtitles, and Ogg and Matroska text streams.
        This command is mainly for cycling all subtitles, if you want to set
        a specific subtitle, use SubFile, SubVob, or SubDemux.'''
        self._stdin.write('sub_select %s\n' % (value))
    def SubSource(self, source):
        '''Display first subtitle from [source]. Here [source] is an integer:
        SUB_SOURCE_SUBS   (0) for file subs
        SUB_SOURCE_VOBSUB (1) for VOBsub files
        SUB_SOURCE_DEMUX  (2) for subtitle embedded in the media file or DVD subs.
        If [source] is -1, will turn off subtitle display. If [source] less than -1,
        will cycle between the first subtitle of each currently available sources.'''
        self._stdin.write('sub_source %s\n' % (source))
    def SubFile(self, value):
        '''Display subtitle specifid by [value] for file subs. The [value] is
        corresponding to ID_FILE_SUB_ID values reported by '-identify'.
        If [value] is -1, will turn off subtitle display. If [value] less than -1,
        will cycle all file subs.'''
        self._stdin.write('sub_file %s\n' % (value))
    def SubVob(self, value):
        '''Display subtitle specifid by [value] for vobsubs. The [value] is
        corresponding to ID_VOBSUB_ID values reported by '-identify'.
        If [value] is -1, will turn off subtitle display. If [value] less than -1,
        will cycle all vobsubs.'''
        self._stdin.write('sub_vob %s\n' % (value))
    def SubDemux(self, value):
        '''Display subtitle specifid by [value] for subtitles from DVD or embedded
        in media file. The [value] is corresponding to ID_SUBTITLE_ID values
        reported by '-identify'. If [value] is -1, will turn off subtitle display.
        If [value] less than -1, will cycle all DVD subs or embedded subs.'''
        self._stdin.write('sub_demux %s\n' % (value))
    def SubScale(self, value, abs=None):
        '''Adjust the subtitle size by +/- <value> or set it to <value> when [abs]
        is nonzero.'''
        self._stdin.write(build_cmd('sub_scale', value, abs))
    def VobsubLang(self, *args):
        '''This is a stub linked to SubSelect for backwards compatibility.'''
        self.SubScale(*args)
    def SubStep(self, value):
        '''Step forward in the subtitle list by <value> steps or backwards if <value>
        is negative.'''
        self._stdin.write('sub_step %s\n' % (value))
    def SubVisibility(self, value=None):
        '''Toggle/set subtitle visibility.'''
        self._stdin.write(build_cmd('sub_visibility', value))
    def ForcedSubsOnly(self, value=None):
        '''Toggle/set forced subtitles only.'''
        self._stdin.write(build_cmd('forced_subs_only', value))
    def SwitchAudio(self, value=None):
        '''Switch to the audio track with the ID [value]. Cycle through the
        available tracks if [value] is omitted or negative.'''
        self._stdin.write(build_cmd('switch_audio', value))
    def SwitchAngle(self, value=None):
        '''Switch to the DVD angle with the ID [value]. Cycle through the
        available angles if [value] is omitted or negative.'''
        self._stdin.write(build_cmd('switch_angle', value))
    def SwitchRatio(self, value):
        '''Change aspect ratio at runtime. [value] is the new aspect ratio expressed
        as a float (e.g. 1.77778 for 16/9).
        There might be problems with some video filters.'''
        self._stdin.write('switch_ratio %s\n' % (value))
    def SwitchTitle(self, value=None):
        '''Switch to the DVD title with the ID [value]. Cycle through the
        available titles if [value] is omitted or negative.'''
        self._stdin.write(build_cmd('switch_title',  value))
    def SwitchVsync(self, value=None):
        '''Toggle vsync (1 == on, 0 == off). If [value] is not provided,
        vsync status is inverted.'''
        self._stdin.write(build_cmd('switch_vsync', value))
    def TeletextAddDigit(self, value):
        '''Enter/leave teletext page number editing mode and append given digit to
        previously entered one.
            * 0..9 Append apropriate digit. (Enables editing mode if called from normal
              mode, and switches to normal mode when third digit is entered.)
            * Delete last digit from page number. (Backspace emulation, works only
              in page number editing mode.)'''
        self._stdin.write('teletext_add_digit %s\n' % (value))
    def TeletextGoLink(self, value):
        '''Follow given link on current teletext page.
        value must be 1,2,3,4,5 or 6'''
        self._stdin.write('teletext_go_link %s\n' % (value))
    def TvStartScan(self):
        '''Start automatic TV channel scanning.'''
        self._stdin.write('tv_start_scan\n')
    def TvStepChannel(self, channel):
        '''Select next/previous TV channel.'''
        self._stdin.write('tv_step_channel %s\n' % (channel))
    def TvStepNorm(self):
        '''Change TV norm.'''
        self._stdin.write('tv_step_norm\n')
    def TvStepChanlist(self):
        '''Change channel list.'''
        self._stdin.write('tv_step_chanlist\n')
    def TvSetChannel(self, channel):
        '''Set the current TV channel.'''
        self._stdin.write('tv_set_channel %s\n' % (channel))
    def TvLastChannel(self):
        '''Set the current TV channel to the last one.'''
        self._stdin.write('tv_last_channel\n')
    def TvSetFreq(self, freq):
        '''Set the TV tuner frequency.
        freq offset in Mhz'''
        self._stdin.write('tv_set_freq %s\n' % (freq))
    def TvStepFreq(self, freq):
        '''Set the TV tuner frequency relative to current value.
        freq offset in Mhz'''
        self._stind.write('tv_step_freq %s\n' % (freq))
    def TvSetNorm(self, norm):
        '''Set the TV tuner norm (PAL, SECAM, NTSC, ...).'''
        self._stdin.write('tv_set_norm %s\n' % (norm))
    def TvSetBrightness(self, value, abs=None):
        '''Set TV tuner brightness or adjust it if [abs] is set to 0.
        value from -100 to 100'''
        self._stdin.write(build_cmd('tv_set_brightness', value, abs))
    def TvSetContrast(self, value, abs=None):
        '''Set TV tuner contrast or adjust it if [abs] is set to 0.
        value from -100 to 100'''
        self._stdin.write(build_cmd('tv_set_contrast', value, abs))
    def TvSetHue(self, value, abs=None):
        '''Set TV tuner hue or adjust it if [abs] is set to 0.
        value from -100 to 100'''
        self._stdin.write(build_cmd('tv_set_hue', value, abs))
    def TvSetSaturation(self, value, abs=None):
        '''Set TV tuner saturation or adjust it if [abs] is set to 0.
        value from -100 to 100'''
        self._stdin.write(build_cmd('tv_set_saturation', value, abs))
    def UseMaster(self):
        '''Switch volume control between master and PCM.'''
        self._stdin.write('use_master\n')
    def VoBorder(self, value=None):
        '''Toggle/set borderless display.'''
        self._stdin.write(build_cmd('vo_border', value))
    def VoFullscreen(self, value=None):
        '''Toggle/set fullscreen mode'''
        self._stdin.write(build_cmd('vo_fullscreen', value))
    def VoOntop(self, value):
        '''Toggle/set stay-on-top.'''
        self._stdin.write(build_cmd('vo_ontop', value))
    def VoRootwin(self, value=None):
        '''Toggle/set playback on the root window.'''
        self._stdin.write(build_cmd('vo_rootwin', value))
    # help
    # exit
    # hide
    # run
    def on_window_destroy(self, evt):
        self.Quit()
        evt.Skip()

    def Destroy(self):
        self.Quit()
        wx.Panel.Destroy(self)
    Destroy.__doc__ = wx.Panel.Destroy.__doc__

def get_type(val, *types):
    if not types:
        types = (int, float, str)
    for f in types: 
        try:
            return f(val)
        except ValueError:
            pass
    return val

def parse_stdout(line):
    line = line.strip()
    if '=' in line:
        s, val = line.split('=', 1)
        val = val.strip('\'')
        s = s.upper()
        if not s.startswith('ANS_'):
            return (None, None)
        else:
            ret = get_type(val)
        return s, ret
    return (None, None)

def build_cmd(*args):
    return ' '.join(str(i) for i in args if not i is None) + '\n'
