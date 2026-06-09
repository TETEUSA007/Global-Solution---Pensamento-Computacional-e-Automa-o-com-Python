# ─── Identificação padrão (sobrescrita pelo usuário em tempo de execução) ─────
NOME_MISSAO = "EVORTEX — Alpha Test"
NOME_EQUIPE = "Equipe EVORTEX"

# ─── Áreas monitoradas ────────────────────────────────────────────────────────
areas_monitoradas = [
    "Temperatura interna",
    "Comunicação com a base",
    "Sistema de energia",
    "Suporte de oxigênio",
    "Estabilidade operacional",
]

# ─── Constantes de pontuação de risco ─────────────────────────────────────────
RISCO_NORMAL  = 0
RISCO_ATENCAO = 1
RISCO_CRITICO = 2

SEP_DUPLO   = "=" * 62
SEP_SIMPLES = "-" * 62


# =============================================================================
#  FUNÇÃO: ler_valor
#  Lê e valida um número digitado pelo usuário dentro de um intervalo.
# =============================================================================

def ler_valor(prompt, minimo, maximo):
    """
    Solicita um número ao usuário repetindo até que o valor seja válido.

    Parâmetros:
      prompt  — texto exibido ao usuário
      minimo  — menor valor aceito (inclusive)
      maximo  — maior valor aceito (inclusive)

    Retorno:
      Número float válido dentro do intervalo.
    """
    while True:
        try:
            entrada = input(prompt).strip()
            valor   = float(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f"  ✗  Valor fora do intervalo permitido ({minimo} – {maximo}). Tente novamente.")
        except ValueError:
            print("  ✗  Entrada inválida. Digite apenas números.")


# =============================================================================
#  FUNÇÃO: coletar_ciclos
#  Pede ao usuário quantos ciclos quer registrar e coleta os 5 valores de cada.
# =============================================================================

def coletar_ciclos():
    """
    Interação principal com o usuário.

    Pede o número de ciclos (mínimo 6) e, para cada ciclo, solicita os 5
    parâmetros com seus respectivos intervalos válidos:
      - Temperatura  :  -50 °C  a  150 °C
      - Comunicação  :    0 %   a  100 %
      - Bateria      :    0 %   a  100 %
      - Oxigênio     :    0 %   a  100 %
      - Estabilidade :    0 %   a  100 %

    Retorno:
      Lista de listas — a matriz dados_missao preenchida pelo usuário.
    """

    print(f"\n{SEP_DUPLO}")
    print("  CONFIGURAÇÃO DA MISSÃO")
    print(SEP_DUPLO)

    # ── Nome da missão e equipe ────────────────────────────────────────────────
    global NOME_MISSAO, NOME_EQUIPE
    nome = input("\n  Nome da missão  : ").strip()
    NOME_MISSAO = nome if nome else NOME_MISSAO
    equipe = input("  Nome da equipe  : ").strip()
    NOME_EQUIPE = equipe if equipe else NOME_EQUIPE

    # ── Quantidade de ciclos ───────────────────────────────────────────────────
    print()
    while True:
        try:
            qtd = int(input("  Quantos ciclos deseja registrar? (mínimo 6): ").strip())
            if qtd >= 6:
                break
            print("  ✗  O mínimo exigido é 6 ciclos.")
        except ValueError:
            print("  ✗  Digite um número inteiro.")

    # ── Coleta dos valores por ciclo ───────────────────────────────────────────
    dados = []

    # Definição dos campos: (rótulo, unidade, mínimo, máximo)
    campos = [
        ("Temperatura interna",    "°C",  -50,  150),
        ("Comunicação com a base", " %",    0,  100),
        ("Sistema de energia",     " %",    0,  100),
        ("Suporte de oxigênio",    " %",    0,  100),
        ("Estabilidade operacional"," %",   0,  100),
    ]

    for n in range(qtd):
        print(f"\n{SEP_SIMPLES}")
        print(f"  CICLO {n + 1} — Digite os valores dos sistemas")
        print(SEP_SIMPLES)

        ciclo = []
        for rotulo, unidade, vmin, vmax in campos:
            prompt = f"  {rotulo:<28} ({vmin} a {vmax}{unidade}): "
            valor  = ler_valor(prompt, vmin, vmax)
            ciclo.append(valor)

        dados.append(ciclo)
        print(f"  ✓  Ciclo {n + 1} registrado.")

    return dados


