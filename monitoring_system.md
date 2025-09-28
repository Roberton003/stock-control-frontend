                            elif word in ["failed", "error"]:
                                failed = int(words[i-1])
                        
                        total = passed + failed
                        return (passed / total * 100) if total > 0 else 0.0
            
            # Se não houver falhas, assume 100%
            return 100.0 if result.returncode == 0 else 0.0
            
        except Exception as e:
            print(f"Erro na análise de testes: {e}")
        
        return 0.0
    
    def _analyze_complexity(self) -> float:
        """Analisar complexidade ciclomática"""
        try:
            result = subprocess.run([
                str(self.venv_python), "-m", "radon", "cc", ".", "--json"
            ], capture_output=True, text=True, cwd=self.project_path)
            
            if result.returncode == 0:
                complexity_data = json.loads(result.stdout)
                total_complexity = 0
                function_count = 0
                
                for file_data in complexity_data.values():
                    for item in file_data:
                        if item.get("type") in ["function", "method"]:
                            total_complexity += item.get("complexity", 0)
                            function_count += 1
                
                return total_complexity / function_count if function_count > 0 else 0.0
        except Exception:
            pass
        
        return 0.0
    
    def _analyze_security(self) -> tuple[int, float]:
        """Analisar questões de segurança"""
        try:
            result = subprocess.run([
                str(self.venv_python), "-m", "bandit", "-r", ".", 
                "-f", "json", "--quiet"
            ], capture_output=True, text=True, cwd=self.project_path)
            
            if result.stdout:
                bandit_data = json.loads(result.stdout)
                issues = len(bandit_data.get("results", []))
                
                # Calcular score baseado na severidade
                high_issues = len([r for r in bandit_data.get("results", []) 
                                 if r.get("issue_severity") == "HIGH"])
                medium_issues = len([r for r in bandit_data.get("results", []) 
                                   if r.get("issue_severity") == "MEDIUM"])
                low_issues = len([r for r in bandit_data.get("results", []) 
                                if r.get("issue_severity") == "LOW"])
                
                # Penalizar por severidade
                score = 100.0 - (high_issues * 20) - (medium_issues * 10) - (low_issues * 5)
                return issues, max(0.0, score)
        except Exception:
            pass
        
        return 0, 100.0
    
    def _measure_build_time(self) -> float:
        """Medir tempo de build"""
        start_time = time.time()
        try:
            subprocess.run([
                str(self.venv_python), "manage.py", "collectstatic", 
                "--noinput", "--clear"
            ], capture_output=True, cwd=self.project_path)
        except Exception:
            pass
        
        return time.time() - start_time
    
    def _analyze_code_style(self) -> int:
        """Analisar violações de estilo"""
        violations = 0
        
        # Flake8
        try:
            result = subprocess.run([
                str(self.venv_python), "-m", "flake8", ".", "--count"
            ], capture_output=True, text=True, cwd=self.project_path)
            
            if result.stdout.strip().isdigit():
                violations += int(result.stdout.strip())
        except Exception:
            pass
        
        return violations
    
    def _analyze_documentation(self) -> float:
        """Analisar qualidade da documentação"""
        try:
            # Contar arquivos com docstrings
            python_files = list(self.project_path.rglob("*.py"))
            documented_files = 0
            
            for file in python_files:
                if "venv" in str(file) or "__pycache__" in str(file):
                    continue
                    
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '"""' in content or "'''" in content:
                            documented_files += 1
                except Exception:
                    continue
            
            return (documented_files / len(python_files) * 100) if python_files else 0.0
        except Exception:
            return 0.0
    
    def _calculate_overall_score(self, metrics: QualityMetrics) -> float:
        """Calcular score geral ponderado"""
        weights = {
            'coverage': 0.25,      # 25% - Cobertura de testes
            'tests': 0.20,         # 20% - Taxa de sucesso dos testes
            'security': 0.20,      # 20% - Score de segurança
            'complexity': 0.10,    # 10% - Complexidade (inversa)
            'style': 0.15,         # 15% - Estilo (inversa)
            'documentation': 0.10  # 10% - Documentação
        }
        
        # Normalizar métricas (0-100)
        normalized_scores = {
            'coverage': metrics.code_coverage,
            'tests': metrics.test_pass_rate,
            'security': metrics.security_score,
            'complexity': max(0, 100 - (metrics.cyclomatic_complexity * 10)),  # Inversa
            'style': max(0, 100 - (metrics.style_violations * 2)),  # Inversa
            'documentation': metrics.documentation_score
        }
        
        # Calcular score ponderado
        weighted_score = sum(
            score * weights[metric] 
            for metric, score in normalized_scores.items()
        )
        
        return round(weighted_score, 2)
    
    def _get_quality_grade(self, score: float) -> str:
        """Converter score em nota"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"
    
    def _save_metrics(self, metrics: QualityMetrics):
        """Salvar métricas no histórico"""
        history = []
        
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    history = json.load(f)
            except Exception:
                pass
        
        history.append(asdict(metrics))
        
        # Manter apenas os últimos 100 registros
        history = history[-100:]
        
        with open(self.metrics_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def _print_quality_report(self, metrics: QualityMetrics):
        """Imprimir relatório de qualidade"""
        print(f"\n📊 RELATÓRIO DE QUALIDADE")
        print(f"{'='*50}")
        print(f"Agente: {metrics.agent_name}")
        print(f"Task ID: {metrics.task_id}")
        print(f"Data: {metrics.timestamp[:19]}")
        print(f"\n🎯 SCORE FINAL: {metrics.overall_score}/100 (Nota: {metrics.quality_grade})")
        
        print(f"\n📈 MÉTRICAS DETALHADAS:")
        print(f"  • Cobertura de Testes: {metrics.code_coverage:.1f}%")
        print(f"  • Taxa de Sucesso: {metrics.test_pass_rate:.1f}%")
        print(f"  • Complexidade Média: {metrics.cyclomatic_complexity:.1f}")
        print(f"  • Score de Segurança: {metrics.security_score:.1f}/100")
        print(f"  • Violações de Estilo: {metrics.style_violations}")
        print(f"  • Documentação: {metrics.documentation_score:.1f}%")
        
        if metrics.security_issues > 0:
            print(f"\n⚠️  ALERTAS DE SEGURANÇA: {metrics.security_issues} issues encontradas")
        
        # Status baseado na nota
        if metrics.quality_grade in ["A+", "A"]:
            print(f"\n✅ ENTREGA APROVADA - Excelente qualidade!")
        elif metrics.quality_grade in ["B", "C"]:
            print(f"\n⚠️  ENTREGA COM RESSALVAS - Melhorias recomendadas")
        else:
            print(f"\n❌ ENTREGA REJEITADA - Qualidade abaixo do padrão")
    
    def get_quality_history(self, agent_name: str = None) -> List[Dict]:
        """Obter histórico de qualidade"""
        if not self.metrics_file.exists():
            return []
        
        try:
            with open(self.metrics_file, 'r') as f:
                history = json.load(f)
            
            if agent_name:
                history = [m for m in history if m['agent_name'] == agent_name]
            
            return sorted(history, key=lambda x: x['timestamp'], reverse=True)
        except Exception:
            return []
    
    def generate_quality_trends(self):
        """Gerar relatório de tendências de qualidade"""
        history = self.get_quality_history()
        
        if not history:
            print("Nenhum histórico de qualidade encontrado.")
            return
        
        # Agrupar por agente
        agents = {}
        for entry in history:
            agent = entry['agent_name']
            if agent not in agents:
                agents[agent] = []
            agents[agent].append(entry)
        
        print(f"\n📈 TENDÊNCIAS DE QUALIDADE")
        print(f"{'='*60}")
        
        for agent, entries in agents.items():
            scores = [e['overall_score'] for e in entries[-10:]]  # Últimas 10 entregas
            avg_score = sum(scores) / len(scores)
            
            trend = "📈" if len(scores) > 1 and scores[-1] > scores[0] else "📉"
            
            print(f"\n🤖 {agent.upper()}:")
            print(f"  • Entregas: {len(entries)}")
            print(f"  • Score Médio: {avg_score:.1f}")
            print(f"  • Tendência: {trend}")
            print(f"  • Última Nota: {entries[0]['quality_grade']}")

class DeliveryValidator:
    """Validador de entregas com critérios mínimos"""
    
    def __init__(self):
        self.minimum_criteria = {
            'overall_score': 60.0,      # Score mínimo geral
            'code_coverage': 70.0,      # Cobertura mínima de testes
            'test_pass_rate': 90.0,     # Taxa mínima de sucesso
            'security_score': 80.0,     # Score mínimo de segurança
            'max_security_issues': 3,   # Máximo de issues de segurança
            'max_style_violations': 20  # Máximo de violações de estilo
        }
    
    def validate_delivery(self, metrics: QualityMetrics) -> tuple[bool, List[str]]:
        """Validar se entrega atende aos critérios mínimos"""
        issues = []
        
        if metrics.overall_score < self.minimum_criteria['overall_score']:
            issues.append(f"Score geral baixo: {metrics.overall_score:.1f} < {self.minimum_criteria['overall_score']}")
        
        if metrics.code_coverage < self.minimum_criteria['code_coverage']:
            issues.append(f"Cobertura de testes baixa: {metrics.code_coverage:.1f}% < {self.minimum_criteria['code_coverage']}%")
        
        if metrics.test_pass_rate < self.minimum_criteria['test_pass_rate']:
            issues.append(f"Taxa de sucesso baixa: {metrics.test_pass_rate:.1f}% < {self.minimum_criteria['test_pass_rate']}%")
        
        if metrics.security_score < self.minimum_criteria['security_score']:
            issues.append(f"Score de segurança baixo: {metrics.security_score:.1f} < {self.minimum_criteria['security_score']}")
        
        if metrics.security_issues > self.minimum_criteria['max_security_issues']:
            issues.append(f"Muitas issues de segurança: {metrics.security_issues} > {self.minimum_criteria['max_security_issues']}")
        
        if metrics.style_violations > self.minimum_criteria['max_style_violations']:
            issues.append(f"Muitas violações de estilo: {metrics.style_violations} > {self.minimum_criteria['max_style_violations']}")
        
        is_valid = len(issues) == 0
        return is_valid, issues

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Uso: python scripts/quality_metrics.py <agent_name> <task_description>")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    task_description = " ".join(sys.argv[2:])
    
    project_path = Path(__file__).parent.parent
    analyzer = QualityAnalyzer(project_path)
    validator = DeliveryValidator()
    
    # Analisar qualidade
    metrics = analyzer.analyze_delivery(agent_name, task_description)
    
    # Validar entrega
    is_valid, issues = validator.validate_delivery(metrics)
    
    if is_valid:
        print(f"\n✅ ENTREGA APROVADA!")
    else:
        print(f"\n❌ ENTREGA REJEITADA!")
        print("Issues encontradas:")
        for issue in issues:
            print(f"  • {issue}")
    
    # Exibir tendências
    analyzer.generate_quality_trends()
    
    sys.exit(0 if is_valid else 1)
```

## 🔄 Sistema de Rollback Automático

**scripts/auto_rollback.py:**
```python
#!/usr/bin/env python
"""
Sistema de rollback automático baseado em métricas de qualidade
"""

import json
import subprocess
from pathlib import Path
from quality_metrics import QualityAnalyzer, DeliveryValidator
from backup import BackupManager

class AutoRollbackSystem:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.analyzer = QualityAnalyzer(project_path)
        self.validator = DeliveryValidator()
        self.backup_manager = BackupManager()
        self.config_file = project_path / "config" / "rollback_config.json"
        self.load_config()
    
    def load_config(self):
        """Carregar configuração de rollback"""
        default_config = {
            "auto_rollback_enabled": True,
            "rollback_triggers": {
                "min_score": 50.0,
                "max_failed_tests": 5,
                "max_security_issues": 5,
                "max_build_failures": 3
            },
            "backup_before_changes": True,
            "notification_webhook": None
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                self.config = {**default_config, **config}
            except Exception:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Salvar configuração"""
        self.config_file.parent.mkdir(exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def should_rollback(self, metrics) -> tuple[bool, List[str]]:
        """Verificar se deve fazer rollback baseado nas métricas"""
        triggers = self.config["rollback_triggers"]
        reasons = []
        
        if metrics.overall_score < triggers["min_score"]:
            reasons.append(f"Score muito baixo: {metrics.overall_score}")
        
        if metrics.security_issues > triggers["max_security_issues"]:
            reasons.append(f"Muitas issues de segurança: {metrics.security_issues}")
        
        # Verificar se testes estão falhando
        if metrics.test_pass_rate < 80.0:
            reasons.append(f"Taxa de falha alta nos testes: {100 - metrics.test_pass_rate:.1f}%")
        
        should_rollback = len(reasons) > 0 and self.config["auto_rollback_enabled"]
        return should_rollback, reasons
    
    def execute_rollback(self, agent_name: str, reasons: List[str]) -> bool:
        """Executar rollback automático"""
        print(f"🚨 INICIANDO ROLLBACK AUTOMÁTICO")
        print(f"Agente: {agent_name}")
        print(f"Razões: {', '.join(reasons)}")
        
        # Encontrar backup mais recente antes da entrega problemática
        backups = self.backup_manager.list_backups()
        
        if not backups:
            print("❌ Nenhum backup disponível para rollback")
            return False
        
        # Usar o backup mais recente
        latest_backup = backups[0].name
        
        print(f"🔄 Restaurando backup: {latest_backup}")
        
        success = self.backup_manager.restore_backup(latest_backup)
        
        if success:
            print("✅ Rollback executado com sucesso")
            self.send_notification(agent_name, reasons, latest_backup)
            return True
        else:
            print("❌ Falha no rollback")
            return False
    
    def send_notification(self, agent_name: str, reasons: List[str], backup_name: str):
        """Enviar notificação sobre rollback"""
        message = {
            "type": "rollback_executed",
            "agent": agent_name,
            "reasons": reasons,
            "backup_restored": backup_name,
            "timestamp": datetime.now().isoformat()
        }
        
        webhook_url = self.config.get("notification_webhook")
        if webhook_url:
            try:
                import requests
                requests.post(webhook_url, json=message)
            except Exception as e:
                print(f"⚠️ Falha ao enviar notificação: {e}")
        
        # Log local
        log_file = self.project_path / "logs" / "rollback.log"
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(f"{json.dumps(message)}\n")
    
    def validate_and_rollback(self, agent_name: str, task_description: str) -> bool:
        """Validar entrega e executar rollback se necessário"""
        # Criar backup antes da validação
        if self.config["backup_before_changes"]:
            self.backup_manager.create_backup(f"before_{agent_name}_validation")
        
        # Analisar qualidade
        metrics = self.analyzer.analyze_delivery(agent_name, task_description)
        
        # Verificar se deve fazer rollback
        should_rollback, reasons = self.should_rollback(metrics)
        
        if should_rollback:
            return self.execute_rollback(agent_name, reasons)
        else:
            print("✅ Entrega aprovada - nenhum rollback necessário")
            return True

if __name__ == '__main__':
    import sys
    from datetime import datetime
    
    if len(sys.argv) < 3:
        print("Uso: python scripts/auto_rollback.py <agent_name> <task_description>")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    task_description = " ".join(sys.argv[2:])
    
    project_path = Path(__file__).parent.parent
    rollback_system = AutoRollbackSystem(project_path)
    
    success = rollback_system.validate_and_rollback(agent_name, task_description)
    sys.exit(0 if success else 1)
```

## 📊 Dashboard de Métricas

**templates/dashboard/quality_metrics.html:**
```html
{% extends 'base/base.html' %}
{% load static %}

{% block title %}Métricas de Qualidade{% endblock %}

{% block content %}
<div class="max-w-7xl mx-auto p-6">
    <header class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Dashboard de Qualidade
        </h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">
            Monitoramento de qualidade das entregas dos agentes
        </p>
    </header>

    <!-- Resumo Geral -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="card">
            <div class="p-6">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-green-100 text-green-600">
                        <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                        </svg>
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold">{{ stats.total_deliveries }}</h3>
                        <p class="text-gray-500">Entregas Totais</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="p-6">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-blue-100 text-blue-600">
                        <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold">{{ stats.avg_score|floatformat:1 }}</h3>
                        <p class="text-gray-500">Score Médio</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="p-6">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-yellow-100 text-yellow-600">
                        <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                        </svg>
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold">{{ stats.rollbacks_count }}</h3>
                        <p class="text-gray-500">Rollbacks</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="p-6">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-purple-100 text-purple-600">
                        <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"/>
                            <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"/>
                        </svg>
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold">{{ stats.avg_coverage|floatformat:1 }}%</h3>
                        <p class="text-gray-500">Cobertura Média</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Gráfico de Tendências -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div class="card">
            <div class="p-6">
                <h3 class="text-lg font-semibold mb-4">Tendência de Qualidade</h3>
                <canvas id="qualityTrendChart" width="400" height="200"></canvas>
            </div>
        </div>

        <div class="card">
            <div class="p-6">
                <h3 class="text-lg font-semibold mb-4">Performance por Agente</h3>
                <canvas id="agentPerformanceChart" width="400" height="200"></canvas>
            </div>
        </div>
    </div>

    <!-- Tabela de Entregas Recentes -->
    <div class="card">
        <div class="p-6">
            <h3 class="text-lg font-semibold mb-4">Entregas Recentes</h3>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                    <thead class="bg-gray-50 dark:bg-gray-700">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">
                                Agente
                            </th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">
                                Data
                            </th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">
                                Score
                            </th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">
                                Nota
                            </th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">
                                Status
                            </th>
                            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">
                                Ações
                            </th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                        {% for delivery in recent_deliveries %}
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                {{ delivery.agent_name|title }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                {{ delivery.timestamp|date:"d/m/Y H:i" }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                {{ delivery.overall_score|floatformat:1 }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full
                                    {% if delivery.quality_grade == 'A+' or delivery.quality_grade == 'A' %}
                                        bg-green-100 text-green-800
                                    {% elif delivery.quality_grade == 'B' %}
                                        bg-yellow-100 text-yellow-800
                                    {% elif delivery.quality_grade == 'C' %}
                                        bg-orange-100 text-orange-800
                                    {% else %}
                                        bg-red-100 text-red-800
                                    {% endif %}">
                                    {{ delivery.quality_grade }}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                {% if delivery.overall_score >= 70 %}
                                    <span class="text-green-600">✅ Aprovado</span>
                                {% elif delivery.overall_score >= 50 %}
                                    <span class="text-yellow-600">⚠️ Com Ressalvas</span>
                                {% else %}
                                    <span class="text-red-600">❌ Rejeitado</span>
                                {% endif %}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                <button onclick="viewDeliveryDetails('{{ delivery.task_id }}')" 
                                        class="text-primary-600 hover:text-primary-900">
                                    Ver Detalhes
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// Gráfico de Tendência de Qualidade
const qualityCtx = document.getElementById('qualityTrendChart').getContext('2d');
new Chart(qualityCtx, {
    type: 'line',
    data: {
        labels: {{ trend_labels|safe }},
        datasets: [{
            label: 'Score de Qualidade',
            data: {{ trend_scores|safe }},
            borderColor: 'rgb(59, 130, 246)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 100
            }
        }
    }
});

// Gráfico de Performance por Agente
const agentCtx = document.getElementById('agentPerformanceChart').getContext('2d');
new Chart(agentCtx, {
    type: 'bar',
    data: {
        labels: {{ agent_names|safe }},
        datasets: [{
            label: 'Score Médio',
            data: {{ agent_scores|safe }},
            backgroundColor: [
                'rgba(34, 197, 94, 0.8)',
                'rgba(59, 130, 246, 0.8)',
                'rgba(168, 85, 247, 0.8)',
                'rgba(245, 158, 11, 0.8)'
            ]
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 100
            }
        }
    }
});

function viewDeliveryDetails(taskId) {
    // Implementar modal ou página de detalhes
    console.log('Viewing details for task:', taskId);
}
</script>
{% endblock %}
```

## 📈 Integração com Django Views

**views/quality_views.py:**
```python
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from pathlib import Path
import json
from datetime import datetime, timedelta
from collections import defaultdict

class QualityDashboardView(TemplateView):
    template_name = 'dashboard/quality_metrics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Carregar dados de qualidade
        metrics_data = self.load_quality_metrics()
        
        context.update({
            'stats': self.calculate_stats(metrics_data),
            'recent_deliveries': metrics_data[:10],  # 10 mais recentes
            'trend_labels': json.dumps(self.get_trend_labels()),
            'trend_scores': json.dumps(self.get_trend_scores(metrics_data)),
            'agent_names': json.dumps(self.get_agent_names(metrics_data)),
            'agent_scores': json.dumps(self.get_agent_scores(metrics_data))
        })
        
        return context
    
    def load_quality_metrics(self):
        """Carregar métricas do arquivo JSON"""
        project_root = Path(__file__).parent.parent.parent
        metrics_file = project_root / "metrics" / "quality_history.json"
        
        if not metrics_file.exists():
            return []
        
        try:
            with open(metrics_file, 'r') as f:
                data = json.load(f)
            
            # Converter timestamp strings para datetime para ordenação
            for item in data:
                item['timestamp'] = datetime.fromisoformat(item['timestamp'])
            
            return sorted(data, key=lambda x: x['timestamp'], reverse=True)
        except Exception as e:
            print(f"Erro ao carregar métricas: {e}")
            return []
    
    def calculate_stats(self, metrics_data):
        """Calcular estatísticas gerais"""
        if not metrics_data:
            return {
                'total_deliveries': 0,
                'avg_score': 0,
                'rollbacks_count': 0,
                'avg_coverage': 0
            }
        
        total_deliveries = len(metrics_data)
        avg_score = sum(m['overall_score'] for m in metrics_data) / total_deliveries
        rollbacks_count = len([m for m in metrics_data if m['overall_score'] < 50])
        avg_coverage = sum(m['code_coverage'] for m in metrics_data) / total_deliveries
        
        return {
            'total_deliveries': total_deliveries,
            'avg_score': avg_score,
            'rollbacks_count': rollbacks_count,
            'avg_coverage': avg_coverage
        }
    
    def get_trend_labels(self):
        """Gerar labels para gráfico de tendência (últimos 30 dias)"""
        labels = []
        for i in range(29, -1, -1):
            date = datetime.now() - timedelta(days=i)
            labels.append(date.strftime('%d/%m'))
        return labels
    
    def get_trend_scores(self, metrics_data):
        """Gerar scores para gráfico de tendência"""
        daily_scores = defaultdict(list)
        
        # Agrupar por dia
        for metric in metrics_data:
            date_key = metric['timestamp'].strftime('%d/%m')
            daily_scores[date_key].append(metric['overall_score'])
        
        # Calcular média diária
        trend_scores = []
        for i in range(29, -1, -1):
            date = datetime.now() - timedelta(days=i)
            date_key = date.strftime('%d/%m')
            
            if date_key in daily_scores:
                avg_score = sum(daily_scores[date_key]) / len(daily_scores[date_key])
                trend_scores.append(round(avg_score, 1))
            else:
                trend_scores.append(None)
        
        return trend_scores
    
    def get_agent_names(self, metrics_data):
        """Obter nomes únicos dos agentes"""
        agents = set(m['agent_name'] for m in metrics_data)
        return sorted(list(agents))
    
    def get_agent_scores(self, metrics_data):
        """Calcular score médio por agente"""
        agent_scores = defaultdict(list)
        
        for metric in metrics_data:
            agent_scores[metric['agent_name']].append(metric['overall_score'])
        
        scores = []
        for agent in sorted(agent_scores.keys()):
            avg_score = sum(agent_scores[agent]) / len(agent_scores[agent])
            scores.append(round(avg_score, 1))
        
        return scores

def quality_api_view(request):
    """API endpoint para dados de qualidade em tempo real"""
    if request.method == 'GET':
        view = QualityDashboardView()
        metrics_data = view.load_quality_metrics()
        
        return JsonResponse({
            'stats': view.calculate_stats(metrics_data),
            'recent_deliveries': [
                {
                    'agent_name': m['agent_name'],
                    'timestamp': m['timestamp'].isoformat(),
                    'overall_score': m['overall_score'],
                    'quality_grade': m['quality_grade']
                }
                for m in metrics_data[:5]
            ]
        })
```

## 🎯 Script de Integração Final

**scripts/integrated_workflow.py:**
```python
#!/usr/bin/env python
"""
Script integrado que combina backup, análise de qualidade e rollback automático
"""

import sys
import subprocess
from pathlib import Path
from quality_metrics import QualityAnalyzer, DeliveryValidator
from auto_rollback import AutoRollbackSystem
from backup import BackupManager

class IntegratedWorkflow:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.backup_manager = BackupManager()
        self.rollback_system = AutoRollbackSystem(project_path)
        
    def execute_agent_task(self, agent_name: str, task_description: str) -> bool:
        """Executar workflow completo para uma tarefa de agente"""
        
        print(f"🚀 INICIANDO WORKFLOW INTEGRADO")
        print(f"Agente: {agent_name}")
        print(f"Tarefa: {task_description}")
        print("=" * 60)
        
        # Fase 1: Backup antes da execução
        print("📦 Fase 1: Criando backup pré-execução...")
        backup_path = self.backup_manager.create_backup(f"before_{agent_name}")
        
        # Fase 2: Executar testes básicos pré-entrega
        print("🧪 Fase 2: Executando validações pré-entrega...")
        if not self._run_basic_tests():
            print("❌ Validações básicas falharam - abortando")
            return False
        
        # Fase 3: Análise de qualidade pós-entrega
        print("📊 Fase 3: Analisando qualidade da entrega...")
        quality_passed = self.rollback_system.validate_and_rollback(
            agent_name, task_description
        )
        
        # Fase 4: Resultado final
        if quality_passed:
            print("✅ WORKFLOW CONCLUÍDO COM SUCESSO")
            print("   Entrega aprovada e integrada")
            
            # Cleanup de backups antigos
            self.backup_manager.cleanup_old_backups()
            return True
        else:
            print("❌ WORKFLOW FALHOU")
            print("   Rollback executado - sistema restaurado")
            return False
    
    def _run_basic_tests(self) -> bool:
        """Executar testes básicos antes da análise detalhada"""
        try:
            # Verificar sintaxe Python
            result = subprocess.run([
                str(self.project_path / "venv" / "bin" / "python"), 
                "-m", "py_compile", "."
            ], capture_output=True, cwd=self.project_path)
            
            if result.returncode != 0:
                print("❌ Erros de sintaxe encontrados")
                return False
            
            # Verificar migrations
            result = subprocess.run([
                str(self.project_path / "venv" / "bin" / "python"), 
                "manage.py", "check"
            ], capture_output=True, cwd=self.project_path)
            
            if result.returncode != 0:
                print("❌ Django check falhou")
                return False
            
            print("✅ Validações básicas passaram")
            return True
            
        except Exception as e:
            print(f"❌ Erro nas validações básicas: {e}")
            return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python scripts/integrated_workflow.py <agent_name> <task_description>")
        print("Exemplo: python scripts/integrated_workflow.py backend_agent 'Implementar autenticação de usuário'")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    task_description = " ".join(sys.argv[2:])
    
    project_path = Path(__file__).parent.parent
    workflow = IntegratedWorkflow(project_path)
    
    success = workflow.execute_agent_task(agent_name, task_description)
    
    sys.exit(0 if success else 1)
```

## 📋 Makefile Atualizado com Monitoramento

**Makefile (versão com métricas):**
```makefile
.PHONY: help install dev test security backup clean quality-check agent-task

VENV_PATH = venv/bin
AGENT_NAME ?= backend_agent
TASK_DESC ?= "Tarefa não especificada"

help: ## Mostrar ajuda
	@echo "Sistema de Desenvolvimento Django com Monitoramento de Qualidade"
	@echo "============================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*# 📊 Sistema de Monitoramento e Métricas (monitoring_system.md)

## 🎯 Objetivo

Este documento define um sistema completo de monitoramento de qualidade, métricas de desempenho e rollback automático para o sistema de agentes Django.

## 📈 Métricas de Qualidade

### Sistema de Pontuação de Entrega

**scripts/quality_metrics.py:**
```python
#!/usr/bin/env python
"""
Sistema de métricas de qualidade para entregas de agentes
"""

import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class QualityMetrics:
    """Métricas de qualidade de uma entrega"""
    agent_name: str
    task_id: str
    timestamp: str
    
    # Métricas de código
    code_coverage: float = 0.0
    test_pass_rate: float = 0.0
    cyclomatic_complexity: float = 0.0
    code_duplication: float = 0.0
    
    # Métricas de segurança
    security_issues: int = 0
    security_score: float = 100.0
    
    # Métricas de performance
    build_time: float = 0.0
    test_execution_time: float = 0.0
    
    # Métricas de conformidade
    style_violations: int = 0
    documentation_score: float = 0.0
    
    # Score final
    overall_score: float = 0.0
    quality_grade: str = "F"

class QualityAnalyzer:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.venv_python = project_path / "venv" / "bin" / "python"
        self.metrics_file = project_path / "metrics" / "quality_history.json"
        self.metrics_file.parent.mkdir(exist_ok=True)
    
    def analyze_delivery(self, agent_name: str, task_description: str) -> QualityMetrics:
        """Analisar qualidade de uma entrega"""
        task_id = f"{agent_name}_{int(time.time())}"
        
        print(f"🔍 Analisando entrega: {agent_name} - {task_description}")
        
        metrics = QualityMetrics(
            agent_name=agent_name,
            task_id=task_id,
            timestamp=datetime.now().isoformat()
        )
        
        # Executar análises
        metrics.code_coverage = self._analyze_test_coverage()
        metrics.test_pass_rate = self._analyze_test_results()
        metrics.cyclomatic_complexity = self._analyze_complexity()
        metrics.security_issues, metrics.security_score = self._analyze_security()
        metrics.build_time = self._measure_build_time()
        metrics.style_violations = self._analyze_code_style()
        metrics.documentation_score = self._analyze_documentation()
        
        # Calcular score final
        metrics.overall_score = self._calculate_overall_score(metrics)
        metrics.quality_grade = self._get_quality_grade(metrics.overall_score)
        
        # Salvar métricas
        self._save_metrics(metrics)
        
        # Relatório
        self._print_quality_report(metrics)
        
        return metrics
    
    def _analyze_test_coverage(self) -> float:
        """Analisar cobertura de testes"""
        try:
            result = subprocess.run([
                str(self.venv_python), "-m", "pytest", 
                "--cov=.", "--cov-report=json", "--quiet"
            ], capture_output=True, text=True, cwd=self.project_path)
            
            coverage_file = self.project_path / "coverage.json"
            if coverage_file.exists():
                with open(coverage_file) as f:
                    coverage_data = json.load(f)
                return coverage_data.get("totals", {}).get("percent_covered", 0.0)
        except Exception as e:
            print(f"⚠️ Erro na análise de cobertura: {e}")
        
        return 0.0
    
    def _analyze_test_results(self) -> float:
        """Analisar taxa de sucesso dos testes"""
        try:
            result = subprocess.run([
                str(self.venv_python), "-m", "pytest", 
                "--tb=no", "--quiet"
            ], capture_output=True, text=True, cwd=self.project_path)
            
            output = result.stdout
            if "passed" in output and "failed" in output:
                # Parse da saída do pytest
                lines = output.split('\n')
                for line in lines:
                    if "passed" in line and ("failed" in line or "error" in line):
                        # Extrair números
                        words = line.split()
                        passed = failed = 0
                        
                        for i, word in enumerate(words):
                            if word == "passed":
                                passed = int(words[i-1])
                            elif wor $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $1, $2}'

install: ## Instalar dependências
	$(VENV_PATH)/pip install --upgrade pip
	$(VENV_PATH)/pip-sync requirements-dev.txt

security: ## Executar verificações de segurança
	$(VENV_PATH)/python scripts/security_check.py
	$(VENV_PATH)/python manage.py check --deploy

quality-check: ## Executar análise de qualidade completa
	$(VENV_PATH)/python scripts/quality_metrics.py $(AGENT_NAME) $(TASK_DESC)

agent-task: ## Executar tarefa de agente com workflow completo
	$(VENV_PATH)/python scripts/integrated_workflow.py $(AGENT_NAME) $(TASK_DESC)

backup: ## Criar backup manual
	$(VENV_PATH)/python scripts/backup.py create manual_backup

rollback: ## Executar rollback se necessário
	$(VENV_PATH)/python scripts/auto_rollback.py $(AGENT_NAME) $(TASK_DESC)

metrics-dashboard: ## Iniciar dashboard de métricas
	$(VENV_PATH)/python manage.py runserver --settings=config.settings

test: ## Executar testes com cobertura
	$(VENV_PATH)/python -m pytest --cov=. --cov-report=html --cov-report=term

dev: security ## Iniciar desenvolvimento
	$(VENV_PATH)/python manage.py migrate
	$(VENV_PATH)/python manage.py runserver

# Exemplos de uso com agentes específicos
backend-task: ## Executar tarefa do agente backend
	@make agent-task AGENT_NAME=backend_agent TASK_DESC="$(TASK_DESC)"

frontend-task: ## Executar tarefa do agente frontend
	@make agent-task AGENT_NAME=frontend_agent TASK_DESC="$(TASK_DESC)"

test-task: ## Executar tarefa do agente de testes
	@make agent-task AGENT_NAME=test_agent TASK_DESC="$(TASK_DESC)"

clean: ## Limpar arquivos temporários
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/ htmlcov/ .coverage

monitor: security quality-check ## Executar monitoramento completo
	@echo "✅ Sistema monitorado e validado!"
```

## 🎯 Resumo do Sistema

Este sistema de monitoramento oferece:

1. **Métricas Abrangentes**: Cobertura, testes, segurança, complexidade, estilo
2. **Validação Automática**: Critérios mínimos configuráveis  
3. **Rollback Inteligente**: Baseado em métricas de qualidade
4. **Dashboard Visual**: Acompanhamento de tendências
5. **Backup Automático**: Proteção contra falhas
6. **Workflow Integrado**: Processo completo do início ao fim

### Comandos Principais:

```bash
# Executar tarefa completa com monitoramento
make agent-task AGENT_NAME=backend_agent TASK_DESC="Implementar API de usuários"

# Verificar qualidade de uma entrega específica
make quality-check AGENT_NAME=frontend_agent TASK_DESC="Criar dashboard"

# Executar monitoramento completo
make monitor

# Ver dashboard de métricas
make metrics-dashboard
```

O sistema garante qualidade consistente e oferece mecanismos de recuperação automática, mantendo o projeto sempre em estado funcional.# 📊 Sistema de Monitoramento e Métricas (monitoring_system.md)

## 🎯 Objetivo

Este documento define um sistema completo de monitoramento de qualidade, métricas de desempenho e rollback automático para o sistema de agentes Django.

## 📈 Métricas de Qualidade

### Sistema de Pontuação de Entrega

**scripts/quality_metrics.py:**
```python
#!/usr/bin/env python
"""
Sistema de métricas de qualidade para entregas de agentes
"""

import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class QualityMetrics:
    """Métricas de qualidade de uma entrega"""
    agent_name: str
    task_id: str
    timestamp: str
    
    # Métricas de código
    code_coverage: float = 0.0
    test_pass_rate: float = 0.0
    cyclomatic_complexity: float = 0.0
    code_duplication: float = 0.0
    
    # Métricas de segurança
    security_issues: int = 0
    security_score: float = 100.0
    
    # Métricas de performance
    build_time: float = 0.0
    test_execution_time: float = 0.0
    
    # Métricas de conformidade
    style_violations: int = 0
    documentation_score: float = 0.0
    
    # Score final
    overall_score: float = 0.0
    quality_grade: str = "F"

class QualityAnalyzer:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.venv_python = project_path / "venv" / "bin" / "python"
        self.metrics_file = project_path / "metrics" / "quality_history.json"
        self.metrics_file.parent.mkdir(exist_ok=True)
    
    def analyze_delivery(self, agent_name: str, task_description: str) -> QualityMetrics:
        """Analisar qualidade de uma entrega"""
        task_id = f"{agent_name}_{int(time.time())}"
        
        print(f"🔍 Analisando entrega: {agent_name} - {task_description}")
        
        metrics = QualityMetrics(
            agent_name=agent_name,
            task_id=task_id,
            timestamp=datetime.now().isoformat()
        )
        
        # Executar análises
        metrics.code_coverage = self._analyze_test_coverage()
        metrics.test_pass_rate = self._analyze_test_results()
        metrics.cyclomatic_complexity = self._analyze_complexity()
        metrics.security_issues, metrics.security_score = self._analyze_security()
        metrics.build_time = self._measure_build_time()
        metrics.style_violations = self._analyze_code_style()
        metrics.documentation_score = self._analyze_documentation()
        
        # Calcular score final
        metrics.overall_score = self._calculate_overall_score(metrics)
        metrics.quality_grade = self._get_quality_grade(metrics.overall_score)
        
        # Salvar métricas
        self._save_metrics(metrics)
        
        # Relatório
        self._print_quality_report(metrics)
        
        return metrics
    
    def _analyze_test_coverage(self) -> float:
        """Analisar cobertura de testes"""
        try:
            result = subprocess.run([
                str(self.venv_python), "-m", "pytest", 
                "--cov=.", "--cov-report=json", "--quiet"
            ], capture_output=True, text=True, cwd=self.project_path)
            
            coverage_file = self.project_path / "coverage.json"
            if coverage_file.exists():
                with open(coverage_file) as f:
                    coverage_data = json.load(f)
                return coverage_data.get("totals", {}).get("percent_covered", 0.0)
        except Exception as e:
            print(f"⚠️ Erro na análise de cobertura: {e}")
        
        return 0.0
    
    def _analyze_test_results(self) -> float:
        """Analisar taxa de sucesso dos testes"""
        try:
            result = subprocess.run([
                str(self.venv_python), "-m", "pytest", 
                "--tb=no", "--quiet"
            ], capture_output=True, text=True, cwd=self.project_path)
            
            output = result.stdout
            if "passed" in output and "failed" in output:
                # Parse da saída do pytest
                lines = output.split('\n')
                for line in lines:
                    if "passed" in line and ("failed" in line or "error" in line):
                        # Extrair números
                        words = line.split()
                        passed = failed = 0
                        
                        for i, word in enumerate(words):
                            if word == "passed":
                                passed = int(words[i-1])
                            elif wor