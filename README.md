# PakeWrapper

Um script Python para automatizar a criação de apps via Pake no macOS.

## Requisitos

- macOS
- Python 3.6+
- Pake instalado via Homebrew (`/opt/homebrew/bin/pake`)

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/profgabrielramos/PakeScript.git
   cd PakeScript
   ```

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
- Build: universal (--multi-arch)
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

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

Gabriel Ramos - [@profgabrielramos](https://github.com/profgabrielramos) 