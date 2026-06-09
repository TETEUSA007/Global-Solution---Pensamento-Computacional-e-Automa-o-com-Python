# Global-Solution---Pensamento-Computacional-Python
Global Solution - Missão Evortex

Mission Control AI — EVORTEX (versão interativa)

O que o programa é
É um sistema de terminal que simula uma central de controle de missão espacial. Em vez de usar dados fixos no código, o próprio usuário digita os valores dos sensores ciclo a ciclo, e o programa analisa tudo em tempo real e gera o relatório completo.

Como o programa funciona, do início ao fim
Ao rodar python3 mission_control_ai.py, o programa passa por quatro etapas:
Etapa 1 — Apresentação
Exibe o nome do sistema e lista os 5 sistemas monitorados da cápsula, para o usuário saber o que vai digitar antes de começar.
Etapa 2 — Configuração
Pede o nome da missão, o nome da equipe e quantos ciclos serão registrados. O programa não aceita menos de 6 ciclos — se o usuário tentar, ele avisa e pede novamente.
Etapa 3 — Entrada dos ciclos
Para cada ciclo, o programa pede os 5 valores um por um, mostrando o intervalo válido de cada um:
Temperatura interna        (-50 a 150°C): 37
Comunicação com a base     (0 a 100 %):  44
Sistema de energia         (0 a 100 %):  41
Suporte de oxigênio        (0 a 100 %):  88
Estabilidade operacional   (0 a 100 %):  52
✓  Ciclo 4 registrado.
Se digitar uma letra ou um número fora do intervalo, o programa rejeita e pede de novo — sem travar e sem perder os dados já digitados.
Etapa 4 — Análise e relatório
Assim que o último ciclo é registrado, o programa analisa tudo automaticamente e exibe dois blocos de saída: a análise ciclo a ciclo e o relatório final consolidado.

O que o programa analisa e como decide
Cada valor digitado passa por uma função específica que usa if/elif/else para classificar o parâmetro em três níveis, gerando uma pontuação:
NívelPontosExemploNORMAL0Temperatura entre 18 °C e 30 °CATENÇÃO1Temperatura entre 31 °C e 35 °CCRÍTICO2Temperatura acima de 35 °C
As 5 pontuações do ciclo são somadas. O total (0 a 10) define a classificação do ciclo inteiro — Estável, Em Atenção ou Crítico — e dispara uma recomendação automática. Se três ou mais parâmetros forem críticos ao mesmo tempo, o sistema emite protocolo de emergência.

O que aparece no relatório final
Depois de todos os ciclos, o programa calcula e exibe:

Médias de cada sensor ao longo de toda a missão
Ciclo mais crítico — qual teve a maior pontuação de risco
Tendência — compara o risco do primeiro ciclo com o do último e diz se a missão melhorou, piorou ou ficou estável
Área mais afetada — soma o risco acumulado de cada sensor em todos os ciclos e aponta qual gerou mais alertas
Classificação final e uma conclusão narrativa que muda conforme a tendência e a gravidade geral


Estruturas de programação utilizadas
O programa usa as quatro estruturas exigidas de forma direta e visível:
Funções — 13 no total, cada uma com uma responsabilidade única. ler_valor() cuida da validação, coletar_ciclos() cuida da entrada, as cinco analisar_X() cuidam de cada sensor, e assim por diante. Nenhuma função faz mais do que uma coisa.
Condicionais — cada função de análise tem sua própria cadeia de if/elif/else. A gerar_recomendacao() usa condicionais em cascata para priorizar o alerta mais grave.
Repetição — o while True em ler_valor() fica pedindo o número até ser válido. O for em coletar_ciclos() percorre os ciclos e os campos. O for principal em main() percorre a matriz inteira. O for duplo em identificar_area_mais_afetada() acumula risco por área. O while True no final de main() permite registrar várias missões seguidas sem reiniciar.
Vetores — dados_missao é a matriz construída pelo usuário em tempo de execução. todos_riscos[] acumula a pontuação de cada ciclo. pontuacoes_areas[] acumula o risco por sensor ao longo de todos os ciclos para identificar a área mais afetada.
