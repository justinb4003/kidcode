#!/usr/bin/python
# Copyright Justin Buist

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import contextlib
import pango
import pygtk
import gtk
import gobject
import pyaudio
import wave
import threading
import os
import sys
pygtk.require('2.0')


TARGET_TEXT = 'HARRIET'

# Use in a 'with' block to supress stderr messages for the duration of
# the block
@contextlib.contextmanager
def ignore_stderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)


def playSound(filename):
    with ignore_stderr():
        chunk = 1024
        f = wave.open(filename, "rb")
        p = pyaudio.PyAudio()
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),
                        rate = f.getframerate(),
                        output = True)
        data = f.readframes(chunk)
        while data:
            stream.write(data)
            data = f.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()

def playFinish():
    t = threading.Thread(target=playSound, args=['applause.wav'])
    t.start()

def playReset():
    t = threading.Thread(target=playSound, args=['boing.wav'])
    t.start()

# BEGIN GTK Event Ops
def delete_event(widget, event, data=None):
    return False

def destroy(widget, data=None):
    gtk.main_quit()

def name_onKeyPress(widget):
    inputText = widget.get_text()
    subTarget = TARGET_TEXT[:len(inputText)]
    if (inputText.lower() == subTarget.lower()):
        if (len(inputText) == len(TARGET_TEXT)):
            # The uesr has typed in every character correct. Notify via sound
            # and then reset the input text widget.
            playFinish()
            widget.set_text('')
    else:
        # The user has typed a character wrong.  Notify via sound and then
        # reset the input text widget.
        playReset()
        widget.set_text('')

# END GTK Event Ops
        

# If this isn't called then the main GTK method will get all manner
# of hosed up if you try and create other threads.
gobject.threads_init()

window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_border_width(10)
window.connect("delete_event", delete_event)
window.connect("destroy", destroy)

vbox = gtk.VBox()

nameFont = pango.FontDescription("Monospace 24")

nameLabel = gtk.Label()
nameLabel.set_justify(gtk.JUSTIFY_LEFT)
nameLabel.modify_font(nameFont)
nameLabel.set_text(TARGET_TEXT)

nameInput = gtk.Entry()
nameInput.modify_font(nameFont)
nameInput.connect('changed', name_onKeyPress)

vbox.add(nameLabel)
vbox.add(nameInput)
window.add(vbox)
window.set_size_request(300, -1)
window.show_all()
window.show()
gtk.main()


