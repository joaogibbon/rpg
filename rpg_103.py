# Versao inicial copiada da lista Python Brasil
# João Gibbon em 05/02/2020
# Refatorado por Nilo Menezes (lskbr)
#
# Requer Python 3.6 ou superior
#
import sys

from random import randint, choice, sample
from time import sleep
from typing import List
from mensagens import (INIMIGO_FORA_DA_LISTA, NUMERO_INVALIDO, TITULO_REGRA, PRESSIONE_ENTER)

from util import valida_str, valida_int, slow_print, caixa, barra, pausa

# 0001 - f-strings, quebra da validinput
# 0002 - movendo o input para dentro de valida_str e valida_int, type hints
# 0003 - slow print, impressao em caixa
# 0004 - Constantes
# 0005 - Instruções movidas para arquivo externo
# 0006 - Função pre-berserker, correção de erros de acentuação
# 0007 - Recortando as funções
# 0008 - Mais funções, barras de vida, modo sem pausa dev
# 0009 - Primeiras classes


class Configuracao:
    def __init__(self):
        # Atrasos na impressão de mensagens em segundos
        self.atraso_padrao = 3
        self.atraso_metade = 1.5
        self.atraso_medio = 2
        self.atraso_pequeno = 1

        self.pausa_curta = 0.1
        self.pausa_media = 0.25
        self.pausa_longa = 0.5
        # Valores iniciais e limites

        self.vida_inicial = 250  # Vida inicial do jogador
        self.super_cura = 250  # Pontos de vida ganhos na super cura
        self.player_sp = 100  # Valor inicial de pontos de skill
        self.inimigo_vida = 50  # Vida inicial de cada inimigo
        self.max_inimigos = 100

        self.max_sp = 100  # Número máximo de pontos skill (SP)

        # Ataque do jogador
        self.jogador_ataque_min = 15  # Dano mínimo
        self.jogador_ataque_max = 20  # Dano máximo

        # Custo de Skills
        self.sp_pierce = 10
        self.sp_custo_supercura = 50
        self.sp_custo_curar = 8
        self.sp_custo_slash = 12

        # Limites de Skills
        self.curar_min = 30
        self.curar_max = 50
        self.pierce_dano_min = 25
        self.pierce_dano_max = 40
        self.slash_dano_min = 25
        self.slash_dano_max = 35
        self.slash_inimigos_min = 5

        # Probabilidate de ataque inimigo
        self.ataque_minimo_para_dano_berzerker = 50
        self.ataque_minimo_para_dano = 25
        self.ataque_max = 100
        self.dano_minimo = 1
        self.dano_maximo = 3

        # Probabilidade de dano - mode berzerker
        self.berzerker_dano_min = 25
        self.berzerker_dano_max = 40
        self.berzerker_vida_drenada = 0.1


INSTRUCOES = None


class Jogador:
    def __init__(self, vida: int, sp: int):
        self.vida = vida
        self.sp = sp

    def consome_sp(self, pontos: int) -> bool:
        if self.sp - pontos >= 0:
            self.sp -= pontos
            return True
        return False

    def bonus_sp(self, pontos: int):
        self.sp += pontos

    def cura(self, pontos: int):
        self.vida += pontos

    def fere(self, pontos: int):
        self.vida -= pontos

    def morto(self) -> bool:
        return self.vida <= 0


class Inimigo:
    def __init__(self, numero: int, vida: int):
        self.numero = numero
        self.vida = vida

    def morto(self) -> bool:
        return self.vida <= 0

    def danifica(self, dano: int):
        self.vida -= dano


class Partida:
    def __init__(self, n_inimigos: int, configuracao: Configuracao):
        self.configuracao = configuracao
        self.n_inimigos = n_inimigos
        self.inimigos = [Inimigo(i + 1, configuracao.inimigo_vida) for i in range(self.n_inimigos)]
        self.jogador = Jogador(configuracao.vida_inicial, configuracao.player_sp)
        self.n_rodadas = 0
        self.n_rodadas_b = 0
        self.n_rodadas_antes_b = 0
        self.n_super_cura = True

    def posicao_de_inimigos(self) -> List[int]:
        return [inimigo.numero for inimigo in self.inimigos]

    def pega_inimigo_por_posicao(self, posicao: int) -> Inimigo:
        for inimigo in self.inimigos:
            if inimigo.numero == posicao:
                return inimigo
        raise Exception(f"Posição inválida {posicao}")

    def elimina_inimigo(self, inimigo: Inimigo):
        self.inimigos.remove(inimigo)

    def danifica_inimigo(self, posicao: int, dano: int):
        inimigo = self.pega_inimigo_por_posicao(posicao)
        inimigo.danifica(dano)
        if inimigo.morto():
            self.elimina_inimigo(inimigo)

    def rodada_de_super_cura(self) -> bool:
        return self.n_inimigos > 10 and self.n_rodadas != 0 and self.n_rodadas % 10 == 0


