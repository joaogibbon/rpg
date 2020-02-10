# Versao inicial copiada da lista Python Brasil
# João Gibbon em 05/02/2020
# Refatorado por Nilo Menezes (lskbr)
#
# Requer Python 3.6 ou superior
#

from random import randint, choice, choices
from time import sleep
from typing import List, Optional

# 0001 - f-strings, quebra da validinput
# 0002 - movendo o input para dentro de valida_str e valida_int, type hints
# 0003 - slow print, impressao em caixa
# 0004 - Constantes
# 0005 - Instruções movidas para arquivo externo
# 0006 - Função pre-berserker, correção de erros de acentuação
# 0007 - Recortando as funções

ATRASO_PADRAO = 3
ATRASO_METADE = 1.5
ATRASO_MEDIO = 2
ATRASO_PEQUENO = 1

PAUSA_CURTA = 0.1
PAUSA_MEDIA = 0.25
PAUSA_LONGA = 0.5

# Mensagens

OPCAO_INVALIDA = 'OPÇÃO INVÁLIDA !!!\n'
INIMIGO_FORA_DA_LISTA = 'INIMIGO NÃO SE ENCONTRA NA LISTA !!!\n'
NUMERO_INVALIDO = 'NÚMERO INVÁLIDO !!!\n'
TITULO_REGRA = '.::..::| INSTRUÇÕES/REGRAS |::..::.'
PRESSIONE_ENTER = '\n\n.::| PRESSIONE ENTER PARA COMEÇAR |::.\n'

# Valores iniciais e limites

VIDA_INICIAL = 250  # Vida inicial do jogador
SUPER_CURA = 250  # Pontos de vida ganhos na super cura
PLAYER_SP = 100  # Valor inicial de pontos de skill
INIMIGO_VIDA = 50  # Vida inicial de cada inimigo
MAX_INIMIGOS = 100

MAX_SP = 100  # Número máximo de pontos skill (SP)

# Ataque do jogador
JOGADOR_ATAQUE_MIN = 15  # Dano mínimo
JOGADOR_ATAQUE_MAX = 20  # Dano máximo

# Custo de Skills
SP_PIERCE = 10
SP_CUSTO_SUPERCURA = 50
SP_CUSTO_CURAR = 8
SP_CUSTO_SLASH = 12

# Limites de Skills
CURAR_MIN = 30
CURAR_MAX = 50
PIERCE_DANO_MIN = 25
PIERCE_DANO_MAX = 40
SLASH_DANO_MIN = 25
SLASH_DANO_MAX = 35
SLASH_INIMIGOS_MIN = 5

# Probabilidate de ataque inimigo
ATAQUE_MINIMO_PARA_DANO_BERZERKER = 50
ATAQUE_MINIMO_PARA_DANO = 25
ATAQUE_MAX = 100
DANO_MINIMO = 1
DANO_MAXIMO = 3

# Probabilidade de dano - mode berzerker
BERZERKER_DANO_MIN = 25
BERZERKER_DANO_MAX = 40
BERZERKER_VIDA_DRENADA = 0.1

# Variáveis Globais
n_inimigos = 0
player_sp = 0
player_vida = 0
n_rodadas = 0
lista_inimigo: List[List[int]] = []


def valida_str(limite, msg) -> str:
    while True:
        valor = input(msg).strip().upper()
        if not valor.isalpha() or valor not in limite or len(valor) == 0:
            print(OPCAO_INVALIDA)
        else:
            break
    return valor


def valida_int(limite, mensagem: str, mensagem_de_erro: Optional[str] = OPCAO_INVALIDA) -> int:
    while True:
        valor = input(mensagem).strip()
        if not valor.isnumeric() or valor.isalpha() or len(valor) == 0 or int(valor) not in limite:
            if not valor.isnumeric() or valor.isalpha() or len(valor) == 0:
                print(OPCAO_INVALIDA)
            else:
                print(mensagem_de_erro)
        else:
            break
    return int(valor)


