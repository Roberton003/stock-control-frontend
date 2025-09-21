<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Templates de Relatório Personalizáveis</h1>
      <Button variant="primary" @click="toggleReportTemplates">
        <Icon :name="reportTemplatesEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ reportTemplatesEnabled ? 'Desativar' : 'Ativar' }} Templates de Relatório
      </Button>
    </div>
    
    <!-- Configurações dos templates de relatório -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações dos Templates de Relatório</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Template Padrão</label>
          <Select 
            v-model="templateSettings.defaultTemplate" 
            :options="templateOptions" 
            placeholder="Selecione um template" 
            @change="updateTemplateSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Formato de Saída</label>
          <Select 
            v-model="templateSettings.outputFormat" 
            :options="outputFormatOptions" 
            placeholder="Selecione um formato" 
            @change="updateTemplateSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Incluir Logotipo</label>
          <Toggle 
            v-model="templateSettings.includeLogo" 
            label="Adicionar logotipo ao relatório" 
            @change="updateTemplateSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Exemplo de template de relatório -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Exemplo de Template de Relatório</h2>
          <Badge :variant="reportTemplatesEnabled ? 'success' : 'default'">
            {{ reportTemplatesEnabled ? 'Ativado' : 'Desativado' }}
          </Badge>
        </div>
      </template>
      
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Editor de Template</h3>
            <div class="border border-gray-300 rounded-md p-4 bg-gray-50">
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Título do Relatório</label>
                <Input 
                  v-model="templateEditor.title" 
                  placeholder="Digite o título do relatório" 
                  @input="updateTemplateEditor"
                />
              </div>
              
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Cabeçalho</label>
                <textarea 
                  v-model="templateEditor.header" 
                  rows="3" 
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                  placeholder="Digite o cabeçalho do relatório"
                  @input="updateTemplateEditor"
                ></textarea>
              </div>
              
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Corpo</label>
                <textarea 
                  v-model="templateEditor.body" 
                  rows="5" 
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                  placeholder="Digite o corpo do relatório usando variáveis como {{data}}, {{nome}}, etc."
                  @input="updateTemplateEditor"
                ></textarea>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Rodapé</label>
                <textarea 
                  v-model="templateEditor.footer" 
                  rows="2" 
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                  placeholder="Digite o rodapé do relatório"
                  @input="updateTemplateEditor"
                ></textarea>
              </div>
            </div>
          </div>
          
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Visualização do Relatório</h3>
            <div class="border border-gray-300 rounded-md p-4 bg-white">
              <div v-if="templatePreview" class="prose max-w-none">
                <h1 class="text-xl font-bold text-center mb-4">{{ templateEditor.title }}</h1>
                
                <div v-if="templateEditor.header" class="border-b border-gray-200 pb-2 mb-4">
                  <p class="text-sm text-gray-700">{{ templateEditor.header }}</p>
                </div>
                
                <div v-if="templateEditor.body" class="mb-4">
                  <p class="text-gray-700">{{ templateEditor.body }}</p>
                </div>
                
                <div v-if="templateEditor.footer" class="border-t border-gray-200 pt-2 mt-4">
                  <p class="text-xs text-gray-500">{{ templateEditor.footer }}</p>
                </div>
              </div>
              <div v-else class="text-center py-8">
                <Icon name="file-alt" class="mx-auto h-12 w-12 text-gray-400" />
                <h3 class="mt-2 text-lg font-medium text-gray-900">Nenhum template carregado</h3>
                <p class="mt-1 text-sm text-gray-500">Crie ou selecione um template para visualizar o relatório.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button variant="outline" @click="resetTemplateEditor">
            <Icon name="undo" class="mr-2" />
            Resetar
          </Button>
          <Button variant="primary" @click="saveTemplate">
            <Icon name="save" class="mr-2" />
            Salvar Template
          </Button>
        </div>
      </template>
    </Card>
    
    <!-- Lista de templates salvos -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Templates Salvos</h2>
          <Button variant="outline" @click="createNewTemplate">
            <Icon name="plus" class="mr-2" />
            Novo Template
          </Button>
        </div>
      </template>
      
      <div class="overflow-x-auto p-4">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Formato</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data de Criação</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Última Modificação</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="template in savedTemplates" :key="template.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ template.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ template.format }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(template.createdAt) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(template.updatedAt) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <Button variant="secondary" size="sm" class="mr-2" @click="loadTemplate(template.id)">
                  <Icon name="eye" />
                </Button>
                <Button variant="outline" size="sm" class="mr-2" @click="editTemplate(template.id)">
                  <Icon name="edit" />
                </Button>
                <Button variant="outline" size="sm" @click="deleteTemplate(template.id)">
                  <Icon name="trash" />
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Paginação -->
      <div class="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
        <div class="text-sm text-gray-700">
          Mostrando <span class="font-medium">1</span> a <span class="font-medium">{{ savedTemplates.length }}</span> de <span class="font-medium">{{ savedTemplates.length }}</span> templates
        </div>
        <div class="flex space-x-2">
          <Button variant="outline" size="sm" disabled>Anterior</Button>
          <Button variant="outline" size="sm" disabled>Próximo</Button>
        </div>
      </div>
    </Card>
    
    <!-- Variáveis disponíveis -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Variáveis Disponíveis</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Dados do Relatório</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li><code>{{titulo}}</code> - Título do relatório</li>
              <li><code>{{data}}</code> - Data de geração do relatório</li>
              <li><code>{{usuario}}</code> - Nome do usuário que gerou o relatório</li>
              <li><code>{{periodo}}</code> - Período de referência do relatório</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Dados de Estoque</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li><code>{{estoque_total}}</code> - Valor total em estoque</li>
              <li><code>{{itens_baixos}}</code> - Número de itens abaixo do mínimo</li>
              <li><code>{{lotes_vencendo}}</code> - Número de lotes próximos ao vencimento</li>
              <li><code>{{movimentacoes}}</code> - Número de movimentações no período</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Dados de Reagentes</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li><code>{{reagente_nome}}</code> - Nome do reagente</li>
              <li><code>{{reagente_categoria}}</code> - Categoria do reagente</li>
              <li><code>{{reagente_quantidade}}</code> - Quantidade em estoque</li>
              <li><code>{{reagente_unidade}}</code> - Unidade de medida</li>
            </ul>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select from '@/components/ui/Select.vue'
