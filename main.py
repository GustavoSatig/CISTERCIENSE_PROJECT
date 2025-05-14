import os
import cv2
from cisterciense import salvar_imagem_cisterciense
from utils import listar_imagens
from interpretador import interpretar_imagem

def menu():
    while True:
        print("\n" + "="*40)
        print("    Conversor de Algarismos Cistercienses")
        print("="*40)
        print("1 - Gerar imagem cisterciense")
        print("2 - Listar imagens salvas")
        print("3 - Interpretar imagem cisterciense")
        print("0 - Sair")
        print("="*40)
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                numero = int(input("Digite o número (0-9999): "))
                if not (0 <= numero <= 9999):
                    print("Número fora do intervalo permitido.")
                    continue
                salvar_imagem_cisterciense(numero)
                print(f"\nNúmero {numero} salvo com sucesso!")
                print("Localização dos algarismos no símbolo:")
                print(f" - Unidade: {numero % 10}")
                print(f" - Dezena: {(numero // 10) % 10}")
                print(f" - Centena: {(numero // 100) % 10}")
                print(f" - Milhar: {(numero // 1000) % 10}")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")

        elif opcao == "2":
            imagens = listar_imagens()
            print("Imagens:")
            for i, img in enumerate(imagens):
                print(f"{i+1}: {img}")
        elif opcao == "3":
            imagens = listar_imagens()
            if not imagens:
                print("Nenhuma imagem encontrada na pasta.")
                continue

            print("\nImagens disponíveis:")
            for idx, nome in enumerate(imagens):
                print(f"{idx + 1} - {nome}")

            escolha = input("Escolha o número da imagem: ")
            if not escolha.isdigit() or not (1 <= int(escolha) <= len(imagens)):
                print("Escolha inválida.")
                continue

            nome_arquivo = imagens[int(escolha) - 1]
            caminho = os.path.join("imagens_cistercienses", nome_arquivo)

            img = cv2.imread(caminho)
            if img is None:
                print(f"Erro ao carregar a imagem: {caminho}")
                continue

            numero, linhas = interpretar_imagem(img)
            print("\nImagem interpretada com sucesso!")
            print(f"Imagem: {nome_arquivo}")
            print(f"Número detectado: {numero}")
            print(f" - Unidade: {numero % 10}")
            print(f" - Dezena: {(numero // 10) % 10}")
            print(f" - Centena: {(numero // 100) % 10}")
            print(f" - Milhar: {(numero // 1000) % 10}")

        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
