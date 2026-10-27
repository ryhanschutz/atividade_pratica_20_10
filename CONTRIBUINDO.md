# Contribuindo com o Projeto AeroMotion Dynamics

Agradecemos o interesse em contribuir com este repositório! Siga as diretrizes abaixo para manter o padrão de qualidade e rastreabilidade do código.

## Padrão de Branches

- `main`: Branch principal, sempre estável e pronta para produção.
- `feat/nome-da-funcionalidade`: Para novas funcionalidades.
- `fix/nome-da-correcao`: Para correção de bugs.
- `docs/nome-da-documentacao`: Para melhorias ou criação de documentação.

## Mensagens de Commit (Conventional Commits)

Utilizamos o padrão **Conventional Commits** em português, no modo imperativo e com até 72 caracteres no título:

```text
tipo(escopo): descrição concisa da alteração no imperativo

[corpo opcional explicando o motivo da mudança]
```

### Tipos permitidos:
- `feat`: Nova funcionalidade adicionada.
- `fix`: Correção de um bug.
- `docs`: Alterações na documentação.
- `refactor`: Refatoração de código que não altera o comportamento.
- `test`: Adição ou ajuste de testes unitários/integração.
- `chore`: Atualização de tarefas de build, pacotes ou configurações.
- `ci`: Alterações nos fluxos de automação e CI/CD.

## Processo de Contribuição

1. Crie uma branch a partir da `main` (`git checkout -b feat/minha-melhoria`).
2. Implemente suas alterações seguindo o padrão de nomenclatura (kebab-case em arquivos, snake_case em Python).
3. Execute os testes locais com `pytest`.
4. Faça o commit seguindo a convenção descrita acima.
5. Abra um **Pull Request** para a branch `main`.