class Jogo:
    def __init__(self, configuracao: Configuracao):
        self.configuracao = configuracao

        n_inimigos = valida_int(
            list(range(1, configuracao.max_inimigos + 1)),
            f"\nEscolha o número de inimigos (max:{configuracao.max_inimigos}):\n",
            NUMERO_INVALIDO)

        self.partida = Partida(n_inimigos, configuracao)

    def atraso(self, n: int) -> float:
        conf = self.configuracao
        if n < 50:
            return conf.pausa_longa
        elif n < 100:
            return conf.pausa_media
        else:
            return conf.pausa_curta

    def danifica_inimigo(self, posicao: int, dano: int):
        conf = self.configuracao
        escolhido = self.partida.pega_inimigo_por_posicao(posicao)

        pv_inimigo_antes = escolhido.vida
        self.partida.danifica_inimigo(posicao, dano)

        slow_print(f' Atacando o inimigo {posicao}', atraso=conf.atraso_metade)
        slow_print(f"\n Você causou {dano} de dano ao inimigo {posicao} ! "
                   f"({pv_inimigo_antes} - {dano} = {escolhido.vida})", atraso=conf.atraso_metade)
        if escolhido.morto():
            caixa(f'  Você matou o inimigo {posicao}!', borda='x')
            sleep(conf.atraso_metade)

    def ataque(self) -> bool:
        conf = self.configuracao
        lista_limite = self.partida.posicao_de_inimigos()
        posicao = valida_int(lista_limite,
                             'Selecione um inimigo da lista acima: \n',
                             INIMIGO_FORA_DA_LISTA)

        dano_player = randint(conf.jogador_ataque_min,
                              conf.jogador_ataque_max)
        self.partida.danifica_inimigo(posicao, dano_player)
        return True

    def instrucao(self):
        global INSTRUCOES
        print(f'\n{TITULO_REGRA:^40}')
        # Carrega as instruções do arquivo externo, mas só na primeira vez.
        if INSTRUCOES is None:
            with open("instruções.txt", "r", encoding="utf-8") as f:
                INSTRUCOES = f.read()
        print(INSTRUCOES)
        pausa(PRESSIONE_ENTER)

    def pre_berserker(self):
        conf = self.configuracao
        slow_print(f'\n VIDA DO HERÓI = {self.partida.jogador.vida}', atraso=conf.atraso_padrao)
        slow_print(' ...', atraso=conf.atraso_pequeno)
        slow_print(' ..', atraso=conf.atraso_pequeno)
        slow_print(' .', atraso=conf.atraso_pequeno)
        slow_print('\n GOLPE FATAL !!!', atraso=conf.atraso_padrao)
        slow_print('\n NOSSO HERÓI SUCUMBE DIANTE DA HORDA INIMIGA ...', atraso=5)
        slow_print(' ...', atraso=conf.atraso_pequeno)
        slow_print(' ..', atraso=conf.atraso_pequeno)
        slow_print(' .', atraso=conf.atraso_pequeno)
        slow_print('\n É O FIM.', end='', atraso=conf.atraso_padrao * 2)
        slow_print('.', end='', atraso=conf.atraso_pequeno)
        slow_print('.', end='',  atraso=conf.atraso_pequeno)
        slow_print(' MAS ESPERE !!!!!\n', atraso=conf.atraso_pequeno)
        slow_print(' O QUE ESTÁ ACONTECENDO...?!?!?\n', atraso=conf.atraso_padrao)
        slow_print(' NÚVENS NEGRAS SURGEM E O CÉU COMEÇA A ESCURECER...\n', atraso=conf.atraso_padrao)
        slow_print(' TUDO ESTÁ TREMENDO,\n', atraso=conf.atraso_padrao)
        slow_print(' RAIOS ECLODEM DA TERRA E RASGAM O CÉU...\n', atraso=conf.atraso_padrao)
        slow_print(' TROVÕES IRROMPEM TODA A REGIÃO, ESTREMECENDO O ÍMPITO DO INIMIGO.\n', atraso=conf.atraso_padrao)
        slow_print(' DO MADA, UMA ENORME EXPLOSÃO ARREMESSA OS INIMIGOS CENTENAS DE METROS...\n',
                   atraso=conf.atraso_padrao)
        slow_print(' DO SEU EPICENTRO, ESTÁ NOSSO HERÓI...\n', atraso=conf.atraso_padrao)
        slow_print(' MAS AGORA ELE ESTÁ DIFERENTE...\n', atraso=conf.atraso_padrao)
        slow_print(' AGORA ELE ESTÁ SEDENTO POR SANGUE.\n', atraso=conf.atraso_padrao)
        slow_print(' NOSSO HERÓI SE TORNOU...UM BERSERKER !!!\n', atraso=conf.atraso_padrao)
        slow_print(' TEMIDO POR SUA IRA, O BESERKER SE TORNOU UMA LENDA...\n', atraso=conf.atraso_padrao)
        slow_print(' SEU CORPO POSSUI UMA AURA NEGRA E VERVELHA, SEUS OLHOS SÃO BRANCOS, E DELES SAEM\n'
                   ' RAIOS QUE ESTRAÇALHAM AS ROCHAS AO SEU REDOR; \n', atraso=conf.atraso_padrao)
        slow_print(' FLUTUAMDO RENTE AO SOLO, NOSSO HERÓI ENCARA OS INIMIGOS...\n', atraso=conf.atraso_padrao)
        slow_print(' E EM FRAÇÃO DE SEGUNDOS OS ALCANÇA, DESFERINDO ATAQUES DE GRANDE PODER.\n',
                   atraso=conf.atraso_padrao)
        pausa(' PRESSIONE ENTER PARA CONTINUAR...\n')
        sleep(conf.atraso_pequeno)

    def pierce_ataque(self) -> bool:
        conf = self.configuracao
        if self.partida.jogador.sp < conf.sp_pierce:
            slow_print('\n Você não possui SP suficiente (PIERCE = {conf.sp_pierce} SP)', conf.atraso_padrao)
            return False
        self.partida.jogador.consome_sp(conf.sp_pierce)
        lista_limite = self.partida.posicao_de_inimigos()
        posicao = valida_int(lista_limite, 'Selecione um inimigo da lista acima:\n',
                             INIMIGO_FORA_DA_LISTA)
        caixa(f'PIERCE ATTACK no inimigo {posicao}')
        dano_player = randint(conf.pierce_dano_min, conf.pierce_dano_max)
        self.partida.danifica_inimigo(posicao, dano_player)
        return True

    def slash_ataque(self) -> bool:
        conf = self.configuracao
        if self.partida.n_inimigos < conf.slash_inimigos_min:
            print(f'\nVocê não pode usar o SLASH com menos de {conf.slash_inimigos_min} inimígos')
            return False
        if self.partida.jogador.sp < conf.sp_custo_slash:
            slow_print(f'\nVocê não possui SP suficiente (Slash = {conf.sp_custo_slash} SP)', atraso=conf.atraso_padrao)
            return False
        self.partida.jogador.consome_sp(conf.sp_custo_slash)
        opcao = valida_int([1, 2], 'Selecionar inimigos (1) ou AUTO (2):\n')
        if opcao == 1:
            lista_limite = self.partida.posicao_de_inimigos()
            lista_inimigo_s = []
            for cont_slash in range(0, conf.slash_inimigos_min):
                inimigo_s = valida_int(
                    lista_limite, f"Selecione o {cont_slash + 1}º inimigo da lista acima: \n",
                    INIMIGO_FORA_DA_LISTA)
                lista_limite.remove(inimigo_s)
                lista_inimigo_s.append(inimigo_s)
        elif opcao == 2:
            lista_inimigo_s = sample(self.partida.posicao_de_inimigos(), 5)

        caixa(' SLASH ATTACK !!!')
        sleep(conf.atraso_metade)
        for posicao in lista_inimigo_s:
            dano_player = randint(conf.slash_dano_min, conf.slash_dano_max)
            self.danifica_inimigo(posicao, dano_player)
        slow_print('\n', atraso=conf.atraso_metade)
        return True

    def curar(self) -> bool:
        conf = self.configuracao
        if self.partida.jogador.sp < conf.sp_custo_curar:
            slow_print(f'\nVocê não possui SP suficiente (CURAR = {conf.sp_custo_curar} SP)',
                       atraso=conf.atraso_padrao)
            return False

        cura = randint(conf.curar_min, conf.curar_max)
        self.partida.jogador.cura(cura)
        self.partida.jogador.consome_sp(conf.sp_custo_curar)

        print(f'Você recuperou {cura} pontos de vida!\n')
        print(f'  VIDA: {self.partida.jogador.vida}')
        slow_print(f'  SP: {self.partida.jogador.sp}\n', atraso=conf.atraso_medio)
        return True

    def super_cura(self) -> bool:
        conf = self.configuracao
        if self.partida.jogador.sp < conf.sp_custo_supercura:
            slow_print(f'\nVocê não possui SP suficiente (SUPER CURAR = {conf.sp_custo_supercura} SP)',
                       atraso=conf.atraso_padrao)
            return False
        self.partida.jogador.cura(conf.super_cura)
        self.partida.jogador.consome_sp(conf.sp_custo_supercura)
        self.partida.n_super_cura = False
        print(f'Você recuperou {conf.super_cura} pontos de vida!\n')
        print(f'  VIDA: {self.partida.jogador.vida}')
        slow_print(f'  SP: {self.partida.jogador.sp}\n', atraso=conf.atraso_medio)
        return True

    def skills(self) -> bool:
        opcoes = ('Selecione a Skill desejada: \n '
                  '- PIERCE (1)\n '
                  '- SLASH (2)\n '
                  '- CURAR (3)\n ')
        numero_opcoes = [1, 2, 3]
        if self.partida.rodada_de_super_cura():
            opcoes += '- SUPER-CURA (4)\n'
            numero_opcoes.append(4)

        skill = valida_int(numero_opcoes, opcoes)
        print()

        if skill == 1:
            return self.pierce_ataque()
        elif skill == 2:
            return self.slash_ataque()
        elif skill == 3:
            return self.curar()
        elif skill == 4:
            return self.super_cura()
        raise Exception(f"Skill inválida {skill}")  # Pro mypy :-D

    def berserker_stats(self,
                        cont_morte_r1, cont_morte_r2, dano_b_total_r1,
                        dano_b_total_r2, total_morte,
                        dano_b_total, vida_drenada):
        print('\n\n-----.::| MODO BERSERKER DESATIVADO |::.-----\n\n\n')
        print('xxxxx.::| ESTATÍSTICA BERSERKER |::.xxxxx\n\n')
        print(f' - MORTES DA RODADA 1 = {cont_morte_r1}\n')
        print(f' - MORTES DA RODADA 2 = {cont_morte_r2}\n')
        print(f' - DANO DA RODADA 1 = {dano_b_total_r1}\n')
        print(f' - DANO DA RODADA 2 = {dano_b_total_r2}\n')
        print(f' - TOTAL DE MORTES = {total_morte}\n')
        print(f' - INIMIGOS RESTANTES = {self.partida.n_inimigos}\n')
        print(f' - TOTAL DE DANO = {dano_b_total}\n')
        print(f' - PONTOS DE VIDA DRENADOS = {vida_drenada}\n')
        print(f' - VIDA = {self.partida.jogador.vida}\n')
        print(f' - SP = {self.partida.jogador.sp}\n')
        print('x' * 39 + '\n\n')
        pausa(' .::| Precione ENTER para continuar jogando |::.\n')

    def berserker(self):
        conf = self.configuracao
        self.partida.jogador.vida = 0
        dano_b_total_r1 = 0
        dano_b_total_r2 = 0
        cont_morte_r1 = 0
        cont_morte_r2 = 0
        self.pre_berserker()

        slow_print('\n-----::..::| MODO BERSERKER ATIVADO |::..::-----\n', atraso=conf.conf.atraso_padrao)
        while self.partida.n_rodadas_b < 2:
            slow_print(f'\n=====.::| BERSERKER RODADA {self.partida.n_rodadas_b + 1} |::.=====\n',
                       atraso=conf.conf.atraso_medio)

            slow_print('.::| ATAQUES BERSERKER |::.', atraso=conf.conf.atraso_pequeno)
            for n_ataques in range(self.partida.n_inimigos):
                escolhido = choice(self.partida.inimigos)
                dano_b = randint(self.conf.berzerker_dano_min,
                                 self.conf.berzerker_dano_max)
                pv_i_antes = escolhido.vida
                escolhido.danifica(dano_b)
                if self.partida.n_rodadas_b == 0:
                    dano_b_total_r1 += dano_b
                elif self.partida.n_rodadas_b == 1:
                    dano_b_total_r2 += dano_b
                slow_print(f"\n Você causou {dano_b} de dano ao inimigo {escolhido.numero} ! "
                           f"({pv_i_antes} - {dano_b} = {escolhido.vida})", self.atraso(self.partida.n_inimigos))
                if escolhido.vida <= 0:
                    caixa(f'   Você matou o inimigo {escolhido.numero}!')
                    self.partida.danifica_inimigo(escolhido.numero)
                    sleep(self.atraso(self.partida.n_inimigos))

                    if self.partida.n_rodadas_b == 0:
                        cont_morte_r1 += 1
                    elif self.partida.n_rodadas_b == 1:
                        cont_morte_r2 += 1
                    if self.inimigos.n_inimigos == 0:
                        sleep(conf.atraso_padrao)
                        print('\n Nº Inimigos = 0\n')
                        slow_print(' .::| PARABÉNS, VOCÊ MATOU TODOS OS INIMIGOS |::.',
                                   atraso=conf.atraso_pequeno)
                        break

            if self.partida.n_inimigos == 0:
                break
            slow_print(f'\n\n.::| FIM DA RODADA {self.partida.n_rodadas_b + 1} |::.', atraso=conf.conf.atraso_padrao)
            self.partida.n_rodadas_b += 1

        dano_b_total = dano_b_total_r1 + dano_b_total_r2
        total_morte = cont_morte_r1 + cont_morte_r2
        vida_drenada = round(conf.berzerker_vida_drenada * dano_b_total)
        self.partida.jogador.cura(vida_drenada)
        self.partida.jogador.sp = 0
        self.berserker_stats(
            cont_morte_r1, cont_morte_r2, dano_b_total_r1,
            dano_b_total_r2, total_morte, dano_b_total, vida_drenada)

    def turno_do_inimigo(self):
        conf = self.configuracao
        soma_dano_inimigo = 0
        slow_print('\n----- .::| TURNO DO INIMIGO |::. -----\n', atraso=conf.atraso_metade)
        for inimigo in self.partida.inimigos:
            acerto = randint(1, conf.ataque_max)
            causa_dano = (
                self.partida.n_rodadas_b == 3 and acerto >= conf.ataque_minimo_para_dano_berzerker) or (
                self.partida.n_rodadas_b != 3 and acerto >= conf.ataque_minimo_para_dano)

            if causa_dano:
                dano_inimigo = randint(conf.dano_minimo, conf.dano_maximo)
                self.partida.jogador.fere(dano_inimigo)
                soma_dano_inimigo += dano_inimigo
                slow_print(f'Inimigo {inimigo.numero} causou {dano_inimigo} de dano !',
                           self.atraso(self.partida.n_inimigos))
            else:
                slow_print(f'Inimigo {inimigo.numero} ERROU o ataque!', self.atraso(self.partida.n_inimigos))

                if self.partida.n_rodadas_b != 3 and self.partida.jogador.sp < 0:
                    self.berserker()
            if self.partida.n_rodadas_b == 2:
                break

        if self.partida.n_rodadas_b != 2:
            slow_print(f'\nDANO TOTAL = {soma_dano_inimigo}', atraso=conf.atraso_padrao)
            print('=' * 39)

    def verifica_bonus_de_vida(self) -> None:
        conf = self.configuracao
        if self.partida.n_rodadas_b == 3:
            if self.partida.n_rodadas % 10 == 0:
                if self.partida.jogador.sp < 25:
                    self.partida.jogador.bonus_sp(72)
                    slow_print('\nHERÓI GANHOU 75 SP !!!', atraso=conf.atraso_medio)

    def imprime_inimigos(self) -> None:
        conf = self.configuracao
        slow_print('\n-----.::| LISTA DE INIMIGOS |::.-----\n', conf.atraso_metade)
        t_atraso = self.atraso(self.partida.n_inimigos)
        for inimigo in self.partida.inimigos:
            slow_print(f' - inimigo {inimigo.numero:3d} vida: {barra(inimigo.vida, dez=None)}', t_atraso)
        print(f'\nNº de inimigos = {self.partida.n_inimigos}')

    def imprime_status_do_heroi(self) -> None:
        print('\n\n===== STATUS DO HERÓI =====')
        self.verifica_bonus_de_vida()
        print(f'\n  VIDA = {barra(self.partida.jogador.vida)}')
        print(f'  SP   = {barra(self.partida.jogador.sp)}\n')

    def menu(self) -> None:
        while True:
            if self.partida.rodada_de_super_cura():
                print('-----.::| SUPER-CURA ativada |::.-----\n')
            opcao = valida_int([1, 2], 'Selecione Atacar (1), Skills (2): \n')
            sem_erro = True
            print()
            if opcao == 1:
                sem_erro = self.ataque()
            elif opcao == 2:
                sem_erro = self.skills()
            if sem_erro:
                break

    def titulo(self) -> None:
        caixa(f"{'-' * 40}  A LENDA DO BERSERKER {'-' * 40}", borda="-", margem=0)
        iniciar = valida_str('CI', '\nPressione (C)omeçar ou (I)nstruções:\n')
        if iniciar == 'I':
            self.instrucao()

    def fim_vitoria(self) -> None:
        conf = self.configuracao
        sleep(conf.atraso_metade)
        print('\n Nº Inimigos = 0\n')
        slow_print('.::| PARABÉNS, VOCÊ MATOU TODOS OS INIMIGOS |::.', atraso=conf.atraso_pequeno)

    def fim_morte(self) -> None:
        conf = self.configuracao
        print('\nVIDA = 0\n')
        slow_print(' .::| GAME OVER |::.\n', atraso=conf.atraso_padrao)

    def jogar_novamente(self) -> bool:
        restart = valida_str('JS', ' (J)ogar novamente ou (S)air:\n')
        return restart == 'J'

    def fim_de_jogo(self) -> bool:
        if self.partida.n_inimigos == 0:
            self.fim_vitoria()
            return True
        elif self.partida.jogador.vida <= 0:
            self.fim_morte()
            return True
        return False

    def incrementa_sp(self) -> None:
        if self.partida.n_rodadas_b != 2:
            self.partida.jogador.sp = min(self.partida.jogador.sp + 3, self.configuracao.max_sp)

    def turno_do_heroi(self) -> None:
        conf = self.configuracao
        slow_print('-----.::| TURNO DO HERÓI |::.-----\n', atraso=conf.atraso_metade)
        self.menu()

    @classmethod
    def loop(cls, configuracao) -> None:
        jogando = True
        while jogando:
            jogo = Jogo(configuracao)
            jogo.titulo()
            while True:
                if jogo.partida.n_rodadas_b == 2:
                    jogo.partida.n_rodadas_b = 3
                jogo.imprime_inimigos()
                jogo.imprime_status_do_heroi()
                jogo.turno_do_heroi()
                if jogo.fim_de_jogo():
                    break
                jogo.turno_do_inimigo()
                if jogo.fim_de_jogo():
                    break
                jogo.incrementa_sp()
                jogo.partida.n_rodadas += 1

            jogando = jogo.jogar_novamente()
        slow_print('\n-FIM-', atraso=jogo.configuracao.atraso_padrao)


if __name__ == "__main__":
    configuracao = Configuracao()
    if len(sys.argv) >= 2:
        if sys.argv[1] == "dev":
            configuracao.atraso_padrao = 0
            configuracao.atraso_metade = 0
            configuracao.atraso_medio = 0
            configuracao.atraso_pequeno = 0
            configuracao.pausa_curta = 0.0
            configuracao.pausa_media = 0.0
            configuracao.pausa_longa = 0.0

    Jogo.loop(configuracao)
