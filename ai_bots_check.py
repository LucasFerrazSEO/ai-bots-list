#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai-bots-check — confere um robots.txt colado contra a lista de bots de IA
conhecidos (ai_bots.json) e diz, por bot, se ele está liberado, bloqueado ou
sem regra explícita.

O QUE FAZ
    Faz o parsing simples de blocos `User-agent:` / `Disallow:` / `Allow:`
    de um robots.txt e, para cada bot da lista, calcula se o caminho testado
    (padrão: `/`) está bloqueado, considerando também o bloco `User-agent: *`
    quando o bot não tem bloco próprio.

USO
    python ai_bots_check.py robots.txt
    python ai_bots_check.py robots.txt --caminho /blog/
    python ai_bots_check.py robots.txt --categoria busca
    curl -s https://exemplo.com/robots.txt | python ai_bots_check.py -

LIMITAÇÕES
    Parsing simples: cobre `Disallow`/`Allow` por prefixo de caminho, não
    trata wildcard (`*`) nem `$` de fim de string do jeito completo do
    protocolo. Para robots.txt com regras complexas, confira o resultado
    manualmente.

Autor: Lucas Ferraz (lucasferraz.com) — dependência zero, só biblioteca padrão.
Licença do código: MIT. Licença dos dados (ai_bots.json): CC BY 4.0.
"""
from __future__ import annotations

import argparse
import json
import os
import sys


def carrega_bots(caminho: str) -> dict:
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def parseia_robots(texto: str) -> dict[str, dict[str, list[str]]]:
    """Agrupa User-agent conforme o protocolo: linhas User-agent consecutivas
    formam um único grupo, que vale para todas até a próxima linha
    User-agent depois de pelo menos uma regra (Disallow/Allow)."""
    blocos: dict[str, dict[str, list[str]]] = {}
    agentes_atuais: list[str] = []
    grupo_com_regra = False
    for linha in texto.splitlines():
        linha = linha.split("#", 1)[0].strip()
        if not linha or ":" not in linha:
            continue
        campo, _, valor = linha.partition(":")
        campo = campo.strip().lower()
        valor = valor.strip()
        if campo == "user-agent":
            if grupo_com_regra:
                agentes_atuais = []
                grupo_com_regra = False
            agentes_atuais.append(valor)
            blocos.setdefault(valor, {"disallow": [], "allow": []})
        elif campo == "disallow" and agentes_atuais:
            for a in agentes_atuais:
                if valor:
                    blocos[a]["disallow"].append(valor)
            grupo_com_regra = True
        elif campo == "allow" and agentes_atuais:
            for a in agentes_atuais:
                if valor:
                    blocos[a]["allow"].append(valor)
            grupo_com_regra = True
    return blocos


def bloqueado(regras: dict[str, list[str]], caminho: str) -> bool | None:
    """True = bloqueado, False = liberado, None = sem regra que bata."""
    melhor_allow = max((len(p) for p in regras["allow"] if caminho.startswith(p)), default=-1)
    melhor_disallow = max((len(p) for p in regras["disallow"] if caminho.startswith(p)), default=-1)
    if melhor_allow < 0 and melhor_disallow < 0:
        return None
    return melhor_disallow > melhor_allow


def avalia(bot_ua: str, blocos: dict[str, dict[str, list[str]]], caminho: str) -> str:
    if bot_ua in blocos:
        resultado = bloqueado(blocos[bot_ua], caminho)
        origem = f"bloco próprio ({bot_ua})"
    elif "*" in blocos:
        resultado = bloqueado(blocos["*"], caminho)
        origem = "bloco User-agent: *"
    else:
        return "sem regra (nenhum bloco User-agent: * nem próprio)"
    if resultado is True:
        return f"BLOQUEADO — {origem}"
    if resultado is False:
        return f"liberado — {origem}"
    return f"sem regra que bata em {caminho} ({origem})"


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Confere um robots.txt contra a lista de bots de IA conhecidos."
    )
    ap.add_argument("robots", help="caminho do robots.txt, ou '-' para ler da entrada padrão")
    ap.add_argument("--caminho", default="/", help="caminho a testar (padrão: /)")
    ap.add_argument("--categoria", choices=["busca", "treinamento"], default="",
                     help="filtra por categoria (padrão: mostra as duas)")
    ap.add_argument("--bots-json", default=os.path.join(os.path.dirname(__file__), "ai_bots.json"),
                     help="caminho do ai_bots.json (padrão: o deste repositório)")
    args = ap.parse_args()

    dados = carrega_bots(args.bots_json)
    texto = sys.stdin.read() if args.robots == "-" else open(args.robots, encoding="utf-8").read()
    blocos = parseia_robots(texto)

    bots = dados["bots"]
    if args.categoria:
        bots = [b for b in bots if b["categoria"] == args.categoria]

    print(f"\n=== ai-bots-check: {args.robots} (caminho testado: {args.caminho}) ===\n")
    for categoria, rotulo in (("busca", "BUSCA COM IA"), ("treinamento", "TREINAMENTO E COLETA")):
        do_grupo = [b for b in bots if b["categoria"] == categoria]
        if not do_grupo:
            continue
        print(f"-- {rotulo} --")
        for bot in do_grupo:
            status = avalia(bot["user_agent"], blocos, args.caminho)
            print(f"  {bot['user_agent']:<24} {bot['produto']:<32} {status}")
        print()


if __name__ == "__main__":
    main()
