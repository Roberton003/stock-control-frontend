# Guia Rápido - Frontend Moderno

## Iniciar o Projeto

### 1. Instalar dependências
```bash
cd stock_control_lab
npm install
```

### 2. Iniciar o servidor de desenvolvimento
```bash
# Terminal 1 - Iniciar o Vite (frontend)
cd stock_control_lab
npm run dev

# Terminal 2 - Iniciar o Django (backend)
cd stock_control_lab
python manage.py runserver
```

## Estrutura de Arquivos

### Pasta `static/src/css/`
- `main.css`: Ponto de entrada principal para todos os estilos
- `colors.css`: Definições de cores personalizadas
- `typography.css`: Estilos de tipografia
- `animations.css`: Animações customizadas
- `components/`: Estilos específicos por componente

### Pasta `static/src/js/`
- `main.js`: Arquivo principal JavaScript
- `dashboard.js`, `products.js`, etc.: Scripts específicos por página
- `utils/`: Funções utilitárias

### Pasta `templates/`
- `base/base.html`: Template principal
- `components/`: Componentes reutilizáveis
- `pages/`: Templates específicos

## Componentes Principais

### Botões
```html
<button class="btn btn-primary">Botão Primário</button>
<button class="btn btn-secondary">Botão Secundário</button>
<button class="btn btn-danger">Botão Perigo</button>
```

### Cards
```html
<div class="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 border-l-4 border-modern-primary">
  <div class="flex justify-between items-center">
    <div>
      <p class="text-gray-500 dark:text-gray-400 text-sm">Título do Card</p>
      <h3 class="text-2xl font-bold mt-1 text-gray-800 dark:text-white">Conteúdo</h3>
    </div>
    <div class="bg-modern-primary bg-opacity-10 p-3 rounded-full">
      <i class="fas fa-icon text-modern-primary text-xl"></i>
    </div>
  </div>
</div>
```

### Tabelas
```html
<table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
  <thead class="bg-gray-50 dark:bg-gray-700">
    <tr>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Cabeçalho</th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Cabeçalho</th>
    </tr>
  </thead>
  <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
    <tr>
      <td class="px-6 py-4 whitespace-nowrap">Dado</td>
      <td class="px-6 py-4 whitespace-nowrap">Dado</td>
    </tr>
  </tbody>
</table>
```

## Funcionalidades Avançadas

### Dark Mode
O sistema suporta modo claro/escuro com persistência local:

```javascript
// Ativar ou desativar dark mode
document.documentElement.classList.toggle('dark');
localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
```

### Animações
Classes de animação disponíveis:
- `animate-pulse` - Pulsação
- `animate-spin` - Rotação
- `hover-lift` - Efeito de elevação no hover
- `stat-card` - Efeitos para cards de estatísticas

### Componentes Interativos com Alpine.js
```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open" x-transition>
    Conteúdo visível/oculto dinamicamente
  </div>
</div>
```

## Build para Produção

```bash
# Gerar assets otimizados
npm run build

# Os arquivos serão gerados em:
# - stock_control_lab/static/dist/css/
# - stock_control_lab/static/dist/js/
```

## Personalização

### Cores
Edite `tailwind.config.js` para personalizar a paleta de cores:

```javascript
colors: {
  primary: {
    DEFAULT: '#034EA2',
    '50': '#E6F0FF',
    // ...
  },
}
```

### Tipografia
Adicione novas fontes editando `static/src/css/main.css`:

```css
@import url('https://fonts.googleapis.com/css2?family=NomeDaFonte:wght@300;400;500;600;700&display=swap');

@layer base {
  html {
    font-family: 'NomeDaFonte', sans-serif;
  }
}
```

## Solução de Problemas

### Vite não inicia
Verifique se a porta 3000 está disponível:
```bash
# Verificar processos na porta 3000
lsof -i :3000
# Ou no Windows
netstat -ano | findstr :3000
```

### Estilos não aplicando
- Verifique se o arquivo `tailwind.config.js` está apontando para os templates corretos
- Confirme que os arquivos de CSS estão sendo importados corretamente no `main.css`

### Dark Mode não persistindo
Verifique se o template base está usando a classe condicional:
```html
<html class="{% if request.user.is_dark_mode %}dark{% endif %}">
```

## Próximos Passos

1. Adicionar mais componentes reutilizáveis
2. Implementar testes de interface
3. Otimizar imagens e assets
4. Adicionar internacionalização (i18n)