# =============================================================================
#  FUNÇÕES DE ANÁLISE DE SENSORES
#  Cada função recebe o valor do sensor e retorna uma tupla:
#    (classificacao: str, pontuacao: int, descricao: str)
# =============================================================================

def analisar_temperatura(valor):
    """
    Classifica a temperatura interna da cápsula.

    Regras:
      < 18 °C         → ATENÇÃO  (temperatura baixa demais)
      18 °C a 30 °C   → NORMAL
      > 30 °C a 35 °C → ATENÇÃO  (aquecimento progressivo)
      > 35 °C         → CRÍTICO  (risco de superaquecimento)
    """
    if valor > 35:
        return ("CRÍTICO",  RISCO_CRITICO, "Risco de superaquecimento detectado")
    elif valor > 30:
        return ("ATENÇÃO",  RISCO_ATENCAO, "Temperatura elevada — monitorar sensor NTC")
    elif valor >= 18:
        return ("NORMAL",   RISCO_NORMAL,  "Temperatura dentro da faixa operacional")
    else:
        return ("ATENÇÃO",  RISCO_ATENCAO, "Temperatura abaixo do mínimo operacional")


def analisar_comunicacao(valor):
    """
    Classifica a qualidade do sinal de comunicação com a base.

    Regras:
      < 30%  → CRÍTICO  (link praticamente perdido)
      30–59% → ATENÇÃO  (comunicação instável)
      ≥ 60%  → NORMAL
    """
    if valor < 30:
        return ("CRÍTICO",  RISCO_CRITICO, "Link com a base em nível crítico")
    elif valor < 60:
        return ("ATENÇÃO",  RISCO_ATENCAO, "Comunicação instável")
    else:
        return ("NORMAL",   RISCO_NORMAL,  "Comunicação estável com a base")


def analisar_bateria(valor):
    """
    Classifica o nível de energia da cápsula.

    Regras:
      < 20%  → CRÍTICO  (falha iminente de energia)
      20–49% → ATENÇÃO  (consumo acelerado)
      ≥ 50%  → NORMAL
    """
    if valor < 20:
        return ("CRÍTICO",  RISCO_CRITICO, "Bateria em nível crítico — falha iminente")
    elif valor < 50:
        return ("ATENÇÃO",  RISCO_ATENCAO, "Bateria abaixo do recomendado")
    else:
        return ("NORMAL",   RISCO_NORMAL,  "Nível de energia adequado")


def analisar_oxigenio(valor):
    """
    Classifica o nível de oxigênio disponível na câmara.

    Regras:
      < 80%  → CRÍTICO  (risco imediato à tripulação)
      80–89% → ATENÇÃO  (reservas reduzidas)
      ≥ 90%  → NORMAL
    """
    if valor < 80:
        return ("CRÍTICO",  RISCO_CRITICO, "Oxigênio em nível crítico — acionar protocolo")
    elif valor < 90:
        return ("ATENÇÃO",  RISCO_ATENCAO, "Oxigênio abaixo do ideal")
    else:
        return ("NORMAL",   RISCO_NORMAL,  "Nível de oxigênio adequado")


def analisar_estabilidade(valor):
    """
    Classifica a estabilidade operacional geral dos sistemas.

    Regras:
      < 40%  → CRÍTICO  (colapso operacional iminente)
      40–69% → ATENÇÃO  (sistemas degradados)
      ≥ 70%  → NORMAL
    """
    if valor < 40:
        return ("CRÍTICO",  RISCO_CRITICO, "Estabilidade operacional crítica")
    elif valor < 70:
        return ("ATENÇÃO",  RISCO_ATENCAO, "Estabilidade operacional reduzida")
    else:
        return ("NORMAL",   RISCO_NORMAL,  "Estabilidade operacional adequada")