def caixa(mensagem: str, borda: str = '=', margem: int = 2):
    tamanho = len(mensagem) + margem
    linha = borda * tamanho
    print(f"\n{linha}")
    print(mensagem)
    print(linha)


def slow_print(mensagem: str, atraso: float = ATRASO_PADRAO, end="\n") -> None:
    print(mensagem, end=end)
    sleep(atraso)


def atraso(n: int) -> float:
    if n < 50:
        return PAUSA_LONGA
    elif n < 100:
        return PAUSA_MEDIA
    else:
        return PAUSA_CURTA


def pausa(mensagem: str):
    input(mensagem)


# Globais
INSTRUCOES = None


def inicialize():
    global player_vida, player_sp, n_rodadas_antes_b
    global n_rodadas, n_rodadas_b, n_super_cura, n_inimigos
    global lista_inimigo
    player_vida = VIDA_INICIAL
    player_sp = PLAYER_SP
    n_rodadas_antes_b = 0
    n_rodadas = 0
    n_rodadas_b = 0
    n_super_cura = True
    lista_inimigo = []
    n_inimigos = valida_int(range(1, MAX_INIMIGOS + 1),
                            "\nEscolha o número de inimigos:\n",
                            NUMERO_INVALIDO)
    for i in range(n_inimigos):
        lista_inimigo.append([i + 1, INIMIGO_VIDA])


def instrucao():
    global INSTRUCOES
    print(f'\n{TITULO_REGRA:^40}')
    # Carrega as instruções do arquivo externo, mas só na primeira vez.
    if INSTRUCOES is None:
        with open("instruções.txt", "r", encoding="utf-8") as f:
            INSTRUCOES = f.read()
    print(INSTRUCOES)
    pausa(PRESSIONE_ENTER)


def pre_berserker(vida: int):
    slow_print(f'\n VIDA DO HERÓI = {vida}', atraso=ATRASO_PADRAO)
    slow_print(' ...', atraso=ATRASO_PEQUENO)
    slow_print(' ..', atraso=ATRASO_PEQUENO)
    slow_print(' .', atraso=ATRASO_PEQUENO)
    slow_print('\n GOLPE FATAL !!!', atraso=ATRASO_PADRAO)
    slow_print('\n NOSSO HERÓI SUCUMBE DIANTE DA HORDA INIMIGA ...', atraso=5)
    slow_print(' ...', atraso=ATRASO_PEQUENO)
    slow_print(' ..', atraso=ATRASO_PEQUENO)
    slow_print(' .', atraso=ATRASO_PEQUENO)
    slow_print('\n É O FIM.', end='', atraso=ATRASO_PADRAO * 2)
    slow_print('.', end='', atraso=ATRASO_PEQUENO)
    slow_print('.', end='',  atraso=ATRASO_PEQUENO)
    slow_print(' MAS ESPERE !!!!!\n', atraso=ATRASO_PEQUENO)
    slow_print(' O QUE ESTÁ ACONTECENDO...?!?!?\n', atraso=ATRASO_PADRAO)
    slow_print(' NÚVENS NEGRAS SURGEM E O CÉU COMEÇA A ESCURECER...\n', atraso=ATRASO_PADRAO)
    slow_print(' TUDO ESTÁ TREMENDO,\n', atraso=ATRASO_PADRAO)
    slow_print(' RAIOS ECLODEM DA TERRA E RASGAM O CÉU...\n', atraso=ATRASO_PADRAO)
    slow_print(' TROVÕES IRROMPEM TODA A REGIÃO, ESTREMECENDO O ÍMPITO DO INIMIGO.\n', atraso=ATRASO_PADRAO)
    slow_print(' DO MADA, UMA ENORME EXPLOSÃO ARREMESSA OS INIMIGOS CENTENAS DE METROS...\n', atraso=ATRASO_PADRAO)
    slow_print(' DO SEU EPICENTRO, ESTÁ NOSSO HERÓI...\n', atraso=ATRASO_PADRAO)
    slow_print(' MAS AGORA ELE ESTÁ DIFERENTE...\n', atraso=ATRASO_PADRAO)
    slow_print(' AGORA ELE ESTÁ SEDENTO POR SANGUE.\n', atraso=ATRASO_PADRAO)
    slow_print(' NOSSO HERÓI SE TORNOU...UM BERSERKER !!!\n', atraso=ATRASO_PADRAO)
    slow_print(' TEMIDO POR SUA IRA, O BESERKER SE TORNOU UMA LENDA...\n', atraso=ATRASO_PADRAO)
    slow_print(' SEU CORPO POSSUI UMA AURA NEGRA E VERVELHA, SEUS OLHOS SÃO BRANCOS, E DELES SAEM\n'
               ' RAIOS QUE ESTRAÇALHAM AS ROCHAS AO SEU REDOR; \n', atraso=ATRASO_PADRAO)
    slow_print(' FLUTUAMDO RENTE AO SOLO, NOSSO HERÓI ENCARA OS INIMIGOS...\n', atraso=ATRASO_PADRAO)
    slow_print(' E EM FRAÇÃO DE SEGUNDOS OS ALCANÇA, DESFERINDO ATAQUES DE GRANDE PODER.\n', atraso=ATRASO_PADRAO)
    pausa(' PRESSIONE ENTER PARA CONTINUAR...\n')
    sleep(ATRASO_PEQUENO)


