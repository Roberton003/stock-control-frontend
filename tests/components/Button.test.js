import { mount } from '@vue/test-utils'
import Button from '../../src/components/ui/Button.vue'

describe('Button.vue', () => {
  it('renders with correct text', () => {
    const wrapper = mount(Button, {
      props: {
        text: 'Click me'
      }
    })
    expect(wrapper.text()).toContain('Click me')
  })

  it('emits click event when clicked', async () => {
    const wrapper = mount(Button, {
      props: {
        text: 'Click me'
      }
    })
    
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })

  it('has correct CSS classes for primary variant', () => {
    const wrapper = mount(Button, {
      props: {
        text: 'Click me',
        variant: 'primary'
      }
    })
    
    const button = wrapper.find('button')
    expect(button.classes()).toContain('bg-primary')
  })

  it('has correct CSS classes for secondary variant', () => {
    const wrapper = mount(Button, {
      props: {
        text: 'Click me',
        variant: 'secondary'
      }
    })
    
    const button = wrapper.find('button')
    expect(button.classes()).toContain('bg-secondary')
  })

  it('is disabled when disabled prop is true', () => {
    const wrapper = mount(Button, {
      props: {
        text: 'Click me',
        disabled: true
      }
    })
    
    const button = wrapper.find('button')
    expect(button.attributes('disabled')).toBeDefined()
  })
})