# =============================================================================
#  FUNÇÃO: calcular_risco_ciclo
#  Recebe um ciclo (linha da matriz) e retorna a lista completa de análises
#  e a pontuação total de risco do ciclo.
# =============================================================================

def calcular_risco_ciclo(ciclo):
    """
    Analisa todos os 5 parâmetros de um ciclo.

    Parâmetro:
      ciclo — lista [temperatura, comunicacao, bateria, oxigenio, estabilidade]

    Retorno:
      analises   — lista de tuplas (classificacao, pontuacao, descricao)
      risco_total — soma das pontuações (0 a 10)
    """
    temperatura, comunicacao, bateria, oxigenio, estabilidade = ciclo

    analises = [
        analisar_temperatura(temperatura),
        analisar_comunicacao(comunicacao),
        analisar_bateria(bateria),
        analisar_oxigenio(oxigenio),
        analisar_estabilidade(estabilidade),
    ]

    # Estrutura de repetição: soma todas as pontuações
    risco_total = 0
    for _, pontuacao, _ in analises:
        risco_total += pontuacao

    return analises, risco_total


# =============================================================================
#  FUNÇÃO: classificar_ciclo
#  Converte a pontuação total em uma classificação textual do ciclo.
# =============================================================================

def classificar_ciclo(risco_total):
    """
    Classifica o ciclo com base na pontuação de risco.

      0–2  pontos → MISSÃO ESTÁVEL
      3–5  pontos → MISSÃO EM ATENÇÃO
      6–10 pontos → MISSÃO CRÍTICA
    """
    if risco_total <= 2:
        return "MISSÃO ESTÁVEL"
    elif risco_total <= 5:
        return "MISSÃO EM ATENÇÃO"
    else:
        return "MISSÃO CRÍTICA"


# =============================================================================
#  FUNÇÃO: gerar_recomendacao
#  Gera recomendações automáticas com base nas análises do ciclo.
# =============================================================================

def gerar_recomendacao(analises, risco_total):
    """
    Gera uma recomendação automática baseada nos alertas críticos do ciclo.

    Prioridade: temperatura → oxigênio → bateria → comunicação → estabilidade
    Se o ciclo for crítico (risco ≥ 6), emite protocolo de emergência integrado.
    Se tudo estiver normal, orienta manutenção da operação padrão.
    """
    # Classificação, pontuação e descrição de cada área
    cls_temp, _, _ = analises[0]
    cls_comm, _, _ = analises[1]
    cls_bat,  _, _ = analises[2]
    cls_ox,   _, _ = analises[3]
    cls_est,  _, _ = analises[4]

    # Protocolo de emergência para ciclo crítico com múltiplas falhas
    criticos = sum(1 for cls, _, _ in analises if cls == "CRÍTICO")
    if criticos >= 3:
        return (
            "⚠ EMERGÊNCIA: Ativar modo de segurança total. "
            "Priorizar suporte à vida, energia e comunicação."
        )

    # Recomendações individuais por área — ordem de prioridade
    if cls_ox == "CRÍTICO":
        return "🆘 Acionar protocolo de suporte à vida — oxigênio crítico."
    if cls_temp == "CRÍTICO":
        return "🌡  Verificar e ativar sistema de controle térmico."
    if cls_bat == "CRÍTICO":
        return "🔋 Ativar modo de economia de energia imediatamente."
    if cls_comm == "CRÍTICO":
        return "📡 Tentar restabelecer link com a base de controle."
    if cls_est == "CRÍTICO":
        return "⚙  Reduzir operações não essenciais — estabilidade crítica."

    # Zona de atenção
    atencoes = sum(1 for cls, _, _ in analises if cls == "ATENÇÃO")
    if atencoes >= 3:
        return (
            "⚡ Múltiplos sistemas em atenção. "
            "Monitorar de perto e preparar plano de contingência."
        )
    if atencoes >= 1:
        return "🔍 Monitorar sistemas em atenção e verificar tendência."

    # Ciclo totalmente normal
    return "✅ Manter operação normal e continuar monitoramento de rotina."


# =============================================================================
#  FUNÇÃO: analisar_tendencia
#  Compara o risco do primeiro e do último ciclo.
# =============================================================================

