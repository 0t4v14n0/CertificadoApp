// ===== Smooth scroll =====
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
        const id = link.getAttribute('href');
        if (id.length > 1) {
            e.preventDefault();
            document.querySelector(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ===== Fade-in ao scroll =====
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.15 });

document.querySelectorAll('.step-card, .req-card, .faq details').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(24px)';
    el.style.transition = 'opacity .6s ease, transform .6s ease';
    observer.observe(el);
});

// ===== Botão "voltar ao topo" =====
const backBtn = document.createElement('button');
backBtn.innerHTML = '↑';
backBtn.className = 'back-to-top';
backBtn.title = 'Voltar ao topo';
document.body.appendChild(backBtn);

backBtn.addEventListener('click', () =>
    window.scrollTo({ top: 0, behavior: 'smooth' })
);

window.addEventListener('scroll', () => {
    backBtn.classList.toggle('visible', window.scrollY > 500);
});

// Estilo inline do botão (ou mova para o CSS)
Object.assign(backBtn.style, {
    position: 'fixed', bottom: '28px', right: '28px',
    width: '46px', height: '46px', borderRadius: '50%',
    background: '#2e9e5b', color: '#fff', border: 'none',
    fontSize: '1.3rem', cursor: 'pointer',
    boxShadow: '0 6px 20px rgba(46,158,91,.4)',
    opacity: '0', pointerEvents: 'none',
    transition: 'opacity .3s, transform .2s'
});

/* ============================================================
   MODAL DO GIF
   ============================================================ */

function abrirModalGif() {
    const modal = document.getElementById('gif-modal');
    if (!modal) return;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function fecharModalGif(event) {
    // Não fecha se o clique foi na imagem em si
    if (event && event.target.classList.contains('gif-modal-img')) return;

    const modal = document.getElementById('gif-modal');
    if (!modal) return;
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

// Botão do hero
document.getElementById('btn-ver-gif')?.addEventListener('click', abrirModalGif);

// Fechar com ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') fecharModalGif();
});