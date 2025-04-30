from classes.interface import Interface

grid = [
    ["fish",None,None,None,None,"shark",None,None,"fish","shark"],
    [None,None,"fish",None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None,"shark",None],
    [None,"shark",None,None,None,None,None,None,None,None],
    [None,None,None,None,"fish",None,None,None,None,None],
    [None,None,None,None,None,None,None,None,"fish",None],
    [None,"fish",None,None,"shark",None,None,None,None,None],
    [None,None,None,None,None,None,None,None,None,None],
    [None,None,"shark",None,None,"fish",None,"shark",None,None],
    ["shark",None,None,None,None,None,None,None,None,"shark"],
]

interface = Interface()
interface.create_window()
interface.create_assets()
interface.create_controls()
interface.draw_wa_tor(grid)

interface.window.mainloop()