def lista_posicao_de_inimigos(lista_inimigo):
    return [inimigo[0] for inimigo in lista_inimigo]


def pega_inimigo_por_posicao(lista_inimigo: list, posicao: int) -> list:
    for inimigo in lista_inimigo:
        if inimigo[0] == posicao:
            return inimigo
    raise Exception(f"Posição inválida {posicao}")


def danifica_inimigo(lista_inimigo: list, posicao: int, dano: int):
    global n_inimigos
    escolhido = pega_inimigo_por_posicao(lista_inimigo, posicao)

    pv_inimigo_antes = escolhido[1]
    escolhido[1] -= dano
    slow_print(f' Atacando o inimigo {posicao}', atraso=ATRASO_METADE)
    slow_print(f"\n Você causou {dano} de dano ao inimigo {posicao} ! "
               f"({pv_inimigo_antes} - {dano} = {escolhido[1]})", atraso=ATRASO_METADE)
    if escolhido[1] <= 0:
        caixa(f'  Você matou o inimigo {posicao}!', borda='x')
        sleep(ATRASO_METADE)
        lista_inimigo.remove(escolhido)
        n_inimigos -= 1


def ataque(lista_inimigo: list) -> bool:
    lista_limite = lista_posicao_de_inimigos(lista_inimigo)
    inimigo = valida_int(lista_limite,
                         'Selecione um inimigo da lista acima: \n',
                         INIMIGO_FORA_DA_LISTA)

    dano_player = randint(JOGADOR_ATAQUE_MIN, JOGADOR_ATAQUE_MAX)
    danifica_inimigo(lista_inimigo, inimigo, dano_player)
    return True


def rodada_de_super_cura() -> bool:
    global n_inimigos, n_rodadas
    return n_inimigos > 10 and n_rodadas != 0 and n_rodadas % 10 == 0


def pierce_ataque(lista_inimigo) -> bool:
    global player_sp
    if player_sp < SP_PIERCE:
        slow_print('\n Você não possui SP suficiente (PIERCE = {SP_PIERCE} SP)', ATRASO_PADRAO)
        return False
    player_sp -= 10
    lista_limite = lista_posicao_de_inimigos(lista_inimigo)
    inimigo = valida_int(lista_limite, 'Selecione um inimigo da lista acima:\n',
                         INIMIGO_FORA_DA_LISTA)
    caixa(f'PIERCE ATTACK no inimigo {inimigo}')
    dano_player = randint(PIERCE_DANO_MIN, PIERCE_DANO_MAX)
    danifica_inimigo(lista_inimigo, inimigo, dano_player)
    return True