def analisar_tendencia(riscos):
    """
    Determina a tendência geral da missão comparando
    o risco do primeiro ciclo com o risco do último ciclo.

    Parâmetro:
      riscos — lista com a pontuação de risco de cada ciclo

    Retorno:
      Tupla (tendencia: str, descricao: str)
    """
    risco_inicial = riscos[0]
    risco_final   = riscos[-1]

    if risco_final > risco_inicial:
        tendencia  = "PIORA"
        descricao  = (
            f"A missão apresentou tendência de piora.\n"
            f"  Risco inicial (Ciclo 1): {risco_inicial} pontos  →  "
            f"Risco final (Ciclo {len(riscos)}): {risco_final} pontos"
        )
    elif risco_final < risco_inicial:
        tendencia  = "MELHORA"
        descricao  = (
            f"A missão apresentou tendência de melhora.\n"
            f"  Risco inicial (Ciclo 1): {risco_inicial} pontos  →  "
            f"Risco final (Ciclo {len(riscos)}): {risco_final} pontos"
        )
    else:
        tendencia  = "ESTÁVEL"
        descricao  = (
            f"A missão permaneceu estável em relação ao início.\n"
            f"  Risco inicial e final: {risco_inicial} pontos"
        )

    return tendencia, descricao


# =============================================================================
#  FUNÇÃO: identificar_area_mais_afetada
#  Soma o risco acumulado de cada área ao longo de todos os ciclos.
# =============================================================================

def identificar_area_mais_afetada(todos_analises):
    """
    Soma a pontuação de risco de cada área em todos os ciclos.

    Parâmetro:
      todos_analises — lista de listas de tuplas (uma lista por ciclo)

    Retorno:
      pontuacoes_areas — lista com a pontuação acumulada de cada área
      indice_maior     — índice da área mais afetada
      nome_maior       — nome da área mais afetada
    """
    # Inicializa vetor de acumuladores — um por área
    pontuacoes_areas = [0] * len(areas_monitoradas)

    # Estrutura de repetição dupla: percorre ciclos e áreas
    for analises_ciclo in todos_analises:
        for idx, (_, pontuacao, _) in enumerate(analises_ciclo):
            pontuacoes_areas[idx] += pontuacao

    # Identifica o índice da maior pontuação
    indice_maior = 0
    for i in range(1, len(pontuacoes_areas)):
        if pontuacoes_areas[i] > pontuacoes_areas[indice_maior]:
            indice_maior = i

    nome_maior = areas_monitoradas[indice_maior]
    return pontuacoes_areas, indice_maior, nome_maior


# =============================================================================
#  FUNÇÃO: exibir_ciclo
#  Formata e imprime no terminal todas as informações de um ciclo.
# =============================================================================

def exibir_ciclo(numero_ciclo, ciclo, analises, risco_total, classificacao, recomendacao):
    """
    Exibe no terminal o relatório detalhado de um ciclo de monitoramento.

    Parâmetros:
      numero_ciclo  — número sequencial do ciclo (1-based)
      ciclo         — lista com os 5 valores do ciclo
      analises      — lista de tuplas (classificacao, pontuacao, descricao)
      risco_total   — pontuação total de risco do ciclo
      classificacao — string com a classificação do ciclo
      recomendacao  — string com a recomendação automática
    """
    # Nomes das unidades para exibição
    unidades = ["°C", "%", "%", "%", "%"]
    rotulos  = [
        "Temperatura",
        "Comunicação",
        "Bateria",
        "Oxigênio",
        "Estabilidade",
    ]

    print(f"\nCICLO {numero_ciclo}")
    print(SEP_SIMPLES)

    # Estrutura de repetição: percorre todas as áreas do ciclo
    for i in range(len(ciclo)):
        valor           = ciclo[i]
        cls, pts, desc  = analises[i]
        unid            = unidades[i]
        rot             = rotulos[i]
        # Exibe sem ".0" quando o valor for inteiro
        val_fmt = int(valor) if valor == int(valor) else valor
        print(f"  {rot:<14}: {val_fmt:>4}{unid}  |  {cls:<8}  |  {desc}")

    print(f"\n  Pontuação de risco do ciclo : {risco_total}")
    print(f"  Classificação do ciclo      : {classificacao}")
    print(f"  Recomendação                : {recomendacao}")


