import { mount } from '@vue/test-utils'
import Input from '../../src/components/ui/Input.vue'

describe('Input.vue', () => {
  it('renders with correct label', () => {
    const wrapper = mount(Input, {
      props: {
        label: 'Username',
        modelValue: ''
      }
    })
    expect(wrapper.find('label').text()).toBe('Username')
  })

  it('renders with correct placeholder', () => {
    const wrapper = mount(Input, {
      props: {
        placeholder: 'Enter your username',
        modelValue: ''
      }
    })
    const input = wrapper.find('input')
    expect(input.attributes('placeholder')).toBe('Enter your username')
  })

  it('emits update:modelValue event when input changes', async () => {
    const wrapper = mount(Input, {
      props: {
        modelValue: ''
      }
    })
    
    const input = wrapper.find('input')
    await input.setValue('test value')
    
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['test value'])
  })

  it('shows error message when error prop is provided', () => {
    const wrapper = mount(Input, {
      props: {
        modelValue: '',
        error: 'This field is required'
      }
    })
    
    expect(wrapper.text()).toContain('This field is required')
    const input = wrapper.find('input')
    expect(input.classes()).toContain('border-red-500')
  })

  it('has correct type attribute', () => {
    const wrapper = mount(Input, {
      props: {
        type: 'password',
        modelValue: ''
      }
    })
    
    const input = wrapper.find('input')
    expect(input.attributes('type')).toBe('password')
  })
})