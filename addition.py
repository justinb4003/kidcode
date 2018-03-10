#!/usr/bin/python
# Copyright Justin Buist

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import os
import random
import pango
import pygtk
import gtk
import gobject
import pyaudio
import wave
import threading
import time
from pygame import mixer
import pygame
pygtk.require('2.0')

TARGET_TEXT = ''


def playSound(filename):
    mixer.music.load(filename)
    mixer.music.play()
    while mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def playCorrect():
    playSound('applause.wav')

def playWrong():
    playSound('boing.wav')

def delete_event(widget, event, data=None):
    return False

def destroy(widget, data=None):
    gtk.main_quit()

def nextWord():
    global TARGET_TEXT
    global repeatButton
    idx = random.randint(0, len(word_list) - 1)
    TARGET_TEXT = word_list[idx]
    playWord(TARGET_TEXT)
    spellInput.set_text('')
    spellInput.grab_focus()
    repeatButton.set_sensitive(True)


def endAndNext():
    global spellInput
    playFinish()
    time.sleep(0.25)
    nextWord()

def startOver():
    global spellInput
    playReset()
    time.sleep(0.25)
    playWord(TARGET_TEXT)
    spellInput.set_text('')
    spellInput.grab_focus()

#def num_onKeyPress(widget):
#    inputText = widget.get_text()
#    subTarget = TARGET_TEXT[:len(inputText)]
#    if (inputText.lower() == subTarget.lower()):
#        if (len(inputText) == len(TARGET_TEXT)):
#            t = threading.Thread(target=endAndNext)
#            t.start()
#    else:
#        t = threading.Thread(target=startOver)
#        t.start()

def buttonCheck_click(widget, data=None):
    global numInput
    inputText = numInput.get_text()
    if (inputText == TARGET_TEXT):
        playCorrect()
        setupProblem()
        numInput.set_text('')
    else:
        playWrong()
        numInput.grab_focus()


def setupProblem():
    global num1
    global num2
    global TARGET_TEXT
    num1 = random.randint(0, 999)
    num2 = random.randint(0, 999)
    answer = num1 + num2
    TARGET_TEXT = str(answer)
    
pygame.init()
mixer.init()

gobject.threads_init()

window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_border_width(10)
window.connect("delete_event", delete_event)
window.connect("destroy", destroy)

inputFont = pango.FontDescription("Monospace 36")

num1 = 0
num2 = 0


setupProblem()



numTop = gtk.Label()
numTop.modify_font(inputFont)
numTop.set_justify(gtk.JUSTIFY_RIGHT)
numTop.set_text(str(num1))

numBtm = gtk.Label()
numBtm.modify_font(inputFont)
numBtm.set_justify(gtk.JUSTIFY_RIGHT)
numBtm.set_text(str(num2))




numInput = gtk.Entry()
numInput.modify_font(inputFont)
numInput.set_alignment(1.0)
#numInput.connect('changed', num_onKeyPress)

checkButton = gtk.Button('Check Answer')
checkButton.connect("clicked", buttonCheck_click)


ralign = gtk.Alignment(1, 0, 0, 0)


vbox = gtk.VBox()
vbox.add(numTop)
vbox.add(numBtm)
vbox.add(numInput)
vbox.add(checkButton)

ralign.add(vbox)

window.add(ralign)
#window.set_size_request(400, 100)
window.show_all()
window.show()
gtk.main()
