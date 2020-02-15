from typing import List, Optional, Union
from mensagens import OPCAO_INVALIDA
from time import sleep


def valida_str(limite: Union[str, List[str]], msg: str) -> str:
    while True:
        valor = input(msg).strip().upper()
        if not valor.isalpha() or valor not in limite or len(valor) == 0:
            print(OPCAO_INVALIDA)
        else:
            break
    return valor


def valida_int(limite: List[int], mensagem: str, mensagem_de_erro: Optional[str] = OPCAO_INVALIDA) -> int:
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


def barra(valor: int, dez: Optional[str] = "X", um: str = "I", separador: str = " ") -> str:
    if dez is None:
        u = valor
        return f"{u * um}{separador}{valor}"
    else:
        d = valor // 10
        u = valor % 10
        return f"{dez * d}{u * um}{separador}{valor}"


def slow_print(mensagem: str, atraso: float, end="\n") -> None:
    print(mensagem, end=end)
    sleep(atraso)


def pausa(mensagem: str):
    input(mensagem)