def slash_ataque(lista_inimigo) -> bool:
    global player_sp
    if n_inimigos < SLASH_INIMIGOS_MIN:
        print(f'\n Você não pode usar o SLASH com menos de {SLASH_INIMIGOS_MIN} inimígos')
        return False
    if player_sp < SP_CUSTO_SLASH:
        slow_print(f'\n Você não possui SP suficiente (Slash = {SP_CUSTO_SLASH} SP)', atraso=ATRASO_PADRAO)
        return False
    player_sp -= SP_CUSTO_SLASH
    opcao = valida_int([1, 2], ' Selecionar inimigos (1) ou AUTO (2):\n')
    if opcao == 1:
        lista_limite = lista_posicao_de_inimigos(lista_inimigo)
        lista_inimigo_s = []
        lista_inimigo_s_aux = []
        for cont_slash in range(0, SLASH_INIMIGOS_MIN):
            inimigo_s = valida_int(
                lista_limite, f" Selecione o {cont_slash + 1}º inimigo da lista acima: \n",
                INIMIGO_FORA_DA_LISTA)
            lista_limite.remove(inimigo_s)
            lista_inimigo_s_aux.append(inimigo_s)
        for i in lista_inimigo_s_aux:
            lista_inimigo_s.append(pega_inimigo_por_posicao(lista_inimigo, i))
    elif opcao == 2:
        lista_inimigo_s = choices(lista_inimigo, k=5)

    caixa(' SLASH ATTACK !!!')
    sleep(ATRASO_METADE)
    for inimigo in lista_inimigo_s:
        dano_player = randint(SLASH_DANO_MIN, SLASH_DANO_MAX)
        danifica_inimigo(lista_inimigo, inimigo[0], dano_player)
    slow_print('\n', atraso=ATRASO_METADE)
    return True


def curar():
    global player_sp, player_vida
    if player_sp < SP_CUSTO_CURAR:
        slow_print(f'\nVocê não possui SP suficiente (CURAR = {SP_CUSTO_CURAR} SP)',
                   atraso=ATRASO_PADRAO)
        return False

    cura = randint(CURAR_MIN, CURAR_MAX)
    player_vida += cura
    player_sp -= SP_CUSTO_CURAR
    print(f'Você recuperou {cura} pontos de vida!\n')
    print(f'  VIDA: {player_vida}')
    slow_print(f'  SP: {player_sp}\n', atraso=ATRASO_MEDIO)
    return True


def super_cura():
    global player_sp, player_vida, n_super_cura
    if player_sp < SP_CUSTO_SUPERCURA:
        slow_print(f'\nVocê não possui SP suficiente (SUPER CURAR = {SP_CUSTO_SUPERCURA} SP)',
                   atraso=ATRASO_PADRAO)
        return False
    player_vida += SUPER_CURA
    player_sp -= SP_CUSTO_SUPERCURA
    n_super_cura = False
    print(f'Você recuperou {SUPER_CURA} pontos de vida!\n')
    print(f'  VIDA: {player_vida}')
    slow_print(f'  SP: {player_sp}\n', atraso=ATRASO_MEDIO)
    return True


def skills(lista_inimigo: list) -> bool:
    opcoes = ('Selecione a Skill desejada: \n '
              '- PIERCE (1)\n '
              '- SLASH (2)\n '
              '- CURAR (3)\n ')
    numero_opcoes = [1, 2, 3]
    if rodada_de_super_cura():
        opcoes += '- SUPER-CURA (4)\n'
        numero_opcoes.append(4)

    skill = valida_int(numero_opcoes, opcoes)

    if skill == 1:
        return pierce_ataque(lista_inimigo)
    elif skill == 2:
        return slash_ataque(lista_inimigo)
    elif skill == 3:
        return curar()
    elif skill == 4:
        return super_cura()
    raise Exception(f"Skill inválida {skill}")  # Pro mypy :-D