# =============================================================================
#  FUNÇÃO: gerar_relatorio_final
#  Consolida todos os dados e exibe o relatório completo da missão.
# =============================================================================

def gerar_relatorio_final(riscos, todos_analises, todos_ciclos):
    """
    Calcula estatísticas globais e exibe o relatório final da missão.

    Parâmetros:
      riscos        — lista com pontuação de risco de cada ciclo
      todos_analises — lista de listas de tuplas (análises por ciclo)
      todos_ciclos  — a própria matriz dados_missao
    """
    n = len(todos_ciclos)

    # ── Médias por área ────────────────────────────────────────────────────────
    somas = [0.0] * 5
    for ciclo in todos_ciclos:
        for i, valor in enumerate(ciclo):
            somas[i] += valor
    medias = [s / n for s in somas]

    # ── Ciclo mais crítico ─────────────────────────────────────────────────────
    indice_critico = 0
    for i in range(1, n):
        if riscos[i] > riscos[indice_critico]:
            indice_critico = i
    ciclo_mais_critico = indice_critico + 1   # 1-based
    maior_risco        = riscos[indice_critico]

    # ── Risco médio global ─────────────────────────────────────────────────────
    risco_medio = sum(riscos) / n

    # ── Ciclos críticos ────────────────────────────────────────────────────────
    qtd_criticos = sum(1 for r in riscos if r >= 6)

    # ── Tendência ──────────────────────────────────────────────────────────────
    tendencia, descricao_tendencia = analisar_tendencia(riscos)

    # ── Área mais afetada ──────────────────────────────────────────────────────
    pontuacoes_areas, idx_maior, nome_area_afetada = identificar_area_mais_afetada(todos_analises)

    # ── Classificação final (baseada no risco médio) ───────────────────────────
    classificacao_final = classificar_ciclo(round(risco_medio))

    # ── Conclusão narrativa baseada na tendência e classificação ───────────────
    if tendencia == "MELHORA" and classificacao_final == "MISSÃO ESTÁVEL":
        conclusao = (
            "A missão foi concluída com sucesso. Os sistemas se recuperaram "
            "progressivamente e a cápsula retornou à faixa operacional segura."
        )
    elif tendencia == "MELHORA":
        conclusao = (
            "A missão apresentou recuperação progressiva após período crítico. "
            "Os sistemas responderam bem às intervenções, mas ainda requerem "
            "monitoramento contínuo."
        )
    elif tendencia == "PIORA":
        conclusao = (
            "A missão apresentou degradação progressiva dos sistemas. "
            "O ciclo final indica piora em relação ao início da operação. "
            "Recomenda-se análise completa antes de novo lançamento."
        )
    else:
        conclusao = (
            "A missão manteve nível de risco estável ao longo dos ciclos. "
            "Sistemas dentro dos parâmetros esperados para o perfil da missão."
        )

    # ── Impressão do relatório ─────────────────────────────────────────────────
    print(f"\n{SEP_DUPLO}")
    print("  RELATÓRIO FINAL DA MISSÃO")
    print(SEP_DUPLO)
    print(f"  Missão                     : {NOME_MISSAO}")
    print(f"  Equipe                     : {NOME_EQUIPE}")
    print(f"  Ciclos analisados          : {n}")
    print(SEP_SIMPLES)

    print(f"\n  MÉDIAS POR ÁREA:")
    print(f"    Temperatura interna      : {medias[0]:.2f} °C")
    print(f"    Comunicação com a base   : {medias[1]:.2f} %")
    print(f"    Sistema de energia       : {medias[2]:.2f} %")
    print(f"    Suporte de oxigênio      : {medias[3]:.2f} %")
    print(f"    Estabilidade operacional : {medias[4]:.2f} %")

    print(f"\n  RISCO:")
    print(f"    Ciclo mais crítico       : Ciclo {ciclo_mais_critico}")
    print(f"    Maior pontuação de risco : {maior_risco} pontos")
    print(f"    Risco médio da missão    : {risco_medio:.2f} pontos")
    print(f"    Ciclos críticos (≥6 pts) : {qtd_criticos}")

    print(f"\n  TENDÊNCIA DA MISSÃO:")
    for linha in descricao_tendencia.split("\n"):
        print(f"    {linha}")

    print(f"\n  PONTUAÇÃO ACUMULADA POR ÁREA:")
    for i, area in enumerate(areas_monitoradas):
        marcador = "  ◄ MAIS AFETADA" if i == idx_maior else ""
        print(f"    {area:<30}: {pontuacoes_areas[i]} pontos{marcador}")

    print(f"\n  Área mais afetada          : {nome_area_afetada}")

    print(f"\n  CLASSIFICAÇÃO FINAL        : {classificacao_final}")

    print(f"\n  CONCLUSÃO:")
    # Quebra o texto de conclusão em linhas de ~58 caracteres
    palavras  = conclusao.split()
    linha_atual = "    "
    for palavra in palavras:
        if len(linha_atual) + len(palavra) + 1 > 62:
            print(linha_atual)
            linha_atual = "    " + palavra + " "
        else:
            linha_atual += palavra + " "
    if linha_atual.strip():
        print(linha_atual)

    print(f"\n{SEP_DUPLO}\n")


