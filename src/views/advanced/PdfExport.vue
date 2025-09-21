<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Exportação para PDF</h1>
      <Button variant="primary" @click="togglePdfExport">
        <Icon :name="pdfExportEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ pdfExportEnabled ? 'Desativar' : 'Ativar' }} Exportação PDF
      </Button>
    </div>
    
    <!-- Configurações da exportação PDF -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações da Exportação PDF</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Orientação</label>
          <Select 
            v-model="pdfSettings.orientation" 
            :options="orientationOptions" 
            placeholder="Selecione a orientação" 
            @change="updatePdfSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Formato</label>
          <Select 
            v-model="pdfSettings.format" 
            :options="formatOptions" 
            placeholder="Selecione o formato" 
            @change="updatePdfSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Margens</label>
          <Select 
            v-model="pdfSettings.margins" 
            :options="marginOptions" 
            placeholder="Selecione as margens" 
            @change="updatePdfSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Exemplo de exportação PDF -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Exemplo de Exportação PDF</h2>
          <Badge :variant="pdfExportEnabled ? 'success' : 'default'">
            {{ pdfExportEnabled ? 'Ativada' : 'Desativada' }}
          </Badge>
        </div>
      </template>
      
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Dados de Exemplo</h3>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unidade</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="item in sampleData" :key="item.id" class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.name }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.category }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.quantity }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.unit }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Visualização do PDF</h3>
            <div class="border border-dashed border-gray-300 rounded h-64 flex items-center justify-center">
              <div v-if="pdfPreview" class="text-center">
                <Icon name="file-pdf" class="mx-auto h-12 w-12 text-red-500" />
                <p class="mt-2 text-sm text-gray-500">Visualização do PDF gerado</p>
                <Button variant="outline" size="sm" class="mt-4" @click="downloadPdf">
                  <Icon name="download" class="mr-2" />
                  Download PDF
                </Button>
              </div>
              <div v-else class="text-center">
                <Icon name="file" class="mx-auto h-12 w-12 text-gray-400" />
                <p class="mt-2 text-sm text-gray-500">Nenhum PDF gerado ainda</p>
                <Button 
                  variant="primary" 
                  size="sm" 
                  class="mt-4" 
                  @click="generatePdf" 
                  :disabled="!pdfExportEnabled"
                >
                  <Icon name="file-pdf" class="mr-2" />
                  Gerar PDF
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Opções de exportação avançadas -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Opções de Exportação Avançadas</h2>
      </template>
      
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Personalização do Cabeçalho</h3>
            <div class="space-y-4">
              <Input 
                v-model="pdfSettings.headerTitle" 
                placeholder="Título do relatório" 
                @input="updatePdfSettings"
              />
              <Input 
                v-model="pdfSettings.headerSubtitle" 
                placeholder="Subtítulo do relatório" 
                @input="updatePdfSettings"
              />
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Logo</label>
                <div class="flex items-center">
                  <div class="border border-dashed border-gray-300 rounded w-16 h-16 flex items-center justify-center">
                    <Icon v-if="!pdfSettings.logo" name="image" class="text-gray-400" />
                    <img v-else :src="pdfSettings.logo" alt="Logo" class="w-full h-full object-contain" />
                  </div>
                  <Button variant="outline" size="sm" class="ml-4">
                    <Icon name="upload" class="mr-2" />
                    Carregar Logo
                  </Button>
                </div>
              </div>
            </div>
          </div>
          
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Personalização do Rodapé</h3>
            <div class="space-y-4">
              <Input 
                v-model="pdfSettings.footerText" 
                placeholder="Texto do rodapé" 
                @input="updatePdfSettings"
              />
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Número de Página</label>
                <Toggle 
                  v-model="pdfSettings.showPageNumbers" 
                  label="Mostrar números de página" 
                  @change="updatePdfSettings"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Data de Geração</label>
                <Toggle 
                  v-model="pdfSettings.showGenerationDate" 
                  label="Mostrar data de geração do PDF" 
                  @change="updatePdfSettings"
                />
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-6 flex justify-end space-x-3">
          <Button variant="outline" @click="resetPdfSettings">
            <Icon name="undo" class="mr-2" />
            Restaurar Padrões
          </Button>
          <Button 
            variant="primary" 
            @click="exportToPdf" 
            :disabled="!pdfExportEnabled"
          >
            <Icon name="file-export" class="mr-2" />
            Exportar para PDF
          </Button>
        </div>
      </div>
    </Card>
    
    <!-- Informações sobre exportação PDF -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações sobre Exportação PDF</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Benefícios da Exportação PDF</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Permite impressão de alta qualidade de relatórios</li>
              <li>Mantém a formatação consistente em diferentes dispositivos</li>
              <li>Facilita o compartilhamento de documentos profissionais</li>
              <li>Pode incluir elementos gráficos e visuais complexos</li>
              <li>Permite adicionar marca d'água e proteção de documentos</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Exportação PDF:</span>
                <span>{{ pdfExportEnabled ? 'Ativada' : 'Desativada' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Orientação:</span>
                <span>{{ pdfSettings.orientation }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Formato:</span>
                <span>{{ pdfSettings.format }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Margens:</span>
                <span>{{ pdfSettings.margins }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Título do Cabeçalho:</span>
                <span>{{ pdfSettings.headerTitle || 'Não definido' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Subtítulo do Cabeçalho:</span>
                <span>{{ pdfSettings.headerSubtitle || 'Não definido' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Texto do Rodapé:</span>
                <span>{{ pdfSettings.footerText || 'Não definido' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Mostrar Números de Página:</span>
                <span>{{ pdfSettings.showPageNumbers ? 'Sim' : 'Não' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Mostrar Data de Geração:</span>
                <span>{{ pdfSettings.showGenerationDate ? 'Sim' : 'Não' }}</span>
              </li>
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
  name: 'PdfExport',
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
    const pdfExportEnabled = ref(true)
    const pdfPreview = ref(false)
    
    // Configurações da exportação PDF
    const pdfSettings = ref({
      orientation: 'portrait',
      format: 'A4',
      margins: 'normal',
      headerTitle: 'Relatório de Estoque',
      headerSubtitle: 'Laboratório de Química',
      logo: '',
      footerText: 'Documento gerado automaticamente pelo Sistema de Controle de Estoque',
      showPageNumbers: true,
      showGenerationDate: true
    })
    
    // Dados fictícios para demonstração
    const sampleData = ref([
      {
        id: 1,
        name: 'Ácido Clorídrico',
        category: 'Ácidos',
        quantity: 25,
        unit: 'Litro'
      },
      {
        id: 2,
        name: 'Etanol 96%',
        category: 'Álcoois',
        quantity: 10,
        unit: 'Litro'
      },
      {
        id: 3,
        name: 'Sulfato de Cobre',
        category: 'Sais',
        quantity: 5,
        unit: 'Kilograma'
      },
      {
        id: 4,
        name: 'Ácido Nítrico',
        category: 'Ácidos',
        quantity: 15,
        unit: 'Litro'
      },
      {
        id: 5,
        name: 'Hidróxido de Sódio',
        category: 'Bases',
        quantity: 8,
        unit: 'Kilograma'
      }
    ])
    
    // Opções para seletores
    const orientationOptions = ref([
      { value: 'portrait', label: 'Retrato' },
      { value: 'landscape', label: 'Paisagem' }
    ])
    
    const formatOptions = ref([
      { value: 'A4', label: 'A4' },
      { value: 'A3', label: 'A3' },
      { value: 'Letter', label: 'Carta (Letter)' },
      { value: 'Legal', label: 'Ofício (Legal)' }
    ])
    
    const marginOptions = ref([
      { value: 'none', label: 'Nenhuma' },
      { value: 'small', label: 'Pequena' },
      { value: 'normal', label: 'Normal' },
      { value: 'large', label: 'Grande' }
    ])
    
    // Métodos
    const togglePdfExport = () => {
      pdfExportEnabled.value = !pdfExportEnabled.value
    }
    
    const updatePdfSettings = () => {
      // Atualizar configurações da exportação PDF
      console.log('Atualizando configurações da exportação PDF:', pdfSettings.value)
    }
    
    const resetPdfSettings = () => {
      pdfSettings.value = {
        orientation: 'portrait',
        format: 'A4',
        margins: 'normal',
        headerTitle: 'Relatório de Estoque',
        headerSubtitle: 'Laboratório de Química',
        logo: '',
        footerText: 'Documento gerado automaticamente pelo Sistema de Controle de Estoque',
        showPageNumbers: true,
        showGenerationDate: true
      }
    }
    
    const generatePdf = () => {
      if (!pdfExportEnabled.value) return
      
      // Simular geração de PDF
      console.log('Gerando PDF com as configurações:', pdfSettings.value)
      pdfPreview.value = true
    }
    
    const downloadPdf = () => {
      if (!pdfPreview.value || !pdfExportEnabled.value) return
      
      // Simular download do PDF
      console.log('Baixando PDF...')
    }
    
    const exportToPdf = () => {
      if (!pdfExportEnabled.value) return
      
      // Lógica para exportar dados para PDF
      console.log('Exportando dados para PDF:', {
        settings: pdfSettings.value,
        data: sampleData.value
      })
      
      // Para fins de demonstração, vamos gerar o PDF
      generatePdf()
    }
    
    return {
      pdfExportEnabled,
      pdfPreview,
      pdfSettings,
      sampleData,
      orientationOptions,
      formatOptions,
      marginOptions,
      togglePdfExport,
      updatePdfSettings,
      resetPdfSettings,
      generatePdf,
      downloadPdf,
      exportToPdf
    }
  }
}
</script>