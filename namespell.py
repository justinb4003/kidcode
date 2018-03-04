#!/usr/bin/python
# Copyright Justin Buist

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import pango
import pygtk
import gtk
import gobject
import pyaudio
import wave
import threading
pygtk.require('2.0')

TARGET_TEXT = 'HARRIET'

# GTK Ops
def delete_event(widget, event, data=None):
    return False

def destroy(widget, data=None):
    gtk.main_quit()

def playSound(filename):
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
    playSound('applause.wav')

def playReset():
    playSound('boing.wav')

def name_onKeyPress(widget):
    inputText = widget.get_text()
    subTarget = TARGET_TEXT[:len(inputText)]
    if (inputText.lower() == subTarget.lower()):
        if (len(inputText) == len(TARGET_TEXT)):
            widget.set_text('')
            t = threading.Thread(target=playFinish)
            t.start() 
    else:
        playReset()
        widget.set_text('')
        

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


