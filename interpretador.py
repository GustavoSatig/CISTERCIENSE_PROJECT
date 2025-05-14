import cv2
import numpy as np
import matplotlib.pyplot as plt

def detectar_linhas(imagem):
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    bordas = cv2.Canny(cinza, 50, 150, apertureSize=3)

    cv2.imshow("Bordas", bordas)
    cv2.waitKey(0)

    linhas = cv2.HoughLinesP(bordas, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=20)

    if linhas is not None:
        img_linhas = imagem.copy()
        for linha in linhas:
            x1, y1, x2, y2 = linha[0]
            cv2.line(img_linhas, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow("Linhas Detectadas", img_linhas)
        cv2.waitKey(0)

    return linhas

def identificar_quadrante(x, y):
    margem = 30

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
    return None

def classificar_posicao(x1, y1, x2, y2, quadrante, altura):
    xm, ym = (x1 + x2) // 2, (y1 + y2) // 2

    if quadrante in ['unidade', 'dezena']:
        if altura < 60:
            return 'top'
        elif altura < 120:
            return 'middle'
        else:
            return 'bottom'
    elif quadrante in ['centena', 'milhar']:
        if altura > 340:
            return 'bottom'
        elif altura > 280:
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

def converter_para_numero(tipos_por_quadrante):
    milhar = deduzir_valor_quadrante(tipos_por_quadrante["milhar"])
    centena = deduzir_valor_quadrante(tipos_por_quadrante["centena"])
    dezena = deduzir_valor_quadrante(tipos_por_quadrante["dezena"])
    unidade = deduzir_valor_quadrante(tipos_por_quadrante["unidade"])

    numero = milhar * 1000 + centena * 100 + dezena * 10 + unidade

    return numero

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
    cv2.line(img_debug, (200, 0), (200, 400), (150, 150, 150), 1)
    cv2.line(img_debug, (0, 200), (400, 200), (150, 150, 150), 1)

    for linha in linhas:
        x1, y1, x2, y2 = linha[0]
        if (180 <= x1 <= 220 and 180 <= x2 <= 220):
            continue

        if min(x1, x2) < 10 or max(x1, x2) > 390 or min(y1, y2) < 10 or max(y1, y2) > 390:
            continue

        quad = identificar_quadrante((x1 + x2) // 2, (y1 + y2) // 2)
        if not quad:
            continue
        tipo = identificar_tipo_linha(x1, y1, x2, y2)

        altura = (y1 + y2) // 2

        zona = classificar_posicao(x1, y1, x2, y2, quad, altura)
        label = f"{tipo}_{zona}"
        tipos_por_quadrante[quad].append(label)

        cor = {
            "milhar": (0, 0, 255),   
            "centena": (0, 255, 0),  
            "dezena": (255, 0, 0),   
            "unidade": (0, 255, 255),
        }.get(quad, (128, 128, 128))
        cv2.line(img_debug, (x1, y1), (x2, y2), cor, 2)
        cv2.putText(img_debug, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, cor, 1)

    milhar = deduzir_valor_quadrante(tipos_por_quadrante["milhar"])
    centena = deduzir_valor_quadrante(tipos_por_quadrante["centena"])
    dezena = deduzir_valor_quadrante(tipos_por_quadrante["dezena"])
    unidade = deduzir_valor_quadrante(tipos_por_quadrante["unidade"])

    numero = milhar * 1000 + centena * 100 + dezena * 10 + unidade

    img_rgb = cv2.cvtColor(img_debug, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.title(f"Número interpretado: {numero}")
    plt.axis('off')
    plt.savefig(f"debug_img/saida_{numero}.png")

    return numero, linhas
