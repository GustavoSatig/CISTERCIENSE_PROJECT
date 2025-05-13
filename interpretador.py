import cv2
import numpy as np
import matplotlib.pyplot as plt

def detectar_linhas(imagem):
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    bordas = cv2.Canny(cinza, 50, 150, apertureSize=3)
    linhas = cv2.HoughLinesP(bordas, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=20)
    return linhas

def identificar_quadrante(x, y):
    if y < 200 and x > 200:
        return "unidade"
    elif y < 200 and x < 200:
        return "dezena"
    elif y > 200 and x > 200:
        return "centena"
    elif y > 200 and x < 200:
        return "milhar"
    return None

def classificar_posicao(x1, y1, x2, y2, quadrante):
    xm, ym = (x1 + x2) // 2, (y1 + y2) // 2

    if quadrante in ['unidade', 'dezena']:  # superior
        if ym < 60:
            return 'top'
        elif ym < 120:
            return 'middle'
        else:
            return 'bottom'
    elif quadrante in ['centena', 'milhar']:  # inferior
        if ym > 340:
            return 'bottom'
        elif ym > 280:
            return 'middle'
        else:
            return 'top'
    return 'unknown'

def identificar_tipo_linha(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    angulo = np.degrees(np.arctan2(dy, dx))

    if abs(dx) < 15:
        return "vertical"
    elif abs(dy) < 15:
        return "horizontal"
    elif -135 < angulo < -45:
        return "diagonal_esq_cima"
    elif -45 <= angulo <= 0:
        return "diagonal_dir_cima"
    elif 0 < angulo < 45:
        return "diagonal_dir_baixo"
    elif 45 <= angulo < 135:
        return "diagonal_esq_baixo"
    return "desconhecida"

def deduzir_valor_quadrante(tipos):
    tipos = sorted(set(tipos))

    if 'vertical_top' in tipos and 'horizontal_middle' in tipos:
        return 9
    if tipos == ['horizontal_middle']:
        return 2
    if tipos == ['vertical_top']:
        return 1
    if 'diagonal_dir_baixo_top' in tipos or 'diagonal_esq_baixo_top' in tipos:
        return 3
    if 'diagonal_dir_cima_top' in tipos or 'diagonal_esq_cima_top' in tipos:
        return 4
    if ('diagonal_dir_cima_top' in tipos or 'diagonal_esq_cima_top' in tipos) and 'vertical_top' in tipos:
        return 5
    if tipos.count('horizontal_top') >= 1 and len(tipos) == 1:
        return 6
    if 'horizontal_top' in tipos and 'vertical_top' in tipos:
        return 7
    if 'horizontal_top' in tipos and 'horizontal_middle' in tipos:
        return 8
    if 'diagonal_dir_baixo_top' in tipos:
        return 4
    if {'vertical_bottom', 'diagonal_dir_cima_top'}.issubset(tipos):
        return 3

    return 0

def filtrar_linhas_semelhantes(linhas, threshold=10):
    unicas = []
    for nova in linhas:
        x1, y1, x2, y2 = nova[0]
        repetida = False
        for antiga in unicas:
            xa1, ya1, xa2, ya2 = antiga[0]
            dist = np.linalg.norm([x1 - xa1, y1 - ya1]) + np.linalg.norm([x2 - xa2, y2 - ya2])
            if dist < threshold * 2:
                repetida = True
                break
        if not repetida:
            unicas.append(nova)
    return unicas

def interpretar_imagem(img):
    linhas = detectar_linhas(img)
    linhas = filtrar_linhas_semelhantes(linhas)
    if linhas is None:
        return 0, []

    tipos_por_quadrante = {
        "milhar": [],
        "centena": [],
        "dezena": [],
        "unidade": [],
    }

    img_debug = img.copy()

    for linha in linhas:
        x1, y1, x2, y2 = linha[0]
        quad = identificar_quadrante((x1 + x2) // 2, (y1 + y2) // 2)
        if not quad:
            continue
        tipo = identificar_tipo_linha(x1, y1, x2, y2)
        zona = classificar_posicao(x1, y1, x2, y2, quad)
        label = f"{tipo}_{zona}"
        print(f"[{quad.upper()}] → tipo: {tipo}, zona: {zona}, label: {label}")
        tipos_por_quadrante[quad].append(label)

        cor = {
            "milhar": (0, 0, 255),     # vermelho
            "centena": (0, 255, 0),    # verde
            "dezena": (255, 0, 0),     # azul
            "unidade": (0, 255, 255),  # amarelo
        }.get(quad, (128, 128, 128))
        cv2.line(img_debug, (x1, y1), (x2, y2), cor, 2)
        cv2.putText(img_debug, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, cor, 1)

    print("\n--- Detecção por quadrante ---")
    for quad, tipos in tipos_por_quadrante.items():
        print(f"{quad.upper()}: {tipos}")

    numero = (
        deduzir_valor_quadrante(tipos_por_quadrante["milhar"]) * 1000 +
        deduzir_valor_quadrante(tipos_por_quadrante["centena"]) * 100 +
        deduzir_valor_quadrante(tipos_por_quadrante["dezena"]) * 10 +
        deduzir_valor_quadrante(tipos_por_quadrante["unidade"])
    )

    # img_rgb = cv2.cvtColor(img_debug, cv2.COLOR_BGR2RGB)
    # plt.imshow(img_rgb)
    # plt.title(f"Número interpretado: {numero}")
    # plt.axis('off')
    # plt.show()

    img_rgb = cv2.cvtColor(img_debug, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.title(f"Número interpretado: {numero}")
    plt.axis('off')
    plt.savefig(f"saida_debug_{numero}.png")  # salva a imagem
    print(f"Imagem de debug salva como saida_debug_{numero}.png")

    return numero, linhas
