# -*- coding: utf-8 -*-


"""
Fleury Lucas
COLAS Delio

17/01/2020

Space-Invaders

"""

from tkinter import *
import random

#Fonction permettant les déplacements du vaisseau sur la droite grâce à la flèche de droite du clavier
def right(event):
    global GameOver, Vaisseau
    if GameOver == 1:
        return
    #Evite que le vaisseau dépasse du Canevas sur la droite
    if Canevas.coords(Vaisseau)[0]+22 >= 1000:
        Canevas.move(Vaisseau,0,0)
    #Deplace le vaisseau de +10 sur l'axe des x
    else:
        Canevas.move(Vaisseau,10,0)
        return
    
#Fonction permettant les déplacements du vaisseau sur la gauche grâce à la flèche de gauche du clavier
def left(event):
    global GameOver
    if GameOver == 1:
        return
    #Empeche le vaisseau de depasser du Canevas sur la gauche
    if Canevas.coords(Vaisseau)[0]-22 <= 0:
        Canevas.move(Vaisseau,0,0)
    #Deplace le vaisseau de -10 sur l'axe des x
    else:
        Canevas.move(Vaisseau,-10,0)
        return

#Fonction de déplacement de l'alien
def deplacementAlien():
    global dxAl,dyAl, LstAlien, speed, GameOver
    if GameOver == 1:
        return
    Max = -1
    #Regarde quel est l'alien le plus à droite
    for alien in LstAlien:
        if alien != None:
            TestMax = Canevas.coords(alien.image)
            if not TestMax:
                return
            if TestMax[0]+40 > Max:
                Max = TestMax[0]
                coordAlien1 = Canevas.coords(alien.image)
                
    Min = 1100
    #Regarde quel est l'alien le plus à gauche
    for alien in LstAlien:
        if alien != None:
            TestMin = Canevas.coords(alien.image)
            if not TestMin:
                return
            if TestMin[0] < Min:
                Min = TestMin[0]
                coordAlien2 = Canevas.coords(alien.image)
    #Fait faire un aller-retour aux aliens et les descend de 30 sur l'axe des y au bout de 1 aller-retour
    if coordAlien1[0]+20>=1000 or coordAlien2[0]-20<=0:
        dxAl= -1*dxAl
        if coordAlien2[0]-20<=0:
            for alien in LstAlien:
                if alien != None:
                    Canevas.move(alien.image,0,30)
    #Déplacement des aliens
    for alien in LstAlien:
        if alien != None:
            Canevas.move(alien.image,dxAl,dyAl)
            alien.collisionAlien()
            
    Maf.after(speed,lambda:deplacementAlien())
    return

#Attribue le tir à la touche espace du clavier
def space(event):
    global GameOver,EnableShot
    if GameOver == 1:
        return
    #Création du projectile et le fais partir du vaisseau
    if EnableShot == 1:
        EnableShot = 0
        xtir = Canevas.coords(Vaisseau)[0]-5
        ytir = Canevas.coords(Vaisseau)[1]-22
        Tir = Canevas.create_oval(xtir,ytir,xtir+10,ytir+10,fill='yellow')
        TirJoueur(xtir,ytir,Tir)
    return

#Fonction attribuant les propriétés aux projectiles (tir joueur) 
def TirJoueur(xtir,ytir,Tir):
    global LstAlien, score
    Canevas.move(Tir,0,-10)
    coordTir = Canevas.coords(Tir)
    if not coordTir:
        return
    for alien in LstAlien:
        if alien != None:
            coordAlien = Canevas.coords(alien.image)
            if not coordAlien:
                return
            #Collision entre le tir et les aliens, destruction de ces derniers si ils entrent en contact. +10 points si l'alien est tué
            if coordAlien[1]-20 < coordTir[1]+22 < coordAlien[1]+20 and coordAlien[0]+20 >= coordTir[0]+22 >= coordAlien[0]-20:
                Canevas.delete(Tir)
                Canevas.delete(alien.image)
                LstAlien[alien.id]=None
                score +=10
                Scorevar.set(score)
                vague()
                return
    #Supprime le tir si il dépasse le canevas (en y=0)          
    if coordTir[1] <= 0:
        Canevas.delete(Tir)
        return
    Maf.after(50,lambda:TirJoueur(xtir,ytir,Tir))
    return