def berserker_stats(cont_morte_r1, cont_morte_r2, dano_b_total_r1,
                    dano_b_total_r2, total_morte, n_inimigos,
                    dano_b_total, vida_drenada):
    print('\n\n-----.::| MODO BERSERKER DESATIVADO |::.-----\n\n\n')
    print('xxxxx.::| ESTATÍSTICA BERSERKER |::.xxxxx\n\n')
    print(f' - MORTES DA RODADA 1 = {cont_morte_r1}\n')
    print(f' - MORTES DA RODADA 2 = {cont_morte_r2}\n')
    print(f' - DANO DA RODADA 1 = {dano_b_total_r1}\n')
    print(f' - DANO DA RODADA 2 = {dano_b_total_r2}\n')
    print(f' - TOTAL DE MORTES = {total_morte}\n')
    print(f' - INIMIGOS RESTANTES = {n_inimigos}\n')
    print(f' - TOTAL DE DANO = {dano_b_total}\n')
    print(f' - PONTOS DE VIDA DRENADOS = {vida_drenada}\n')
    print(f' - VIDA = {player_vida}\n')
    print(f' - SP = {player_sp}\n')
    print('x' * 39 + '\n\n')
    pausa(' .::| Precione ENTER para continuar jogando |::.\n')


def berserker(lista_inimigo: list):
    global player_vida, n_rodadas_b, player_sp, n_inimigos
    player_vida = 0
    dano_b_total_r1 = 0
    dano_b_total_r2 = 0
    cont_morte_r1 = 0
    cont_morte_r2 = 0
    pre_berserker(0)

    slow_print('\n-----::..::| MODO BERSERKER ATIVADO |::..::-----\n', atraso=ATRASO_PADRAO)
    while n_rodadas_b < 2:
        slow_print(f'\n=====.::| BERSERKER RODADA {n_rodadas_b + 1} |::.=====\n',
                   atraso=ATRASO_MEDIO)

        slow_print('.::| ATAQUES BERSERKER |::.', atraso=ATRASO_PEQUENO)
        for n_ataques in range(len(lista_inimigo)):
            escolhido = choice(lista_inimigo)
            dano_b = randint(BERZERKER_DANO_MIN, BERZERKER_DANO_MAX)
            pv_i_antes = escolhido[1]
            escolhido[1] -= dano_b
            if n_rodadas_b == 0:
                dano_b_total_r1 += dano_b
            elif n_rodadas_b == 1:
                dano_b_total_r2 += dano_b
            slow_print(f"\n Você causou {dano_b} de dano ao inimigo {escolhido[0]} ! "
                       f"({pv_i_antes} - {dano_b} = {escolhido[1]})", atraso(n_inimigos))
            if escolhido[1] <= 0:
                caixa(f'   Você matou o inimigo {escolhido[0]}!')
                sleep(atraso(n_inimigos))
                lista_inimigo.remove(escolhido)
                n_inimigos -= 1
                if n_rodadas_b == 0:
                    cont_morte_r1 += 1
                elif n_rodadas_b == 1:
                    cont_morte_r2 += 1
                if n_inimigos == 0:
                    sleep(ATRASO_PADRAO)
                    print('\n Nº Inimigos = 0\n')
                    slow_print(' .::| PARABÉNS, VOCÊ MATOU TODOS OS INIMIGOS |::.',
                               atraso=ATRASO_PEQUENO)
                    break

        if n_inimigos == 0:
            break
        slow_print(f'\n\n.::| FIM DA RODADA {n_rodadas_b + 1} |::.', atraso=ATRASO_PADRAO)
        n_rodadas_b += 1

    dano_b_total = dano_b_total_r1 + dano_b_total_r2
    total_morte = cont_morte_r1 + cont_morte_r2
    vida_drenada = round(BERZERKER_VIDA_DRENADA * dano_b_total)
    player_vida += vida_drenada
    player_sp = 0
    berserker_stats(cont_morte_r1, cont_morte_r2, dano_b_total_r1,
                    dano_b_total_r2, total_morte, n_inimigos,
                    dano_b_total, vida_drenada)