import Toggle from '@/components/ui/Toggle.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'ReportTemplates',
  components: {
    Card,
    Button,
    Input,
    Select,
    Toggle,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const reportTemplatesEnabled = ref(true)
    const templatePreview = ref(false)
    
    // Configurações dos templates de relatório
    const templateSettings = ref({
      defaultTemplate: 'default',
      outputFormat: 'pdf',
      includeLogo: true
    })
    
    // Editor de template
    const templateEditor = ref({
      title: 'Relatório de Estoque',
      header: 'Laboratório de Química\nRelatório de Estoque - Período de Referência',
      body: 'Este relatório apresenta o status atual do estoque de reagentes do laboratório.\n\nValores totais:\n- Estoque total: {{estoque_total}}\n- Itens abaixo do mínimo: {{itens_baixos}}\n- Lotes próximos ao vencimento: {{lotes_vencendo}}\n- Movimentações no período: {{movimentacoes}}',
      footer: 'Documento gerado automaticamente pelo Sistema de Controle de Estoque\nData de geração: {{data}}'
    })
    
    // Templates salvos
    const savedTemplates = ref([
      {
        id: 1,
        name: 'Relatório Padrão',
        format: 'PDF',
        createdAt: '2023-09-15T14:30:00',
        updatedAt: '2023-09-15T14:30:00'
      },
      {
        id: 2,
        name: 'Relatório Resumido',
        format: 'Excel',
        createdAt: '2023-09-10T09:15:00',
        updatedAt: '2023-09-12T11:45:00'
      },
      {
        id: 3,
        name: 'Relatório Detalhado',
        format: 'PDF',
        createdAt: '2023-09-05T16:20:00',
        updatedAt: '2023-09-05T16:20:00'
      }
    ])
    
    // Opções para seletores
    const templateOptions = ref([
      { value: 'default', label: 'Padrão' },
      { value: 'summary', label: 'Resumido' },
      { value: 'detailed', label: 'Detalhado' },
      { value: 'custom', label: 'Personalizado' }
    ])
    
    const outputFormatOptions = ref([
      { value: 'pdf', label: 'PDF' },
      { value: 'excel', label: 'Excel' },
      { value: 'csv', label: 'CSV' },
      { value: 'html', label: 'HTML' }
    ])
    
    // Métodos
    const toggleReportTemplates = () => {
      reportTemplatesEnabled.value = !reportTemplatesEnabled.value
    }
    
    const updateTemplateSettings = () => {
      // Atualizar configurações dos templates de relatório
      console.log('Atualizando configurações dos templates de relatório:', templateSettings.value)
    }
    
    const updateTemplateEditor = () => {
      // Atualizar editor de template
      console.log('Atualizando editor de template:', templateEditor.value)
      templatePreview.value = true
    }
    
    const resetTemplateEditor = () => {
      templateEditor.value = {
        title: 'Relatório de Estoque',
        header: 'Laboratório de Química\nRelatório de Estoque - Período de Referência',
        body: 'Este relatório apresenta o status atual do estoque de reagentes do laboratório.\n\nValores totais:\n- Estoque total: {{estoque_total}}\n- Itens abaixo do mínimo: {{itens_baixos}}\n- Lotes próximos ao vencimento: {{lotes_vencendo}}\n- Movimentações no período: {{movimentacoes}}',
        footer: 'Documento gerado automaticamente pelo Sistema de Controle de Estoque\nData de geração: {{data}}'
      }
      templatePreview.value = false
    }
    
    const saveTemplate = () => {
      if (!reportTemplatesEnabled.value) return
      
      // Lógica para salvar o template
      console.log('Salvando template:', templateEditor.value)
    }
    
    const createNewTemplate = () => {
      if (!reportTemplatesEnabled.value) return
      
      // Resetar o editor para criar um novo template
      resetTemplateEditor()
      console.log('Criando novo template')
    }
    
    const loadTemplate = (id) => {
      if (!reportTemplatesEnabled.value) return
      
      // Lógica para carregar um template salvo
      const template = savedTemplates.value.find(t => t.id === id)
      if (template) {
      