#Création de la classe alien   
class Alien:
    def __init__(self,i,xa,ya):
        self.id=i
        self.x=xa
        self.y=ya
        self.count=0
        self.rand=random.randrange(0, 60)
        
    #Fonction qui permet d'afficcher les aliens    
    def draw(self):
        global Canevas
        self.img_alien = PhotoImage(file = "alien.gif")
        self.image= Canevas.create_image(self.x,self.y, image=self.img_alien)
        return
    
    #Défini les projectiles tirés par les aliens
    def Projectile(self):
        coord=Canevas.coords(self.image)
        if not coord:
            return
        projectile = Canevas.create_oval(coord[0],coord[1]+40,coord[0]+10,coord[1]+10+40,fill='red')
        self.TirAlien(projectile)

    #Propriétés du tir des aliens
    def TirAlien(self,projectile):
        global vie, GameOver
        Canevas.move(projectile,0,10)
        coordVaisseau=Canevas.coords(Vaisseau)
        coordProjectile=Canevas.coords(projectile)
        if not coordProjectile:
            return
        if not coordVaisseau:
            return
        #Supprime le projectile et enlève une vie au joueur si il y a collision entre le viasseau et le projectiles des aliens
        if coordVaisseau[1]+45 > coordProjectile[3] > coordVaisseau[1] and coordVaisseau[0]+45 >= coordProjectile[0] >= coordVaisseau[0]:
            Canevas.delete(projectile)
            vie-=1
            Vievar.set(vie)
            if vie == 0:
                GameOver=1
                Findujeu()
                return
            return
        
        #Supprime le projectile s'il dépasse le canevas (x=560)
        if Canevas.coords(projectile)[1] > 560:
            Canevas.delete(projectile)
            return
        #Supprime les projectiles aliens et les ilots s'il rentre en collision
        for ilot in LstIlots:
            for i in range(0,8):
                if ilot.Lst[i] != None:
                    coordsilot = Canevas.coords(ilot.Lst[i])
                    if not coordsilot:
                        Maf.after(50,lambda:self.TirAlien(projectile))
                        return
                    if coordsilot[3] > coordProjectile[3] > coordsilot[1] and coordsilot[2] >= coordProjectile[0] >= coordsilot[0]:
                        Canevas.delete(projectile)
                        Canevas.delete(ilot.Lst[i])
                        ilot.Lst[i] = None
                
        Maf.after(50,lambda:self.TirAlien(projectile))
        
    #Disparation de l'alien et du vaisseau lorsqu'il se rencontre
    def collisionAlien(self):
        global GameOver
        if GameOver == 1:
            return
        Max = 0
        #Permet de savoir l'alien le plus bas
        for alien in LstAlien:
            if alien != None:
                TestMax = Canevas.coords(alien.image)
                if not TestMax:
                    return
                if TestMax[1]+40 > Max:
                    Max = TestMax[1]+40
                    coordAlien = Canevas.coords(alien.image)
        coordVaisseau=Canevas.coords(Vaisseau)
        if not coordAlien:
            return
        if not coordVaisseau:
            return
        #Fin du jeu si les aliens arrive sur la mçeme ligne que le vaisseau
        if coordAlien[1]+40 >= coordVaisseau[1]:
            GameOver = 1
            Findujeu()
        return
