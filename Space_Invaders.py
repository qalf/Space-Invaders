# -*- coding: utf-8 -*-


"""
Fleury Lucas
COLAS Delio

17/12/2020

Space-Invaders

"""

from tkinter import *
import random

def right(event):
    if Canevas.coords(Vaisseau)[2] == 500:
        Canevas.move(Vaisseau,0,0)
    else:
        Canevas.move(Vaisseau,10,0)
        return

def left(event):
    if Canevas.coords(Vaisseau)[0] == 0:
        Canevas.move(Vaisseau,0,0)
    else:
        Canevas.move(Vaisseau,-10,0)
        return


def Debutjeu():
    return    


def deplacementAlien():
    global dxAl,dyAl
    #Evite les collisions
    if Canevas.coords(Alien)[2]>500 or Canevas.coords(Alien)[0]<0:
        dxAl= -1*dxAl
    #Fais bouger l'alien et rappel la fonction
    Canevas.move(Alien,dxAl,dyAl)
    Maf.after(100,deplacementAlien)

    return




    



Maf=Tk()
Maf.title('SPACE INVADER')

#Création d'un menu
Menubar = Menu(Maf)
Menuclassic = Menu(Menubar, tearoff=0)
Menuclassic.add_command(label = 'Lancer le jeu', command = Debutjeu())
Menuclassic.add_command(label = 'Quitter le jeu', command=Maf.destroy)
Menubar.add_cascade(label='Menu', menu= Menuclassic)

#Affichage Menu
Maf.config(menu = Menubar)


#Création bouton quitter
Boutonquit = Button(Maf,text='QUIT',command=Maf.destroy)
Boutonquit.grid(row = 2, column = 2,sticky=N,padx=10)

#Création bouton play
BoutonGame = Button(Maf, text='PLAY', command = Debutjeu())
BoutonGame.grid(row = 3, column = 2 , sticky=N, padx=10)

#Affichage Score
Score = Label(Maf, text='Score:')
Score.grid(row=0, column = 1, sticky = W)

#Création du canevas
Canevas = Canvas(Maf, width=500 , height=500, bg='black',)
Canevas.grid(row=1,column=0,columnspan=2,rowspan=3)



#Affichage de l'image
photo=PhotoImage(file='testimage.gif')
Canevas.create_image(250,250,image=photo)

#Création Alien version simple + deplacement
Alien = Canevas.create_oval(20,20,40,40,fill='blue')
dxAl=10
dyAl=0
deplacementAlien()

#Creation Vaisseau version simple
Vaisseau = Canevas.create_rectangle(240,470,270,500,fill='red')



#Affectation touche du clavier
Canevas.bind_all("<Right>",right)
Canevas.bind_all("<Left>",left)

#Création projectile
Tir = Canevas.create_oval(250,460,260,465,fill='yellow')



Maf.mainloop()



