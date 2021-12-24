from tkinter import ttk, StringVar, Entry, Frame, Label, E, W, LEFT, RIGHT, X
import source.gui.widgets as widgets
from source.classes.Empty import Empty
import json
import os

def entrando_page(parent,settings):
    # Entrance Randomizer
    self = ttk.Frame(parent)

    # Entrance Randomizer options
    self.widgets = {}

    # Entrance Randomizer option sections
    self.frames = {}
    self.frames["widgets"] = Frame(self)
    self.frames["widgets"].pack(anchor=W)

    # Load Entrance Randomizer option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    # Checkboxes go West
    # Everything else goes East
    # They also get split left & right
    with open(os.path.join("resources","app","gui","randomize","entrando","widgets.json")) as widgetDefns:
        myDict = json.load(widgetDefns)
        for framename,theseWidgets in myDict.items():
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.widgets[key] = dictWidgets[key]
                packAttrs = {"anchor":E}
                if self.widgets[key].type == "checkbox":
                    packAttrs["anchor"] = W
                self.widgets[key].pack(packAttrs)

    self.frames["entranceoverride"] = Frame(self)
    self.frames["entranceoverride"].pack(anchor=W, fill=X)

    ## entranceoverride
    # widget ID
    widget = "entranceoverride"

    # Empty object
    self.widgets[widget] = Empty()
    # pieces
    self.widgets[widget].pieces = {}

    # frame
    self.widgets[widget].pieces["frame"] = Frame(self.frames["entranceoverride"])
    # frame: label
    self.widgets[widget].pieces["frame"].label = Label(self.widgets[widget].pieces["frame"], text='Entrance Override: ')
    # storage var
    self.widgets[widget].storageVar = StringVar()
    # textbox
    self.widgets[widget].pieces["textbox"] = Entry(self.widgets[widget].pieces["frame"], textvariable=self.widgets[widget].storageVar)
    self.widgets[widget].storageVar.set(settings["entranceoverride"])

    # frame label: pack
    self.widgets[widget].pieces["frame"].label.pack(side=LEFT)
    # textbox: pack
    self.widgets[widget].pieces["textbox"].pack(side=LEFT, fill=X, expand=True)
    # frame: pack
    self.widgets[widget].pieces["frame"].pack(fill=X)

    return self