#Définit la classe des ilots
class Ilot:
    def __init__(self,i,xi,yi):
        self.id = i
        self.x = xi
        self.y = yi

    def affich(self):
        #Création des rectangles qui compose les ilots
        self.image0 = Canevas.create_rectangle(self.x,self.y,self.x+40,self.y+40,fill='gray')
        self.image1 = Canevas.create_rectangle(self.x+40,self.y,self.x+80,self.y+40,fill='gray')
        self.image2 = Canevas.create_rectangle(self.x+80,self.y,self.x+120,self.y+40,fill='gray')
        
        self.image3 = Canevas.create_rectangle(self.x,self.y+40,self.x+40,self.y+80,fill='gray')
        self.image4 = Canevas.create_rectangle(self.x+40,self.y+40,self.x+80,self.y+80,fill='gray')
        self.image5 = Canevas.create_rectangle(self.x+80,self.y+40,self.x+120,self.y+80,fill='gray')

        self.image6 = Canevas.create_rectangle(self.x,self.y+80,self.x+40,self.y+120,fill='gray')
        self.image7 = Canevas.create_rectangle(self.x+80,self.y+80,self.x+120,self.y+120,fill='gray')
        
        self.Lst=[self.image0,self.image1,self.image2,self.image3,self.image4,self.image5,self.image6,self.image7]
        return
    
def compteur():
    global count, random1, LstAlien, cadence
    #Compteur aléatoire pour le tir des aliens qui ne sont pas mort
    for alien in LstAlien:
        if alien != None:
            alien.count+=1
            if alien.rand == alien.count:
                alien.count = 0
                alien.rand = random.randrange(0, 60)
                alien.Projectile()
    Maf.after(cadence,compteur)

def delayTir():
    global shot, EnableShot
    #Compteur pour avoir un delais sur le tir du vaisseau et empécher le spam
    shot+=1
    if shot == 10:
        shot=0
        EnableShot = 1
    Maf.after(100,delayTir)
    
def Findujeu():
    global Canevas, Maf
    #On supprime tout ce qu'il y a sur le canevas pour y afficher un texte : "Game Over"
    Canevas.delete("all")
    Canevas.create_text(500,281,fill='red',text='GAME OVER')
    Canevas.update()
    

def Debutdujeu():
    global LstAlien,score, vie, LstIlots, Canevas, Maf, Vaisseau, speed, cadence, nbrVague, GameOver, EnableShot, shot, dxAl, dyAl, photo, img_vaisseau, mort
    #On supprime tout ce qu'il y a sur le canevas pour bien repartir de zéro
    Canevas.delete("all")
    Canevas.update()
    
    #Affichage de l'image en background
    photo=PhotoImage(file='fond.gif')
    Canevas.create_image(502,281,image=photo)
    
    # création de l'image du vaisseau
    vaisseau_x = 500
    vaisseau_y = 533
    img_vaisseau = PhotoImage(file = "vaisseau.gif")
    Vaisseau = Canevas.create_image(vaisseau_x, vaisseau_y, image=img_vaisseau)
    
    #Affectation touche du clavier
    Canevas.bind_all("<Right>",right)
    Canevas.bind_all("<Left>",left)
    Canevas.bind_all("<space>",space)
    
    #Constante
    dxAl=10
    dyAl=0
    vie = 3
    score = 0
    mort = 0
    nbrVague=1
    cadence=200
    speed=200
    GameOver=0
    shot=0
    EnableShot=1
    
    Vievar.set(vie)
    Scorevar.set(score)
    Vaguevar.set(nbrVague)
    
    #Creation des ilots
    Ilot0 = Ilot(0,150,375)
    Ilot1 = Ilot(1,350,375)
    Ilot2 = Ilot(2,550,375)
    Ilot3 = Ilot(3,750,375)
    LstIlots = [Ilot0,Ilot1,Ilot2,Ilot3]

    for ilot in LstIlots:
        ilot.affich()
    
    #Création des aliens
    Alien0=Alien(0,100,50)
    Alien1=Alien(1,300,50)
    Alien2=Alien(2,500,50)
    Alien3=Alien(3,700,50)
    Alien4=Alien(4,100,150)
    Alien5=Alien(5,300,150)
    Alien6=Alien(6,500,150)
    Alien7=Alien(7,700,150)
    Alien8=Alien(8,100,250)
    Alien9=Alien(9,300,250)
    Alien10=Alien(10,500,250)
    Alien11=Alien(11,700,250)
    LstAlien=[Alien0,Alien1,Alien2,Alien3,Alien4,Alien5,Alien6,Alien7,Alien8,Alien9,Alien10,Alien11]
    for alien in LstAlien:
        alien.draw()
    
    