# =============================================================================
#  PROGRAMA PRINCIPAL
# =============================================================================

def main():
    """
    Função principal do Mission Control AI — EVORTEX.

    Fluxo de execução:
      1. Exibe tela de boas-vindas
      2. Coleta nome da missão, equipe e quantidade de ciclos
      3. Para cada ciclo: solicita os 5 valores ao usuário
      4. Analisa, classifica, recomenda e exibe cada ciclo
      5. Gera relatório final consolidado
      6. Pergunta se o usuário quer registrar uma nova missão
    """

    # ── Tela de boas-vindas ────────────────────────────────────────────────────
    print(f"\n{SEP_DUPLO}")
    print("  MISSION CONTROL AI")
    print("  Sistema de Monitoramento — MISSÃO EVORTEX")
    print(SEP_DUPLO)
    print("  Sensores monitorados:")
    for i, area in enumerate(areas_monitoradas):
        print(f"    [{i + 1}] {area}")
    print(SEP_DUPLO)

    # ── Loop principal: permite registrar várias missões na mesma sessão ───────
    while True:

        # 1. Coleta os dados digitados pelo usuário
        dados_missao = coletar_ciclos()

        # 2. Exibe cabeçalho da análise
        print(f"\n{SEP_DUPLO}")
        print("  ANÁLISE DOS CICLOS")
        print(SEP_DUPLO)
        print(f"  Missão  : {NOME_MISSAO}")
        print(f"  Equipe  : {NOME_EQUIPE}")
        print(f"  Ciclos  : {len(dados_missao)}")
        print(SEP_DUPLO)

        # 3. Acumuladores
        todos_riscos   = []
        todos_analises = []

        # 4. Percorre cada ciclo digitado pelo usuário
        for numero in range(len(dados_missao)):
            ciclo = dados_missao[numero]

            analises, risco_total = calcular_risco_ciclo(ciclo)
            classificacao         = classificar_ciclo(risco_total)
            recomendacao          = gerar_recomendacao(analises, risco_total)

            exibir_ciclo(numero + 1, ciclo, analises,
                         risco_total, classificacao, recomendacao)

            todos_riscos.append(risco_total)
            todos_analises.append(analises)

        # 5. Relatório final
        gerar_relatorio_final(todos_riscos, todos_analises, dados_missao)

        # 6. Pergunta se quer registrar nova missão
        print()
        resposta = input("  Deseja registrar uma nova missão? (s/n): ").strip().lower()
        if resposta != "s":
            print(f"\n{SEP_DUPLO}")
            print("  Encerrando Mission Control AI — EVORTEX.")
            print("  Até a próxima missão.")
            print(f"{SEP_DUPLO}\n")
            break


# ─── Ponto de entrada ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
