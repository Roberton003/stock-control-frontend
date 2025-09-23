import { mount } from '@vue/test-utils'
import AppHeader from '../../src/components/layout/AppHeader.vue'

describe('AppHeader.vue', () => {
  it('renders the header with correct title', () => {
    const wrapper = mount(AppHeader)
    expect(wrapper.text()).toContain('Stock Control Lab')
  })

  it('contains navigation links', () => {
    const wrapper = mount(AppHeader)
    const navLinks = wrapper.findAll('nav ul li a')
    expect(navLinks.length).toBeGreaterThan(0)
  })
})