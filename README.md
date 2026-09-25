**English** · [Português (Brasil)](README.pt-BR.md)

# ai-bots-list

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg) [![Data: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](DATA-LICENSE)

`ai-bots-list` is a free, open source, versioned list of known AI bots
(AI search and training) in `ai_bots.json`, plus a command line tool
(`ai_bots_check.py`) that checks a `robots.txt` against that list. For
each bot it tells you whether it is allowed, blocked or has no explicit
rule. The checker runs locally with the Python standard library only.

## Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Features

`ai_bots.json` splits the bots into two categories:

- **busca** (search): bots that feed real-time answers from AI assistants
  and AI search engines (retrieval), such as OAI-SearchBot, PerplexityBot,
  Google-Extended, Bingbot and similar. Allowing them tends to mean
  showing up in answers; blocking them tends to mean leaving the answer
  corpus.
- **treinamento** (training): bots that collect content to train models or
  build open datasets, such as GPTBot, ClaudeBot, CCBot and similar.
  Allowing them tends to mean entering the training corpus of future
  versions.

Each entry has `user_agent`, `provedor`, `produto` and `categoria`. The
list is curated by hand and updated when a provider announces or changes
a user agent. It is not automated scraping of a third-party source.

## Installation

Python 3.9 or newer, standard library only. No external dependencies.

```bash
git clone https://github.com/LucasFerrazSEO/ai-bots-list.git
cd ai-bots-list
```

## Usage

**1. Point it at your `robots.txt`** (local file):

```bash
python ai_bots_check.py robots.txt
```

**2. Or check any site's robots.txt straight from the terminal**, without
downloading the file first:

```bash
curl -s https://exemplo.com/robots.txt | python ai_bots_check.py -
```

**3. Read the result, grouped by category.** Real output (excerpt) from a
robots.txt that blocks only GPTBot. The tool prints its report in
Brazilian Portuguese.

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

**4. Test a specific path**, not just the site root:

```bash
python ai_bots_check.py robots.txt --caminho /blog/
```

**5. Filter by category** if you only want the search bots (the ones that
feed real-time answers) or only the training bots:

```bash
python ai_bots_check.py robots.txt --categoria busca
```

## FAQ

**Is ai-bots-list really free?**
Yes. The code is MIT and the data in `ai_bots.json` is CC BY 4.0. You can
reuse it freely, with attribution.

**Does the list cover every AI bot out there?**
It covers the most relevant providers in 2026. It is not exhaustive, and
new bots show up often. Contributions are welcome.

**Does blocking a search bot in robots.txt keep me out of AI answers?**
It tends to, but each provider documents separately what it does with a
block. The tool shows the rule in your robots.txt, it does not guarantee
how the AI side behaves.

**Does this work together with `ai-crawler-log-parser`?**
Yes. Both use the same `ai_bots.json` structure. Once you decide what to
block or allow here, use
[`ai-crawler-log-parser`](https://github.com/LucasFerrazSEO/ai-crawler-log-parser)
to check in your server log whether the bots actually followed the rule.

## Limitations

Simple robots.txt parsing: it handles `Disallow`/`Allow` by path prefix
and does not handle wildcards (`*`) or the end-of-string `$` the way the
full protocol does. For robots.txt files with complex rules, check the
result by hand.

## Contributing

Bug reports and suggestions are welcome through [GitHub Issues](https://github.com/LucasFerrazSEO/ai-bots-list/issues).

## Author

[Lucas Ferraz](https://lucasferraz.com) is an SEO, website development and Generative Engine Optimization specialist and the founder of [Lucas Ferraz SEO](https://lucasferrazseo.com).

## License

MIT. See [LICENSE](LICENSE). The data in `ai_bots.json` is licensed under
CC BY 4.0, see [DATA-LICENSE](DATA-LICENSE); free reuse with attribution
to [Lucas Ferraz](https://lucasferraz.com).
