import cv2
import numpy as np
import matplotlib.pyplot as plt

def detectar_linhas(imagem):
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    bordas = cv2.Canny(cinza, 50, 150, apertureSize=3)
    linhas = cv2.HoughLinesP(bordas, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=20)
    return linhas

def identificar_quadrante(x, y):
    margem = 30  # margem de segurança aumentada

    if y < 200:
        if x >= 200 + margem:
            return "unidade"
        elif x <= 200 - margem:
            return "dezena"
    elif y >= 200:
        if x >= 200 + margem:
            return "centena"
        elif x <= 200 - margem:
            return "milhar"
    return None  # zona central, ignorar

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

    DIGITOS = {
        0: [],
        1: ['vertical_top'],
        2: ['horizontal_middle'],
        3: ['diagonal_esq_baixo_top'],
        4: ['diagonal_esq_cima_top'],
        5: ['diagonal_esq_cima_top', 'vertical_top'],
        6: ['horizontal_top'],
        7: ['horizontal_top', 'vertical_top'],
        8: ['horizontal_middle', 'horizontal_top'],
        9: ['horizontal_middle', 'vertical_top'],
    }

    for numero, combinacao in DIGITOS.items():
        if sorted(combinacao) == tipos:
            return numero

    # Correções específicas tolerantes (gambiarras úteis mas seguras)
    if 'diagonal_esq_cima_top' in tipos and 'vertical_bottom' in tipos:
        return 3
    if 'diagonal_dir_cima_top' in tipos and 'vertical_bottom' in tipos:
        return 3
    if 'diagonal_esq_cima_top' in tipos:
        return 4
    if 'diagonal_esq_baixo_top' in tipos:
        return 3
    if 'horizontal_top' in tipos and len(tipos) == 1:
        return 6

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
    # Desenha linhas centrais dos quadrantes (eixos X e Y)
    cv2.line(img_debug, (200, 0), (200, 400), (150, 150, 150), 1)  # vertical
    cv2.line(img_debug, (0, 200), (400, 200), (150, 150, 150), 1)  # horizontal

    for linha in linhas:
        x1, y1, x2, y2 = linha[0]
        if (180 <= x1 <= 220 and 180 <= x2 <= 220):
            print(f"Ignorando linha central: ({x1}, {y1}) → ({x2}, {y2})")
            continue

        if min(x1, x2) < 10 or max(x1, x2) > 390 or min(y1, y2) < 10 or max(y1, y2) > 390:
            continue

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

    milhar = deduzir_valor_quadrante(tipos_por_quadrante["milhar"])
    centena = deduzir_valor_quadrante(tipos_por_quadrante["centena"])
    dezena = deduzir_valor_quadrante(tipos_por_quadrante["dezena"])
    unidade = deduzir_valor_quadrante(tipos_por_quadrante["unidade"])

    print(f"\n↳ MILHAR: {milhar} | CENTENA: {centena} | DEZENA: {dezena} | UNIDADE: {unidade}")

    numero = milhar * 1000 + centena * 100 + dezena * 10 + unidade

    img_rgb = cv2.cvtColor(img_debug, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.title(f"Número interpretado: {numero}")
    plt.axis('off')
    plt.savefig(f"saida_debug_{numero}.png")  # salva a imagem
    print(f"Imagem de debug salva como saida_debug_{numero}.png")

    return numero, linhas
