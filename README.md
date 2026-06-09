# Global-Solution---Pensamento-Computacional-Python
Global Solution - Missão Evortex

Mission Control AI — EVORTEXMission Control AI — EVORTEX
O programa simula o monitoramento de uma missão espacial experimental chamada EVORTEX Alpha Test, analisando 8 ciclos de operação com 5 parâmetros cada.

O que o programa faz, passo a passo
1. Armazena os dados em uma matriz
A variável dados_missao é uma lista de listas. Cada linha é um ciclo da missão, cada coluna é um sensor:
pythondados_missao = [
    [23, 95, 91, 97, 92],  # Ciclo 1 — lançamento estável
    [41, 25, 17, 76, 31],  # Ciclo 5 — estado crítico
    ...
]
2. Analisa cada ciclo com funções específicas
Cinco funções independentes classificam cada parâmetro usando if/elif/else. Por exemplo, analisar_temperatura(41) retorna ("CRÍTICO", 2, "Risco de superaquecimento").
3. Calcula o risco do ciclo
A função calcular_risco_ciclo() chama as 5 funções de análise e usa um for para somar as pontuações. O resultado varia de 0 (tudo normal) a 10 (tudo crítico).
4. Classifica e recomenda
Com base na pontuação, classificar_ciclo() define se a missão está Estável, Em Atenção ou Crítica. A gerar_recomendacao() emite automaticamente a ação mais urgente — se três ou mais parâmetros forem críticos ao mesmo tempo, dispara o protocolo de emergência.
5. Gera o relatório final
Após percorrer todos os ciclos, gerar_relatorio_final() calcula médias, identifica o ciclo mais crítico, soma o risco acumulado de cada área com um for duplo para apontar qual foi a mais afetada, e compara o risco do Ciclo 1 com o do Ciclo 8 para determinar a tendência da missão.

Estruturas de programação utilizadas
EstruturaOnde apareceFunções13 funções, cada uma com uma responsabilidade claraCondicionaisif/elif/else dentro de cada função de análiseRepetiçãofor principal em main(), for em calcular_risco_ciclo(), for duplo em identificar_area_mais_afetada()Vetoresdados_missao (matriz), todos_riscos[], pontuacoes_areas[]
