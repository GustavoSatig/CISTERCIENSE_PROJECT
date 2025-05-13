import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

def listar_imagens(pasta="imagens_cistercienses"):
    return [f for f in os.listdir(pasta) if f.endswith(('.png', '.jpg', '.jpeg'))]

def detectar_linhas(imagem):
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    bordas = cv2.Canny(cinza, 50, 150, apertureSize=3)
    return cv2.HoughLinesP(bordas, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=20)

def mostrar_imagem_com_linhas(caminho_imagem):
    img = cv2.imread(caminho_imagem)
    linhas = detectar_linhas(img.copy())

    if linhas is not None:
        for linha in linhas:
            x1, y1, x2, y2 = linha[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.axis('off')
    plt.title("Imagem com linhas detectadas")
    plt.show()

    if linhas is not None:
        print(f"{len(linhas)} linhas detectadas:")
        for idx, linha in enumerate(linhas):
            print(f"Linha {idx+1}: ({linha[0][0]}, {linha[0][1]}) -> ({linha[0][2]}, {linha[0][3]})")
    else:
        print("Nenhuma linha detectada.")

