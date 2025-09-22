# Renomear Repositório no GitHub

## Passos para renomear o repositório de `stock-control-frontend` para `stock-control-lab`:

1. Acesse https://github.com/Roberton003/stock-control-frontend
2. Clique em "Settings" (na barra lateral direita)
3. Role para baixo até a seção "Danger Zone"
4. Clique no botão "Rename" próximo a "Repository name"
5. Altere o nome de `stock-control-frontend` para `stock-control-lab`
6. Clique em "Rename repository"

## Após renomear o repositório:

1. Atualize o remote URL localmente:
   ```bash
   cd stock-control-frontend
   git remote set-url origin https://github.com/Roberton003/stock-control-lab.git
   ```

2. Renomeie o diretório local (opcional):
   ```bash
   cd ..
   mv stock-control-frontend stock-control-lab
   ```

## Atualizações necessárias após renomear:

- [ ] Atualizar README.md com novo link do repositório
- [ ] Atualizar package.json com novo nome do projeto
- [ ] Atualizar links em documentações relacionadas
- [ ] Atualizar referências no backend (se houver)
- [ ] Atualizar configurações de CI/CD (se houver)