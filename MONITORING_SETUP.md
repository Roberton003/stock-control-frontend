# Monitoramento e Observabilidade - Stock Control Lab

## Visão Geral

Este documento descreve as ferramentas e práticas recomendadas para monitoramento, logging e observabilidade do sistema Stock Control Lab tanto em ambiente de desenvolvimento quanto em produção.

## Monitoramento de Aplicações

### Backend (Django)

#### 1. Django Extensions para Monitoramento
- `django-extensions`: Ferramentas de diagnóstico e perfilamento
- `django-debug-toolbar`: Para ambiente de desenvolvimento
- `silk`: Perfilamento de requisições, consultas e templates

#### 2. Configurações de Monitoramento em Produção

Adicione ao `requirements.txt` para produção:
```
sentry-sdk==2.19.2  # Para reportar erros em produção
django-prometheus==2.3.1  # Para métricas Prometheus
```

##### Configuração do Django para métricas:
```python
# settings.py
INSTALLED_APPS = [
    # ... outros apps
    'django_prometheus',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    # ... outros middlewares
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

# Exportar métricas
PROMETHEUS_EXPORT_MIGRATIONS = True
```

#### 3. Captura de Exceções com Sentry
```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn="https://<sua-chave>@sentry.io/<seu-projeto>",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )
```

### Frontend (Vue.js)

#### 1. Monitoramento de Desempenho
- `@sentry/vue`: Integração do Sentry com Vue.js
- `vue-logger-plugin`: Para logs estruturados no frontend

#### 2. Configuração de Monitoramento no Frontend
```javascript
// main.js
import { createApp } from 'vue'
import * as Sentry from '@sentry/vue'
import { Integrations } from '@sentry/tracing'

const app = createApp(App)

if (process.env.NODE_ENV === 'production') {
  Sentry.init({
    app,
    dsn: 'https://<sua-chave>@sentry.io/<seu-projeto>',
    integrations: [
      new Integrations.BrowserTracing(),
    ],
    traces_sample_rate: 1.0,
  })
}
```

## Monitoramento de Infraestrutura

### 1. Prometheus + Grafana
- **Prometheus**: Coleta e armazenamento de métricas
- **Grafana**: Visualização e alertas

#### Configuração do Prometheus
Arquivo `prometheus.yml`:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'stock-control-backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'  # Precisa de django-prometheus
    
  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:9187']  # Exporter do PostgreSQL

  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:9121']  # Exporter do Redis
```

### 2. Exporters para Serviços
- **postgres_exporter**: Para métricas do PostgreSQL
- **redis_exporter**: Para métricas do Redis
- **node_exporter**: Para métricas do sistema operacional

## Configuração de Logging

### Níveis de Log
- `DEBUG`: Informações detalhadas, tipicamente de interesse apenas ao diagnosticar problemas
- `INFO`: Confirmação de que as coisas estão funcionando como esperado
- `WARNING`: Indicação de que ocorreu algo inesperado
- `ERROR`: Erro devido a algum problema
- `CRITICAL`: Erro grave

### Configuração de Logging no Django
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/stock-control.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'inventory': {  # Seu app principal
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Monitoramento de Saúde

### 1. Endpoint de Health Check
Adicione um endpoint `/health/` para verificar a saúde do sistema:

```python
# views.py
from django.http import JsonResponse

def health_check(request):
    # Verificar conexão com o banco de dados
    from django.db import connection
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False
    
    # Verificar outros serviços...
    
    status = {
        'status': 'ok' if db_ok else 'error',
        'database': 'ok' if db_ok else 'error',
        'timestamp': timezone.now().isoformat(),
    }
    
    return JsonResponse(status, status=200 if db_ok else 503)
```

### 2. Health Checks para Docker
Adicione HEALTHCHECK no Dockerfile:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health/ || exit 1
```

## Alertas e Notificações

### 1. Configuração de Alertas no Grafana
- Tempo de resposta da API acima de 2 segundos
- Taxa de erros acima de 5%
- Uso de CPU acima de 80%
- Uso de memória acima de 80%
- Falhas de conexão com o banco de dados

### 2. Integração com Slack/Discord para Alertas
Configure notificações via webhook para canais de operações.

## Dashboard de Monitoramento

### Métricas Chave (KPIs)
- **Disponibilidade**: % de tempo que o sistema está disponível
- **Tempo de resposta**: Tempo médio de resposta das APIs
- **Throughput**: Número de requisições por minuto
- **Erros**: Taxa de erro das requisições
- **Latência**: Tempo de processamento das requisições
- **Uso de recursos**: CPU, memória, disco

### Dashboard Recomendado
1. **Dashboard Geral do Sistema**
   - Métricas de desempenho do sistema
   - Uso de recursos
   - Status dos serviços

2. **Dashboard de Aplicação**
   - Métricas de requisições
   - Tempo de resposta por endpoint
   - Erros e exceções

3. **Dashboard de Banco de Dados**
   - Consultas por segundo
   - Tempo de execução de consultas
   - Conexões ativas

## Monitoramento em Tempo Real

### 1. Live Dashboard com WebSocket
Implemente atualizações em tempo real para:
- Notificações de sistema
- Alertas críticos
- Métricas em tempo real

### 2. Monitoramento de Regras de Negócio
- Reagentes com estoque baixo
- Reagentes próximos ao vencimento
- Requisições pendentes por tempo

## Configuração para Docker Compose

Exemplo de configuração para incluir ferramentas de monitoramento no docker-compose:

```yaml
version: '3.8'

services:
  # ... outros serviços

  # Prometheus
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  # Grafana
  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
    depends_on:
      - prometheus

  # PostgreSQL Exporter
  postgres-exporter:
    image: prometheuscommunity/postgres-exporter
    environment:
      - DATA_SOURCE_NAME=postgresql://stock_user:stock_password@db:5432/stock_control_lab?sslmode=disable
    ports:
      - "9187:9187"
    depends_on:
      - db

  # Redis Exporter
  redis-exporter:
    image: oliver006/redis_exporter
    environment:
      - REDIS_ADDR=redis:6379
    ports:
      - "9121:9121"
    depends_on:
      - redis

volumes:
  grafana-storage:
```

## Boas Práticas

1. **Monitore métricas de negócio**, não apenas métricas técnicas
2. **Defina alertas com limiares apropriados** para evitar alertas falsos
3. **Registre logs estruturados** para facilitar análise
4. **Use tags consistentes** para facilitar filtragem e agregação
5. **Teste seus alertas** para garantir que estão funcionando corretamente
6. **Documente seus dashboards** e métricas importantes

## Considerações sobre Custo

- **Elastic Stack (ELK)**: Poderoso, mas mais caro em ambientes grandes
- **Sentry**: Excelente para reporte de erros, com plano gratuito limitado
- **Grafana Cloud**: Oferece hospedagem gerenciada para Prometheus/Grafana
- **New Relic / DataDog**: Soluções comerciais completas com trial gratuito

Este conjunto de ferramentas e práticas fornecerá observabilidade completa para o sistema Stock Control Lab em ambiente de produção.