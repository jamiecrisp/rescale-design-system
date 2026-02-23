// ============================================================================
// Re:Scale Modal
// ============================================================================
// Usage:
//   import { RsModal } from './modal.js';
//   const modal = new RsModal(document.querySelector('.rs-modal'));
//   modal.open();
//   modal.close();
// ============================================================================

export class RsModal {
  constructor(el) {
    this.el = el;
    this.dialog = el.querySelector('.rs-modal__dialog');
    this.closeBtn = el.querySelector('.rs-modal__close');
    this._previouslyFocused = null;

    this._onKeydown = this._onKeydown.bind(this);
    this._onBackdropClick = this._onBackdropClick.bind(this);

    if (this.closeBtn) {
      this.closeBtn.addEventListener('click', () => this.close());
    }
  }

  open() {
    this._previouslyFocused = document.activeElement;
    this.el.removeAttribute('hidden');
    document.addEventListener('keydown', this._onKeydown);
    this.el.addEventListener('click', this._onBackdropClick);
    document.body.style.overflow = 'hidden';

    // Focus first focusable element in dialog
    const focusable = this._getFocusable();
    if (focusable.length) focusable[0].focus();
  }

  close() {
    this.el.setAttribute('hidden', '');
    document.removeEventListener('keydown', this._onKeydown);
    this.el.removeEventListener('click', this._onBackdropClick);
    document.body.style.overflow = '';

    if (this._previouslyFocused) {
      this._previouslyFocused.focus();
    }
  }

  _onKeydown(e) {
    if (e.key === 'Escape') {
      this.close();
      return;
    }

    if (e.key === 'Tab') {
      this._trapFocus(e);
    }
  }

  _onBackdropClick(e) {
    if (e.target === this.el) {
      this.close();
    }
  }

  _getFocusable() {
    const selectors = 'a[href], button:not(:disabled), input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex="-1"])';
    return Array.from(this.dialog.querySelectorAll(selectors));
  }

  _trapFocus(e) {
    const focusable = this._getFocusable();
    if (!focusable.length) return;

    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }
}
