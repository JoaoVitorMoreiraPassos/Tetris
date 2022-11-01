import os
import random
from time import sleep, time
#pip install pynput
from pynput import keyboard

        
class Tetris():
    def __init__(self, l=30, col=12):
        self.linhas = l
        self.colunas = col
        self.campo = []
        self.formas = []
        self.posx = None
        self.posy = None
        self.forma = None
        self.pode_descer = True
        self.quitar = False
        self.simbolo = "O"

    def on_press(self, key):
        if key == keyboard.Key.down:
            self.moveDown()
        if(key == keyboard.Key.left):
            self.moveLeft()
        if(key == keyboard.Key.right):
            self.moveRight()
        if key == keyboard.Key.esc:
            self.quitar = True
            
    def start(self):
        self.iniciaFormas()
        for i in range(self.linhas):
            self.campo.append([])
            for j in range(self.colunas):
                self.campo[i].append(" ")
        self.forma = self.escolheForma()
        self.posy = self.escolheColuna()
        self.posx = 0
        listener = keyboard.Listener(self.on_press)
        listener.start()
        self.mostra()
            
    def iniciaFormas(self):
        self.formas.append( {"dimensao":[3, 2]  ,  "posicao": [[0, 0] , [0, 1] , [0, 2] , [1, 1]] , "limite":{'l': [[0,-1], [1, 0]]        , 'r':[[0,3], [1,2]]        , 'd':[[1,0], [2,1], [1,2]]}} ) # mini T para baixo
        self.formas.append( {"dimensao":[2, 3]  ,  "posicao": [[0, 0] , [1, 0] , [2, 0] , [1, 1]] , "limite":{'l': [[0,-1], [1,-1], [2,-1]], 'r':[[0,1], [1,2], [2,1]] , 'd':[[3,0], [2,1]       ]}} ) # mini T para direita
        self.formas.append( {"dimensao":[3, 2]  ,  "posicao": [[0, 1] , [1, 0] , [1, 1] , [1, 2]] , "limite":{'l': [[0, 0], [1,-1]]        , 'r':[[0,2], [1,3]]        , 'd':[[2,0], [2,1], [2,2]]}} ) # mini T para cima
        self.formas.append( {"dimensao":[2, 3]  ,  "posicao": [[0, 1] , [1, 1] , [1, 0] , [2, 1]] , "limite":{'l': [[0, 0], [1,-1], [2, 0]], 'r':[[0,2], [1,2], [2,2]] , 'd':[[2,0], [3,1]       ]}} ) # mini T para esquerda

        self.formas.append( {"dimensao":[2, 3]  ,  "posicao": [[0, 1] , [1, 1] , [1, 0] , [2, 0]] , "limite":{'l': [[0, 0], [1,-1], [2,-1]], 'r':[[0,2], [1,2], [2,1]] , 'd':[[3,0], [2,1]       ]}} ) # raio em pé 1
        self.formas.append( {"dimensao":[3, 2]  ,  "posicao": [[0, 0] , [0, 1] , [1, 1] , [1, 2]] , "limite":{'l': [[0,-1], [1, 0]]        , 'r':[[0,2], [1,3]]        , 'd':[[1,0], [2,1], [2,2]]}} ) # raio deitado 1
        self.formas.append( {"dimensao":[2, 3]  ,  "posicao": [[0, 0] , [1, 0] , [1, 1] , [2, 1]] , "limite":{'l': [[0,-1], [1,-1], [2, 0]], 'r':[[0,1], [1,2], [2,2]] , 'd':[[2,0], [3,1]       ]}} ) # raio em pé 2
        self.formas.append( {"dimensao":[3, 2]  ,  "posicao": [[1, 0] , [1, 1] , [0, 1] , [0, 2]] , "limite":{'l': [[0, 0], [1,-1]]        , 'r':[[0,3], [1,2]]        , 'd':[[2,0], [2,1], [1,2]]}} ) # raio deitado 2
        
        self.formas.append( {"dimensao":[3, 2]  ,  "posicao": [[0, 0] , [0, 1] , [0, 2] , [1, 0]] , "limite":{'l': [[0,-1], [1,-1]]        , 'r':[[0,3], [1,1]]        , 'd':[[2,0], [1,2], [1,2]]}} ) # L deitado 1
        self.formas.append( {"dimensao":[2, 3]  ,  "posicao": [[0, 0] , [1, 0] , [2, 0] , [2, 1]] , "limite":{'l': [[0,-1], [1,-1], [2,-1]], 'r':[[0,1], [1,1], [2,2]] , 'd':[[3,0], [3,1]       ]}} ) # L em pé
        self.formas.append( {"dimensao":[3, 2]  ,  "posicao": [[0, 2] , [1, 0] , [1, 1] , [1, 2]] , "limite":{'l': [[0, 1], [1,-1]]        , 'r':[[0,3], [1,3]]        , 'd':[[2,0], [2,1], [2,2]]}} ) # L deitado 2
        self.formas.append( {"dimensao":[2, 3]  ,  "posicao": [[0, 0] , [0, 1] , [1, 1] , [2, 1]] , "limite":{'l': [[0,-1], [1, 0], [2, 0]], 'r':[[0,2], [1,2], [2,2]] , 'd':[[1,0], [3,1]       ]}} ) # L de cabeça para baixo
           
        self.formas.append( {"dimensao":[1, 4]  ,  "posicao": [[0, 0] , [1, 0] , [2, 0] , [3, 0]] , "limite":{'l': [[0,-1], [1,-1], [2,-1] , [3,-1]], 'r':[[0,1], [1,1], [2,1], [3,1]] ,'d':[[4,0]]}}) # I em pé
        self.formas.append( {"dimensao":[4, 1]  ,  "posicao": [[0, 0] , [0, 1] , [0, 2] , [0, 3]] , "limite":{'l': [[0,-1]]                , 'r':[[0,4]]             ,'d':[[1,0],[1,1],[1,2],[1,3]]}}) # I deitado
    
    def apagaForma(self):
        for i in self.formas[self.forma]['posicao']:
                self.campo[self.posx+i[0]][self.posy+i[1]] = " "
            
    def podeMover(self, direcao):
        forma = self.formas[self.forma]
        for i in forma['limite'][direcao]:
            if self.campo[self.posx+i[0]][self.posy+i[1]] == "O": return False, self.posx+i[0]
        return True, ""
    
    def moveSides(self, direcao):
        self.apagaForma()
        self.posy += direcao
        self.adicionaForma()
        self.pode_descer = True 
 
    def moveLeft(self):
        self.pode_descer = False
        if(self.posy == 0 or not(self.podeMover('l')[0])):
            self.pode_descer = True
            return
        self.moveSides(-1)
        
    def moveRight(self):
        self.pode_descer = False
        forma = self.formas[self.forma]
        if((self.posy == self.colunas - forma['dimensao'][0]) or not (self.podeMover('r')[0])):
            self.pode_descer = True
            return
        self.moveSides(1)
        
    def moveDown(self):           
        if(self.posx < self.linhas - self.formas[self.forma]['dimensao'][1]):
            retorno = self.podeMover('d')
            if not(retorno[0]): 
                return retorno
            self.apagaForma()
            self.posx += 1
            self.adicionaForma()
            return True, ""
        self.posx = 0
        return False, ""
    
    def apagaLinha(self, linha):
        self.campo.pop(linha)
        self.campo.insert(0,[" " for i in range(self.colunas)])
        self.posx = 0
        
    def buscaLinhaCompleta(self):
        for i in range(self.linhas):
            temp = list(map(lambda x: x == "O", self.campo[i]))
            if(all(temp)):
                self.apagaLinha(i)
            
    def adicionaForma(self):
        forma = self.formas[self.forma]
        for i in forma['posicao']:
            self.campo[self.posx+i[0]][self.posy+i[1]] = "O"
        
    def escolheForma(self): 
        return random.randint(0,13)
    
    def escolheColuna(self):
        forma = self.formas[self.forma]
        return random.randint(0, self.colunas - forma['dimensao'][0])
        
    def mostra(self):
        tempo = time() 
        while True:
            sleep(0.2)
            if self.pode_descer:
                continuar = self.moveDown()
                if not continuar[0]:
                    if (isinstance(continuar[1], int)):
                        if (self.posx == 0):
                            print("Game Over")
                            break
                    self.buscaLinhaCompleta()
                    self.forma = self.escolheForma()
                    self.posx = 0
                    self.posy = self.escolheColuna()
                    print(self.forma, self.posy)
                    self.adicionaForma()
                #Mostra o campo 
                os.system('clear')      
                a = ("-"*self.colunas).center(self.colunas*2+3, "-")
                print(a)
                print(f"|Tempo: {time() - tempo:.2f}s", f'{"|":>{len(a)-len(f"Tempo: {time()-tempo:.2f}s")-2}}')
                print(("-"*self.colunas).center(self.colunas*2+3, "-"))  
                for i in self.campo:
                    print("|", end=" ")
                    for j in i:
                        print(j, end=" ")
                    print("|")
                print(("-"*self.colunas).center(self.colunas*2+3, "-"))
                if self.quitar == True:
                    break

tetris = Tetris(35, 15)
tetris.start()    
