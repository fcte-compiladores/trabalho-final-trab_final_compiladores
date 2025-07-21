## Integrantes

|Matrícula | Aluno | Turma |
| -- | -- | -- |
| 22/2029243  | Victor Hugo dos Santos Bernardes | 16h |
| 20/2015868 | Alexandre Lema Xavier Júnior | 18h |

## Sobre o Projeto

Este projeto implementa um Analisador Léxico (Lexer) e um Analisador Sintático (Parser) para a linguagem PDDL (Planning Domain Definition Language). O objetivo é validar a estrutura sintática dos arquivos `domain.pddl` e `problem.pddl`, utilizados na definição de domínios e problemas em planejadores automáticos. 

A ferramenta realiza a Análise Léxica e a Análise Sintática, detectando e reportando erros estruturais com base nas regras da linguagem PDDL.

A ferramenta desenvolvida é capaz de:

- **Análise Léxica:** Ler o código fonte PDDL e transformá-lo em uma sequência de tokens (unidades mínimas com significado, como palavras-chave, identificadores, parênteses, etc.).

- **Análise Sintática:** Verificar se a sequência de tokens gerada pelo analisador léxico está de acordo com a gramática (regras de sintaxe) da linguagem PDDL. Em caso de sucesso, o parser confirma que o arquivo está bem formado sintaticamente; em caso de falha, ele reporta um erro de sintaxe.

## Linguagem Suportada

O compilador aceita uma linguagem compatível com a sintaxe básica do PDDL, com suporte para os seguintes elementos:

- **Definições de domínio e problema** com `define`, `domain`, `problem`.
- **Seções estruturadas**, como `:requirements`, `:types`, `:predicates`, `:action`, `:parameters`, `:precondition` e `:effect`.
- **Uso de símbolos e identificadores** com prefixo `?` para variáveis.
- **Operadores lógicos** como `and`, `not`, e conectivos PDDL válidos.

### Exemplos de Comandos Analisados:
A linguagem PDDL tem uma sintaxe baseada em S-expressions (similar a LISP). Um exemplo de definição de um domínio:

```lisp
(define (domain hello-world)
  (:predicates (saudacao))
  (:action dizer-ola
    :precondition ()
    :effect (saudacao)))
```

E um exemplo de definição de um problema para esse domínio:

```lisp
(define (problem blocks-a-on-b)
    (:domain blocks-world)
    (:objects a b - block)
    (:init (ontable b) (clear a) (handempty))
    (:goal (on a b))
)
```

## Estrutura do Projeto

```text
pddl_parser/
├── exemplos/                # Arquivos de exemplo .pddl
│   ├── domain_helloworld.pddl
│   └── problem_helloworld.pddl
├── src/
│   ├── lexer.py             # Analisador Léxico
│   ├── parser.py            # Analisador Sintático (recursivo descendente)
│   ├── main.py        # Enumeração de códigos de tokens
│   └── ast.py               # Representação da Árvore Sintática Abstrata (AST)
├── parser_interativo.py                  # Ponto de entrada principal
├── README.md                # Documentação do projeto
```

## Como rodar
Clone o repositório:
```bash
git clone https://github.com/VHbernardes/trab_final_compiladores.git
```
Para executar a ferramenta e interagir com os parsers, navegue até a raiz do repositório (pddl_parser/) e execute o script parser_interativo.py:
```bash
cd pddl_parser
python3 parser_interativo.py
```
O programa apresentará um menu interativo com as seguintes opções:

- **Opções 1 a 5**- Executam exemplos válidos de arquivos PDDL, analisando tanto o domínio (.pddl) quanto o problema (.pddl) associado. A saída mostrará os logs detalhados do processo de análise sintática.
- **Opção 6** - Exemplos Inválidos: Permite escolher arquivos PDDL que contêm erros sintáticos intencionais. O parser tentará analisá-los e reportará a falha, demonstrando sua capacidade de detecção de erros.
- **Opção 7** - Gerar AST de um exemplo: Permite escolher um exemplo válido para que o parser gere e imprima a Árvore de Sintaxe Abstrata (AST) correspondente ao arquivo PDDL.
- **Opção 0** - Sair: Encerra o programa.

## Exemplos
A pasta exemplos/ contém arquivos PDDL com diferentes características:

- **domain_helloworld.pddl / problem_helloworld.pddl**: Exemplos mínimos para teste básico.
- **domain_blocks.pddl / problem_blocks.pddl:** Domínio e problema clássicos do "Mundo dos Blocos", demonstrando tipos, predicados e ações mais complexas.
- **domain_brainfuck.pddl / problem_brainfuck.pddl:** Exemplos criativos que modelam a lógica de uma máquina Brainfuck usando a sintaxe PDDL. Demonstram a flexibilidade sintática do PDDL e a - capacidade do parser de analisar estruturas diversas.
- **domain_json.pddl / problem_json.pddl:** Exemplos que modelam a manipulação de uma estrutura JSON usando a sintaxe PDDL.
- **domain_lights.pddl / problem_lights.pddl:** Domínio e problema de controle de luzes.
- **domain_blocks_invalido.pddl:** Exemplo com um erro sintático (ex: parêntese ausente, palavra-chave malformada) que o parser deve detectar.
- **domain_json_invalido.pddl:** Exemplo com outro tipo de erro sintático (ex: estrutura incorreta de um predicado) que o parser deve detectar.

## Estrutura do Código
* **`parser_interativo.py`**: É o script principal que fornece o menu interativo e orquestra a execução das funcionalidades do analisador.
* **`src/`**: Contém os módulos principais do analisador:
    * **`lexer.py`**: Implementa a Análise Léxica. É responsável por ler o arquivo PDDL e dividi-lo em uma sequência de tokens (palavras-chave, identificadores, parênteses, operadores, etc.). Utiliza expressões regulares para o reconhecimento dos padrões de tokens.
    * **`parser.py`**: Implementa a Análise Sintática utilizando uma abordagem de **Descida Recursiva manual**. Cada regra gramatical PDDL (como `define`, `domain`, `action`) é representada por um método. Este módulo valida a estrutura do PDDL e imprime logs detalhados do processo de reconhecimento sintático.
    * **`main.py`**: Atua como um ponto de entrada para a funcionalidade principal do parser, especialmente para a **geração da AST**. A função `parse_to_ast` (importada por `parser_interativo.py`) está localizada aqui e é responsável por construir a Árvore de Sintaxe Abstrata (AST) a partir do código PDDL, representando-o como uma estrutura de dados aninhada (dicionários e listas Python) para posterior análise ou visualização.

### Etapas de Compilação Implementadas
O projeto foca e implementa as duas primeiras fases essenciais de um compilador:
* **Análise Léxica**: Realizada pelo módulo `lexer.py`. Converte a cadeia de caracteres do código fonte PDDL em uma sequência de tokens.
* **Análise Sintática**: Realizada pelo módulo `parser.py`. Verifica se a sequência de tokens está em conformidade com as regras gramaticais do PDDL, garantindo que o código está estruturado corretamente. Parte dessa fase também é a **construção da AST** realizada através da função `parse_to_ast` (em `src/main.py`), que representa a estrutura hierárquica do código.

### Bugs, Limitações e Problemas Conhecidos
* **Cobertura PDDL**: O parser implementa um subconjunto da linguagem PDDL, focando nas seções mais comuns (`:requirements`, `:types`, `:constants`, `:predicates`, `:actions`, `:domain`, `:objects`, `:init`, `:goal`, `:metric`). Seções mais complexas ou menos comuns (como `:durative-action`, `:derived`, `:functions` completas, ou expressões numéricas e lógicas mais avançadas) podem não estar totalmente implementadas.
* **Geração de AST**: A geração da Árvore de Sintaxe Abstrata (AST) é uma funcionalidade presente, sendo a AST gerada uma representação em dicionários/listas Python. Originalmente, havia a intenção de explorar a geração da AST também por meio da biblioteca **Lark**, em paralelo com o parser manual. No entanto, devido a complexidades inesperadas na integração e depuração de erros específicos da biblioteca (`KeyError: '_NL'`), e limitações de tempo, não foi possível implementar e finalizar a geração da AST via Lark.

## Referências
* Crafting Interpreters (Bob Nystrom)
* Documentação Oficial do PDDL: Descreva qual versão ou documentação você consultou para entender a sintaxe e a estrutura da linguagem (ex: PDDL 1.2, PDDL 2.1).