def turno_do_inimigo(lista_inimigo: list):
    global player_vida, n_rodadas_b
    soma_dano_inimigo = 0
    slow_print('\n----- .::| TURNO DO INIMIGO |::. -----\n', atraso=ATRASO_METADE)
    print('=' * 36)
    for i in lista_inimigo:
        acerto = randint(1, ATAQUE_MAX)
        causa_dano = (
            n_rodadas_b == 3 and acerto >= ATAQUE_MINIMO_PARA_DANO_BERZERKER) or (
            n_rodadas_b != 3 and acerto >= ATAQUE_MINIMO_PARA_DANO)

        if causa_dano:
            dano_inimigo = randint(DANO_MINIMO, DANO_MAXIMO)
            player_vida -= dano_inimigo
            soma_dano_inimigo += dano_inimigo
            slow_print(f'\nInimigo {i[0]} causou {dano_inimigo} de dano !', atraso(n_inimigos))
        else:
            slow_print(f'\nInimigo {i[0]} ERROU o ataque!', atraso(n_inimigos))

            if n_rodadas_b != 3 and player_vida < 0:
                berserker(lista_inimigo)
        if n_rodadas_b == 2:
            break

    if n_rodadas_b != 2:
        slow_print(f'\n DANO TOTAL = {soma_dano_inimigo}', atraso=ATRASO_PADRAO)
        print('=' * 33)


caixa(f"{'-' * 40}  A LENDA DO BERSERKER {'-' * 40}", borda="-", margem=0)
iniciar = valida_str('CI', '\nPressione (C)omeçar ou (I)nstruções:\n')

jogando = True
if iniciar == 'I':
    instrucao()

while jogando:
    inicialize()
    while True:
        if n_rodadas_b == 2:
            n_rodadas_b = 3
        slow_print('\n-----.::| LISTA DE INIMIGOS |::.-----\n', ATRASO_METADE)
        for numero, vida in lista_inimigo:
            slow_print(f' - inimigo ({numero}) -- vida = {vida}',
                       atraso(n_inimigos))

        print(f'\n Nº de inimigos = {n_inimigos}')
        print('\n\n===== STATUS DO HERÓI =====')
        if n_rodadas_b == 3:
            if n_rodadas % 10 == 0:
                if player_sp < 25:
                    player_sp += 72
                    slow_print('\n HERÓI GANHOU 75 SP !!!', atraso=ATRASO_MEDIO)
        print(f'\n  VIDA = {player_vida}')
        print(f'  SP = {player_sp}\n')
        slow_print('-----.::| TURNO DO HERÓI |::.-----\n', atraso=ATRASO_METADE)
        while True:
            if n_rodadas > 0:
                if rodada_de_super_cura():
                    print('-----.::| SUPER-CURA ativada |::.-----\n')
            opcao = valida_int([1, 2], 'Selecione Atacar (1), Skills (2): \n')
            sem_erro = True
            if opcao == 1:
                sem_erro = ataque(lista_inimigo)
            elif opcao == 2:
                sem_erro = skills(lista_inimigo)
            if sem_erro:
                break

        turno_do_inimigo(lista_inimigo)
        if n_inimigos == 0:
            sleep(ATRASO_METADE)
            print('\n Nº Inimigos = 0\n')
            slow_print('.::| PARABÉNS, VOCÊ MATOU TODOS OS INIMIGOS |::.', atraso=ATRASO_PEQUENO)
            break
        elif player_vida <= 0:
            print('\nVIDA = 0\n')
            slow_print(' .::| GAME OVER |::.\n', atraso=ATRASO_PADRAO)
            break
        if n_rodadas_b != 2:
            player_sp += min(player_sp + 3, MAX_SP)

        n_rodadas += 1

    restart = valida_str('JS', ' (J)ogar novamente ou (S)air:\n')
    jogando = restart == 'J'

slow_print('\n -FIM-', atraso=ATRASO_PADRAO)
