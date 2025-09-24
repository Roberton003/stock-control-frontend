#!/bin/bash
# Script de deploy para staging e produção
# Autor: Stock Control Lab Team
# Data: 24/09/2025

set -e  # Sair se algum comando falhar

# Função para exibir mensagem de erro e sair
error_exit() {
    echo "❌ ERRO: $1"
    exit 1
}

# Verificar se o ambiente foi passado como argumento
if [ -z "$1" ]; then
    echo "Uso: $0 [staging|production]"
    exit 1
fi

ENVIRONMENT=$1

echo "🚀 Iniciando deploy para ambiente: $ENVIRONMENT"

# Função para deploy em staging
deploy_to_staging() {
    echo "🔧 Configurando deploy para staging..."
    
    # Verificar se estamos no branch de staging
    CURRENT_BRANCH=$(git branch --show-current)
    if [ "$CURRENT_BRANCH" != "staging" ] && [ "$CURRENT_BRANCH" != "develop" ]; then
        echo "⚠️  Aviso: Você não está no branch staging ou develop"
        read -p "Deseja continuar mesmo assim? (s/n): " -n 1 -r
        echo
        [[ ! $REPLY =~ ^[Ss]$ ]] && echo "Operação cancelada." && exit 1
    fi
    
    # Atualizar código
    echo "🔄 Atualizando código..."
    git pull origin $CURRENT_BRANCH
    
    # Atualizar dependências
    echo "📦 Atualizando dependências..."
    cd backend && source venv/bin/activate
    pip install -r requirements.txt
    cd ../frontend && npm install
    cd ..
    
    # Executar migrações
    echo "🔄 Executando migrações..."
    cd backend && python manage.py migrate --settings=config.settings.staging
    cd ..
    
    # Coletar arquivos estáticos
    echo "🧹 Coletando arquivos estáticos..."
    cd backend && python manage.py collectstatic --settings=config.settings.staging --noinput
    cd ..
    
    # Fazer build do frontend
    echo "🔨 Fazendo build do frontend..."
    cd frontend && npm run build
    cd ..
    
    # Testar a aplicação
    echo "🧪 Testando a aplicação..."
    cd backend && python -m pytest --settings=config.settings.staging
    cd ..
    
    echo "✅ Deploy para staging concluído com sucesso!"
}

# Função para deploy em produção
deploy_to_production() {
    echo "🔧 Configurando deploy para produção..."
    
    # Verificar se estamos no branch de produção
    CURRENT_BRANCH=$(git branch --show-current)
    if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
        error_exit "Você não está no branch main ou master para deploy em produção"
    fi
    
    # Confirmar deploy em produção
    echo "⚠️  ATENÇÃO: Você está prestes a fazer deploy em produção!"
    read -p "Tem certeza que deseja continuar? (s/n): " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Ss]$ ]] && echo "Operação cancelada." && exit 1
    
    # Fazer backup do banco de dados
    echo "💾 Fazendo backup do banco de dados..."
    cd backend
    source venv/bin/activate
    python manage.py dumpdata > /backups/backup_$(date +%Y%m%d_%H%M%S).json
    cd ..
    
    # Atualizar código
    echo "🔄 Atualizando código..."
    git pull origin $CURRENT_BRANCH
    
    # Atualizar dependências
    echo "📦 Atualizando dependências..."
    cd backend && pip install -r requirements.txt
    cd ../frontend && npm install
    cd ..
    
    # Executar migrações
    echo "🔄 Executando migrações..."
    cd backend && python manage.py migrate --settings=config.settings.production
    cd ..
    
    # Coletar arquivos estáticos
    echo "🧹 Coletando arquivos estáticos..."
    cd backend && python manage.py collectstatic --settings=config.settings.production --noinput
    cd ..
    
    # Fazer build do frontend
    echo "🔨 Fazendo build do frontend..."
    cd frontend && npm run build
    cd ..
    
    # Testar a aplicação (testes críticos apenas)
    echo "🧪 Testando a aplicação..."
    cd backend && python -m pytest --settings=config.settings.production -k "critical"
    cd ..
    
    # Reiniciar serviços
    echo "🔄 Reiniciando serviços..."
    sudo systemctl restart stock-control-backend
    sudo systemctl restart nginx
    
    # Verificar status dos serviços
    sudo systemctl status stock-control-backend --no-pager
    sudo systemctl status nginx --no-pager
    
    echo "✅ Deploy para produção concluído com sucesso!"
}

# Função para deploy com Docker
deploy_with_docker() {
    echo "🐳 Fazendo deploy com Docker..."
    
    # Construir imagens
    echo "🔨 Construindo imagens Docker..."
    docker-compose -f docker-compose.$ENVIRONMENT.yml build
    
    # Subir containers
    echo "🚀 Subindo containers..."
    docker-compose -f docker-compose.$ENVIRONMENT.yml up -d
    
    # Aguardar os serviços estarem prontos
    echo "⏳ Aguardando serviços estarem prontos..."
    sleep 30
    
    # Verificar saúde dos containers
    docker-compose -f docker-compose.$ENVIRONMENT.yml ps
    
    echo "✅ Deploy com Docker concluído!"
}

# Executar o deploy com base no ambiente
case $ENVIRONMENT in
    "staging")
        deploy_to_staging
        ;;
    "production")
        deploy_to_production
        ;;
    *)
        error_exit "Ambiente inválido. Use staging ou production"
        ;;
esac

echo ""
echo "📋 Próximos passos:"
echo "   1. Verificar logs da aplicação"
echo "   2. Testar manualmente as funcionalidades principais"
echo "   3. Verificar o monitoramento e alertas"
echo ""
echo "🔍 Links úteis:"
echo "   - Aplicação: https://$ENVIRONMENT.stock-control-lab.com"
echo "   - Monitoramento: https://monitoring.stock-control-lab.com"
echo "   - Logs: /var/log/stock-control/"