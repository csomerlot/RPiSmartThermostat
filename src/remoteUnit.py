#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class Notebook:


    def delete(self, widget, event=None):
        print('Closed')
        gtk.main_quit()
        return False
        
    def makeFrame(self, name):
        frame = gtk.Frame(name)
        frame.set_border_width(10)
        frame.set_size_request(300, 175) #420x272?
        frame.show()
        return frame
        
    def makeLabel(self, text):
        label = gtk.Label()
        label.set_use_markup(gtk.TRUE)
        label.set_markup('<span size="14000">%s</span>'%text)
        return label
        
    def callback(self, widget, data=None):
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("delete_event", self.delete)
        window.set_border_width(10)

        table = gtk.Table(3,6,False)
        window.add(table)

        ## Create a new notebook, place the position of the tabs
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_LEFT)
        table.attach(notebook, 0,6,0,1)
        notebook.show()
        self.show_tabs = True
        self.show_border = True

        ## Temperature
        frame = self.makeFrame('Temperature')
        ## Add a temp reading for each room
        notebook.append_page(frame, self.makeLabel('Temps'))
        
        ## Water
        frame = self.makeFrame('Household Water Usage')
        ## add a graph of water usage, well depth, irrigation usage
        notebook.append_page(frame, self.makeLabel('Water'))
        
        ## Electricity
        frame = self.makeFrame('Household Electricity Usage')
        ## Add graph of usage by appliance (NILM)
        notebook.append_page(frame, self.makeLabel('Electricity'))
        
        ## Controls
        devices = [['Furnace', "Patio", "Watering"], ["Fans", "Lights", "Door"]]
        frame = self.makeFrame('Controls')
        spacing = 5
        controlTable = gtk.Table(len(devices)+2,len(devices[0])+2,True)
        controlTable.set_row_spacings(spacing)
        controlTable.set_col_spacings(spacing)
        frame.add(controlTable)
        for r in range(len(devices)):
            for c in range(len(devices[0])):
                button = gtk.ToggleButton(devices[r][c])
                button.connect("toggled", self.callback, devices[r][c])
                controlTable.attach(button,c+1,c+2, r+1,r+2)
                button.show()
        controlTable.show()
        ## Add check boxes to set on/off status of appliances, heat, fans, irrigation, patio melter, door lock, etc.
        notebook.append_page(frame, self.makeLabel('Controls'))
        
        ## Video
        frame = self.makeFrame('Video')
        ## Add stills from various webcams?
        notebook.append_page(frame, self.makeLabel('Video'))

        table.show()
        window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    Notebook()
    main()
