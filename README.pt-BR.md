[English](README.md) · **Português (Brasil)**

# ai-bots-list

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg) [![Data: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](DATA-LICENSE)

`ai-bots-list` é um conjunto gratuito e de código aberto com uma lista
versionada de bots de IA conhecidos (busca com IA e treinamento), em
`ai_bots.json`, mais uma ferramenta de linha de comando
(`ai_bots_check.py`) que confere um `robots.txt` contra essa lista e diz,
bot por bot, se ele está liberado, bloqueado ou sem regra explícita. O
verificador roda localmente, só com a biblioteca padrão do Python.

## Sumário

- [Recursos](#recursos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Perguntas frequentes](#perguntas-frequentes)
- [Limitações](#limitações)
- [Como contribuir](#como-contribuir)
- [Autor](#autor)
- [Licença](#licença)

## Recursos

`ai_bots.json` separa os bots em duas categorias:

- **busca**: bots que alimentam respostas de assistentes e buscadores com
  IA em tempo real (retrieval), como OAI-SearchBot, PerplexityBot,
  Google-Extended, Bingbot e afins. Liberar tende a significar aparecer
  nas respostas; bloquear tende a significar sair do corpus de resposta.
- **treinamento**: bots que coletam conteúdo para treinar modelos ou
  compor bases abertas, como GPTBot, ClaudeBot, CCBot e afins. Liberar
  tende a significar entrar no corpus de treinamento de versões futuras.

Cada entrada leva `user_agent`, `provedor`, `produto` e `categoria`. A
lista é curadoria manual, atualizada quando um provedor anuncia ou muda um
user agent. Não é raspagem automática de terceiro.

## Instalação

Python 3.9 ou mais recente, só biblioteca padrão. Sem dependência externa.

```bash
git clone https://github.com/LucasFerrazSEO/ai-bots-list.git
cd ai-bots-list
```

## Uso

**1. Aponte para o seu `robots.txt`** (arquivo local):

```bash
python ai_bots_check.py robots.txt
```

**2. Ou confira o robots.txt de qualquer site direto do terminal**, sem
baixar o arquivo antes:

```bash
curl -s https://exemplo.com/robots.txt | python ai_bots_check.py -
```

**3. Leia o resultado, separado por categoria.** Exemplo real (trecho), de
um robots.txt que bloqueia só o GPTBot:

```
=== ai-bots-check: robots.txt (caminho testado: /) ===

-- BUSCA COM IA --
  OAI-SearchBot            ChatGPT Search                   liberado — bloco User-agent: *
  ChatGPT-User             Navegação do ChatGPT             liberado — bloco User-agent: *
  ...

-- TREINAMENTO E COLETA --
  GPTBot                   Coleta para treinamento          BLOQUEADO — bloco próprio (GPTBot)
  ClaudeBot                Coleta para treinamento          liberado — bloco User-agent: *
  anthropic-ai             Crawler geral                    liberado — bloco User-agent: *
  ...
```

**4. Teste um caminho específico**, não só a raiz do site:

```bash
python ai_bots_check.py robots.txt --caminho /blog/
```

**5. Filtre por categoria**, se só quiser ver os bots de busca (os que
alimentam resposta em tempo real) ou só os de treinamento:

```bash
python ai_bots_check.py robots.txt --categoria busca
```

## Perguntas frequentes

**ai-bots-list é realmente grátis?**
Sim. O código é MIT e os dados de `ai_bots.json` são CC BY 4.0. Pode
reusar livremente, com atribuição.

**A lista cobre todos os bots de IA que existem?**
Cobre os provedores mais relevantes em 2026. Não é exaustiva, e novos bots
aparecem com frequência. Contribuições são bem-vindas.

**Bloquear um bot de busca no robots.txt impede aparecer na resposta da
IA?**
Tende a impedir, mas cada provedor documenta separadamente o que faz com
um bloqueio. A ferramenta mostra a regra do seu robots.txt, não garante o
comportamento do lado da IA.

**Isso funciona junto com o `ai-crawler-log-parser`?**
Sim. Os dois usam a mesma estrutura de `ai_bots.json`. Depois de decidir
o que bloquear ou liberar aqui, use o
[`ai-crawler-log-parser`](https://github.com/LucasFerrazSEO/ai-crawler-log-parser)
para conferir, pelo log do servidor, se os bots realmente respeitaram a
regra.

## Limitações

Parsing simples de robots.txt: cobre `Disallow`/`Allow` por prefixo de
caminho, não trata wildcard (`*`) nem `$` de fim de string do jeito
completo do protocolo. Para robots.txt com regras complexas, confira o
resultado manualmente.

## Como contribuir

Relatos de erro e sugestões são bem-vindos pelas [Issues do GitHub](https://github.com/LucasFerrazSEO/ai-bots-list/issues).

## Autor

[Lucas Ferraz](https://lucasferraz.com) é especialista em SEO, criação de sites e Generative Engine Optimization e fundador da [Lucas Ferraz SEO](https://lucasferrazseo.com).

## Licença

MIT. Veja o arquivo [LICENSE](LICENSE). Os dados de `ai_bots.json` estão
sob CC BY 4.0, veja [DATA-LICENSE](DATA-LICENSE); reuso livre com
atribuição a [Lucas Ferraz](https://lucasferraz.com).
