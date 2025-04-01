# PakeWrapper

Um script Python para automatizar a criação de apps via Pake no macOS.

## Requisitos

- macOS
- Python 3.6+
- Pake instalado via Homebrew (`/opt/homebrew/bin/pake`)

## Instalação

1. Clone este repositório ou baixe o arquivo `pakewrapper.py`
2. Torne o script executável:
   ```bash
   chmod +x pakewrapper.py
   ```

## Uso

Execute o script:
```bash
./pakewrapper.py
```

O script irá:
1. Solicitar a URL do site
2. Opcionalmente, solicitar um caminho para um ícone (.icns ou .png)
3. Gerar e executar o comando Pake com as configurações otimizadas
4. Mostrar o progresso e resultado da compilação

## Configurações Padrão

- Dimensões: 1280x800 (otimizado para M3)
- Transparência: habilitada
- Build: universal (--darwin-universal)
- Nome do app: baseado no domínio da URL

## Logs

Os logs são salvos em `~/.pakewrapper.log` para diagnóstico de problemas.

## Tratamento de Erros

O script inclui validações para:
- Existência do Pake
- Formato da URL
- Caminho e formato do ícone
- Permissões de execução
- Erros durante a compilação

## Interrupção

Você pode interromper o processo a qualquer momento com Ctrl+C.

## Sugestões Pós-Instalação

Após a criação do app:
1. Arraste o .app para a pasta Applications
2. Execute pela primeira vez para permitir no Security
3. Use o Spotlight (⌘+Space) para lançar o app 