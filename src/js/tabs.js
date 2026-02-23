// ============================================================================
// Re:Scale Tabs
// ============================================================================
// Usage:
//   import { RsTabs } from './tabs.js';
//   new RsTabs(document.querySelector('.rs-tabs'), (index) => {
//     console.log('Tab switched to', index);
//   });
// ============================================================================

export class RsTabs {
  constructor(el, onChange) {
    this.el = el;
    this.tabs = Array.from(el.querySelectorAll('.rs-tabs__tab'));
    this.onChange = onChange || (() => {});

    this.tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => this.select(i));
      tab.addEventListener('keydown', (e) => this._onKeydown(e, i));
    });
  }

  select(index) {
    this.tabs.forEach((tab, i) => {
      const selected = i === index;
      tab.setAttribute('aria-selected', selected ? 'true' : 'false');
      tab.setAttribute('tabindex', selected ? '0' : '-1');
    });

    this.onChange(index);
  }

  _onKeydown(e, currentIndex) {
    let next = null;

    switch (e.key) {
      case 'ArrowRight':
      case 'ArrowDown':
        next = (currentIndex + 1) % this.tabs.length;
        break;
      case 'ArrowLeft':
      case 'ArrowUp':
        next = (currentIndex - 1 + this.tabs.length) % this.tabs.length;
        break;
      case 'Home':
        next = 0;
        break;
      case 'End':
        next = this.tabs.length - 1;
        break;
      default:
        return;
    }

    e.preventDefault();
    this.select(next);
    this.tabs[next].focus();
  }
}
