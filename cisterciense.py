import cv2
import numpy as np
import os

def criar_base():
    img = np.ones((400, 400, 3), dtype=np.uint8) * 255
    cv2.line(img, (200, 20), (200, 380), (0, 0, 0), 6)
    return img

topo = (200, 20)
base = (200, 380)

def desenha_direita(img, ponto_inicio):
    end_point = (ponto_inicio[0] + 60, ponto_inicio[1])
    cv2.line(img, ponto_inicio, end_point, (0, 0, 0), 6)

def desenha_esquerda(img, ponto_inicio):
    end_point = (ponto_inicio[0] - 60, ponto_inicio[1])
    cv2.line(img, ponto_inicio, end_point, (0, 0, 0), 6)

def desenha_diagonal_direita(img, ponto_inicio):
    end_point = (ponto_inicio[0] + 60, ponto_inicio[1] + 60)
    cv2.line(img, ponto_inicio, end_point, (0, 0, 0), 6)

def desenha_diagonal_esquerda(img, ponto_inicio):
    end_point = (ponto_inicio[0] - 60, ponto_inicio[1] + 60)
    cv2.line(img, ponto_inicio, end_point, (0, 0, 0), 6)

def desenha_diagonal_direita_cima(img, ponto_inicio):
    end_point = (ponto_inicio[0] + 60, ponto_inicio[1] - 60)
    cv2.line(img, ponto_inicio, end_point, (0, 0, 0), 6)

def desenha_diagonal_esquerda_cima(img, ponto_inicio):
    end_point = (ponto_inicio[0] - 60, ponto_inicio[1] - 60)
    cv2.line(img, ponto_inicio, end_point, (0, 0, 0), 6)

def desenha_paralela_quadrante(img, deslocamento_horizontal, parte):
    centro_x = 200 + deslocamento_horizontal
    if parte == 'superior':
        start_point = (centro_x, 20)
        end_point = (centro_x, 80)
    else:
        start_point = (centro_x, 320)
        end_point = (centro_x, 380)
    cv2.line(img, start_point, end_point, (0,0,0), 6)

def desenha_cisterciense(numero):
    img = criar_base()

    milhar = (numero // 1000) % 10
    centena = (numero // 100) % 10
    dezena = (numero // 10) % 10
    unidade = numero % 10

    def desenhar_por_quadrante(valor, lado):
        if valor == 1:
            if lado == 'sup': desenha_direita(img, topo)
            elif lado == 'esq': desenha_esquerda(img, topo)
            elif lado == 'inf': desenha_direita(img, base)
            else: desenha_esquerda(img, base)
        elif valor == 2:
            ponto = (200, 80) if lado in ['sup', 'esq'] else (200, 320)
            if lado == 'sup': desenha_direita(img, ponto)
            elif lado == 'esq': desenha_esquerda(img, ponto)
            elif lado == 'inf': desenha_direita(img, ponto)
            else: desenha_esquerda(img, ponto)
        elif valor == 3:
            if lado == 'sup': desenha_diagonal_direita(img, topo)
            elif lado == 'esq': desenha_diagonal_esquerda(img, topo)
            elif lado == 'inf': desenha_diagonal_direita(img, (200, 320))
            else: desenha_diagonal_esquerda(img, (200, 320))
        elif valor == 4:
            ponto = (200, 80) if lado in ['sup', 'esq'] else (200, 320)
            if lado == 'sup': desenha_diagonal_direita_cima(img, ponto)
            elif lado == 'esq': desenha_diagonal_esquerda_cima(img, ponto)
            elif lado == 'inf': desenha_diagonal_direita(img, ponto)
            else: desenha_diagonal_esquerda(img, ponto)
        elif valor == 5:
            desenhar_por_quadrante(1, lado)
            desenhar_por_quadrante(4, lado)
        elif valor == 6:
            direcao = 'superior' if lado in ['sup', 'esq'] else 'inferior'
            deslocamento = 60 if lado in ['sup', 'inf'] else -60
            desenha_paralela_quadrante(img, deslocamento, direcao)
        elif valor == 7:
            desenhar_por_quadrante(1, lado)
            desenhar_por_quadrante(6, lado)
        elif valor == 8:
            desenhar_por_quadrante(2, lado)
            desenhar_por_quadrante(6, lado)
        elif valor == 9:
            desenhar_por_quadrante(1, lado)
            desenhar_por_quadrante(2, lado)
            desenhar_por_quadrante(6, lado)

    if unidade > 0: desenhar_por_quadrante(unidade, 'sup')
    if dezena > 0: desenhar_por_quadrante(dezena, 'esq')
    if centena > 0: desenhar_por_quadrante(centena, 'inf')
    if milhar > 0: desenhar_por_quadrante(milhar, 'dir')

    return img

def salvar_imagem_cisterciense(numero, pasta="imagens_cistercienses"):
    img = desenha_cisterciense(numero)
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    caminho = f"{pasta}/{numero}.png"
    cv2.imwrite(caminho, img)
    return caminho