def vague():
    global mort, LstAlien, nbrVague, speed, cadence
    # Lance une autre vague d'alien quand ils ont tous été tué
    for alien in LstAlien:
        if alien != None:
            mort=0
            return
        elif alien == None:
            mort+=1
    # Il y a 12 aliens par vague donc quand "mort" = 12 on lance la vague suivante
    if mort == 12:
        nbrVague+=1
        Vaguevar.set(nbrVague)
        mort=0
        if speed > 30:
            speed-=20
        if cadence > 30:
            cadence-=20
        Alien0=Alien(0,100,50)
        Alien1=Alien(1,300,50)
        Alien2=Alien(2,500,50)
        Alien3=Alien(3,700,50)
        Alien4=Alien(4,100,150)
        Alien5=Alien(5,300,150)
        Alien6=Alien(6,500,150)
        Alien7=Alien(7,700,150)
        Alien8=Alien(8,100,250)
        Alien9=Alien(9,300,250)
        Alien10=Alien(10,500,250)
        Alien11=Alien(11,700,250)
        LstAlien=[Alien0,Alien1,Alien2,Alien3,Alien4,Alien5,Alien6,Alien7,Alien8,Alien9,Alien10,Alien11]
        for alien in LstAlien:
            alien.draw()

            
#Permet d'afficher le A propos
def Apropos():
    global Canevas, Maf
    Canevas.delete("all")
    Canevas.create_text(500,30,fill='white',text='A propos')
    Canevas.create_text(500,281,fill='white',text="Space invaders est un jeu crée en 1978 par les célèbres Lucas Fleury et Delio Colas. ")
    Canevas.create_text(500,300,fill='white',text="C'est un shoot'em up inspiré de l'unviers du roman La guerre des mondes") 
#
Maf=Tk()
Maf.title('SPACE INVADER')

#Création d'un menu
Menubar = Menu(Maf)
Menuclassic = Menu(Menubar, tearoff=0)
Menuclassic.add_command(label = 'Rejouer', command = Debutdujeu)
Menuclassic.add_command(label = 'Quitter le jeu', command=Maf.destroy)
Menuclassic.add_command(label = 'A propos', command=Apropos)
Menubar.add_cascade(label='Menu', menu= Menuclassic)

#Affichage Menu
Maf.config(menu = Menubar)


#Création bouton quitter
Boutonquit = Button(Maf,text='QUITTER',command=Maf.destroy)
Boutonquit.grid(row = 2, column = 3, padx=10)

#Création bouton play
BoutonGame = Button(Maf, text='REJOUER', command = Debutdujeu)
BoutonGame.grid(row = 3, column = 3 , padx=10)

#Affichage Score + Vie
Vietxt = Label(Maf, text='Vie :')
Vietxt.grid(row=0, column = 0)

Vievar = StringVar()
Vie = Label(Maf,textvariable=Vievar)
Vie.grid(row=1, column = 0)

Scoretxt = Label(Maf, text='Score :')
Scoretxt.grid(row=0, column = 1)

Scorevar = StringVar()
Score = Label(Maf,textvariable=Scorevar)
Score.grid(row=1, column = 1)

Vaguetxt = Label(Maf, text='Vague :')
Vaguetxt.grid(row=0, column = 2)

Vaguevar = StringVar()
NbrVague = Label(Maf,textvariable=Vaguevar)
NbrVague.grid(row=1, column = 2)

#Création du canevas
longueur = 1000
hauteur = 560
Canevas = Canvas(Maf, width=longueur , height=hauteur, bg='black',)
Canevas.grid(row=2,column=0,columnspan=3,rowspan=2)


Debutdujeu()
deplacementAlien()
compteur()
delayTir()

Maf.mainloop()



