import os
import cv2
from cisterciense import salvar_imagem_cisterciense
from utils import listar_imagens
from interpretador import interpretar_imagem

def menu():
    while True:
        print("\n1 - Gerar imagem cisterciense")
        print("2 - Listar imagens salvas")
        print("3 - Detectar linhas em imagem")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            numero = int(input("Digite o número (0-9999): "))
            salvar_imagem_cisterciense(numero)
        elif opcao == "2":
            imagens = listar_imagens()
            print("Imagens:")
            for i, img in enumerate(imagens):
                print(f"{i+1}: {img}")
        elif opcao == "3":
            imagens = listar_imagens()
            for i, img in enumerate(imagens):
                print(f"{i+1}: {img}")
            escolha = int(input("Escolha a imagem para leitura: "))
            caminho = os.path.join("imagens_cistercienses", imagens[escolha-1])

            img = cv2.imread(caminho)
            numero, linhas = interpretar_imagem(img)
            print(f"\nNúmero interpretado: {numero}")
            for idx, linha in enumerate(linhas):
                print(f"Linha {idx+1}: ({linha[0][0]}, {linha[0][1]}) -> ({linha[0][2]}, {linha[0][3]})")
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()

