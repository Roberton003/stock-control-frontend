import { mount } from '@vue/test-utils'
import Table from '../../src/components/ui/Table.vue'

describe('Table.vue', () => {
  const sampleHeaders = ['Name', 'Category', 'Quantity']
  const sampleData = [
    { id: 1, name: 'Reagent A', category: 'Acids', quantity: 10 },
    { id: 2, name: 'Reagent B', category: 'Bases', quantity: 5 }
  ]

  it('renders headers correctly', () => {
    const wrapper = mount(Table, {
      props: {
        headers: sampleHeaders,
        data: sampleData
      }
    })
    
    sampleHeaders.forEach(header => {
      expect(wrapper.text()).toContain(header)
    })
  })

  it('renders data rows correctly', () => {
    const wrapper = mount(Table, {
      props: {
        headers: sampleHeaders,
        data: sampleData
      }
    })
    
    sampleData.forEach(row => {
      expect(wrapper.text()).toContain(row.name)
      expect(wrapper.text()).toContain(row.category)
      expect(wrapper.text()).toContain(String(row.quantity))
    })
  })

  it('renders empty state when no data is provided', () => {
    const wrapper = mount(Table, {
      props: {
        headers: sampleHeaders,
        data: []
      }
    })
    
    expect(wrapper.text()).toContain('No data available')
  })

  it('emits row-click event when a row is clicked', async () => {
    const wrapper = mount(Table, {
      props: {
        headers: sampleHeaders,
        data: sampleData
      }
    })
    
    const firstRow = wrapper.findAll('tbody tr')[0]
    await firstRow.trigger('click')
    
    expect(wrapper.emitted('row-click')).toBeTruthy()
    expect(wrapper.emitted('row-click')[0][0]).toEqual(sampleData[0])
  })

  it('shows loading state when loading prop is true', () => {
    const wrapper = mount(Table, {
      props: {
        headers: sampleHeaders,
        data: sampleData,
        loading: true
      }
    })
    
    expect(wrapper.findComponent({ name: 'Spinner' }).exists()).toBe(true)
  })
})