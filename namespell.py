#!/usr/bin/python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import pygtk
import gtk
pygtk.require('2.0')

# GTK Ops
def delete_event(widget, event, data=None):
    print('Delete hit.')
    return False

def destroy(widget, data=None):
    print('Destroy hit.')
    gtk.main_quit()
    app_running = False
    print('main_quit() completed.')


window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_border_width(10)
window.connect("delete_event", delete_event)
window.connect("destroy", destroy)

vbox = gtk.VBox()

nameLabel = gtk.Label()
nameLabel.set_markup('<span font_size="xx-large"><tt>HARRIET</tt></span>')
nameLabel.set_use_markup(True)

nameInput = gtk.TextView()
nameInputBuf = nameInput.get_buffer()
sz = nameInputBuf.create_tag(size_points=40, weight=10, justification="left")
pos = nameInputBuf.get_end_iter()
nameInputBuf.insert_with_tags(pos, 'HI', sz)

vbox.add(nameLabel)
vbox.add(nameInput)
window.add(vbox)
window.set_size_request(300, -1)
window.show_all()
window.show()
gtk.main()


