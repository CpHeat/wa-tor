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
interface.draw_wa_tor(grid)
#
# #button
# bouton=Button(window, text="Fermer", command=window.quit)
# bouton.pack()
# # label
# label = Label(window, text="Texte par défaut", bg="yellow")
# label.pack()
# # entrée
# value = StringVar()
# value.set("texte par défaut")
# entree = Entry(window, textvariable=value, width=30)
# entree.pack()
# # checkbutton
# bouton = Checkbutton(window, text="Nouveau?")
# bouton.pack()

#grid canvas
# canvas_width = grid_width * cell_size
# canvas_height = grid_height * cell_size
# canvas = Canvas(window, width = canvas_width, height = canvas_height, bg='#42b6f5')
# canvas.grid(row=20, column=20)
# 
# 
# for x, row in enumerate(grid):
#     for y, cell in enumerate(row):
#         if cell == "fish":
#             canvas.create_image(x*cell_size, y*cell_size, anchor=NW, image=fish_image)
#         elif cell == "shark":
#             canvas.create_image(x*cell_size, y*cell_size, anchor=NW, image=shark_image)






interface.window.mainloop()