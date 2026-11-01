// Original animated "GIF" stickers, drawn on canvas as a pure function of time.
// No third-party GIFs, characters or provider branding.
(function () {
  const TAU = Math.PI * 2;
  const rand = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  const ease = (p) => 1 - Math.pow(1 - Math.min(1, Math.max(0, p)), 3);

  function bg(ctx, w, h, a, b) {
    const g = ctx.createLinearGradient(0, 0, w, h); g.addColorStop(0, a); g.addColorStop(1, b);
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  }
  function confetti(ctx, w, h, t, n, seed) {
    const cols = ['#FDE047', '#F472B6', '#34D399', '#60A5FA', '#F97316', '#FFFFFF'];
    for (let i = 0; i < n; i++) {
      const r = rand(i + seed), r2 = rand(i * 3 + seed), sp = 0.35 + 0.65 * rand(i * 7 + seed);
      const y = ((r2 + t * sp * 0.6) % 1.15) * h * 1.1 - h * 0.08;
      const x = r * w + Math.sin(t * 3 + i) * 10;
      ctx.save(); ctx.translate(x, y); ctx.rotate(t * 4 * (r - 0.5) + i);
      ctx.fillStyle = cols[i % cols.length]; ctx.fillRect(-w * 0.012, -w * 0.006, w * 0.024, w * 0.012); ctx.restore();
    }
  }
  function bigText(ctx, txt, x, y, size, fill, stroke, rot = 0, sc = 1) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc);
    ctx.font = `800 ${size}px Poppins`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.lineJoin = 'round'; ctx.lineWidth = size * 0.16; ctx.strokeStyle = stroke; ctx.strokeText(txt, 0, 0);
    ctx.fillStyle = fill; ctx.fillText(txt, 0, 0); ctx.restore();
  }

  const DRAW = {
    // SOLD! stamp slams in, wobbles, confetti
    sold(ctx, w, h, t) {
      bg(ctx, w, h, '#1E3A8A', '#2563EB');
      const p = (t % 1.6) / 1.6;
      confetti(ctx, w, h, t, 34, 1);
      const slam = p < 0.18 ? 2.2 - 1.3 * ease(p / 0.18) : 0.9 + 0.1 * Math.cos((p - 0.18) * 18) * Math.exp(-(p - 0.18) * 6);
      ctx.save(); ctx.translate(w / 2, h / 2); ctx.rotate(-0.12); ctx.scale(slam, slam);
      const bw = w * 0.62, bh = h * 0.42;
      ctx.lineWidth = w * 0.022; ctx.strokeStyle = '#EF4444'; ctx.fillStyle = 'rgba(255,255,255,.95)';
      ctx.beginPath(); ctx.roundRect(-bw / 2, -bh / 2, bw, bh, w * 0.04); ctx.fill(); ctx.stroke();
      ctx.font = `800 ${h * 0.26}px Poppins`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#EF4444';
      ctx.fillText('SOLD!', 0, h * 0.01); ctx.restore();
    },
    // sales bell swinging with ring lines
    bell(ctx, w, h, t) {
      bg(ctx, w, h, '#F59E0B', '#F97316');
      const a = Math.sin(t * 14) * 0.45 * (0.6 + 0.4 * Math.abs(Math.sin(t * 2)));
      ctx.save(); ctx.translate(w / 2, h * 0.2); ctx.rotate(a);
      const s = h * 0.5;
      ctx.fillStyle = '#FFF7D6'; ctx.strokeStyle = '#7C2D12'; ctx.lineWidth = s * 0.05;
      ctx.beginPath(); ctx.moveTo(-s * 0.45, s * 0.85); ctx.quadraticCurveTo(-s * 0.42, s * 0.05, 0, s * 0.02);
      ctx.quadraticCurveTo(s * 0.42, s * 0.05, s * 0.45, s * 0.85); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#7C2D12'; ctx.beginPath(); ctx.arc(0, s * 0.93, s * 0.1, 0, TAU); ctx.fill();
      ctx.restore();
      ctx.strokeStyle = 'rgba(255,255,255,.9)'; ctx.lineWidth = w * 0.014; ctx.lineCap = 'round';
      const k = (t * 3) % 1;
      for (const side of [-1, 1]) for (let i = 0; i < 3; i++) {
        const r = w * (0.2 + 0.06 * i + 0.05 * k);
        ctx.globalAlpha = 1 - k * 0.8;
        ctx.beginPath(); ctx.arc(w / 2, h * 0.5, r, side > 0 ? -0.5 : Math.PI - 0.5 + 0.0, side > 0 ? 0.5 : Math.PI + 0.5); ctx.stroke();
      }
      ctx.globalAlpha = 1;
      bigText(ctx, 'DING!', w / 2, h * 0.86, h * 0.15, '#fff', '#7C2D12');
    },
    // money raining
    money(ctx, w, h, t) {
      bg(ctx, w, h, '#065F46', '#10B981');
      for (let i = 0; i < 14; i++) {
        const r = rand(i + 9), sp = 0.5 + 0.5 * rand(i * 5 + 2);
        const y = ((rand(i * 11) + t * sp * 0.5) % 1.2) * h * 1.2 - h * 0.15;
        const x = r * w; const bw = w * 0.17, bh = bw * 0.48;
        ctx.save(); ctx.translate(x, y); ctx.rotate(Math.sin(t * 3 + i) * 0.5);
        ctx.fillStyle = '#BBF7D0'; ctx.strokeStyle = '#047857'; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.roundRect(-bw / 2, -bh / 2, bw, bh, 4); ctx.fill(); ctx.stroke();
        ctx.fillStyle = '#047857'; ctx.font = `700 ${bh * 0.7}px Poppins`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText('$', 0, 1); ctx.restore();
      }
      bigText(ctx, 'PAYDAY', w / 2, h / 2, h * 0.2, '#fff', '#064E3B', 0, 1 + 0.05 * Math.sin(t * 8));
    },
    // LET'S GO pulsing with sparkles
    letsgo(ctx, w, h, t) {
      bg(ctx, w, h, '#7C3AED', '#DB2777');
      for (let i = 0; i < 10; i++) {
        const x = rand(i + 4) * w, y = rand(i + 40) * h, s = (0.5 + 0.5 * Math.sin(t * 6 + i * 2)) * w * 0.03;
        ctx.fillStyle = '#FDE68A'; ctx.beginPath();
        for (let k = 0; k < 8; k++) { const r = k % 2 ? s * 0.35 : s; ctx.lineTo(x + Math.cos(k * TAU / 8) * r, y + Math.sin(k * TAU / 8) * r); }
        ctx.fill();
      }
      const sc = 1 + 0.08 * Math.sin(t * 10);
      bigText(ctx, "LET'S", w / 2, h * 0.36, h * 0.22, '#fff', '#4C1D95', -0.06, sc);
      bigText(ctx, 'GO!', w / 2, h * 0.66, h * 0.3, '#FDE047', '#4C1D95', -0.06, sc);
    },
    // chart line shooting up
    rocket(ctx, w, h, t) {
      bg(ctx, w, h, '#0F172A', '#1E293B');
      ctx.strokeStyle = 'rgba(255,255,255,.08)'; ctx.lineWidth = 1;
      for (let i = 1; i < 6; i++) { ctx.beginPath(); ctx.moveTo(0, h * i / 6); ctx.lineTo(w, h * i / 6); ctx.stroke(); }
      const p = (t % 1.8) / 1.8; const n = 40;
      ctx.strokeStyle = '#22D3EE'; ctx.lineWidth = w * 0.02; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.beginPath(); let ex = 0, ey = 0;
      for (let i = 0; i <= n * Math.min(1, p * 1.3); i++) {
        const u = i / n; const x = w * (0.08 + 0.8 * u); const y = h * (0.85 - 0.65 * Math.pow(u, 2.2) - 0.05 * Math.sin(u * 12));
        i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); ex = x; ey = y;
      }
      ctx.stroke();
      ctx.fillStyle = '#22D3EE'; ctx.beginPath(); ctx.arc(ex, ey, w * 0.03, 0, TAU); ctx.fill();
      bigText(ctx, 'TO THE MOON', w / 2, h * 0.16, h * 0.12, '#fff', '#0F172A');
    },
    // trophy with shine
    trophy(ctx, w, h, t) {
      bg(ctx, w, h, '#B45309', '#FBBF24');
      ctx.save(); ctx.translate(w / 2, h * 0.5 + Math.sin(t * 4) * 4); const s = h * 0.36;
      ctx.fillStyle = '#FEF3C7'; ctx.strokeStyle = '#78350F'; ctx.lineWidth = s * 0.06;
      ctx.beginPath(); ctx.moveTo(-s * 0.6, -s * 0.8); ctx.lineTo(s * 0.6, -s * 0.8); ctx.quadraticCurveTo(s * 0.6, s * 0.2, 0, s * 0.3);
      ctx.quadraticCurveTo(-s * 0.6, s * 0.2, -s * 0.6, -s * 0.8); ctx.fill(); ctx.stroke();
      ctx.fillRect(-s * 0.12, s * 0.3, s * 0.24, s * 0.35); ctx.strokeRect(-s * 0.12, s * 0.3, s * 0.24, s * 0.35);
      ctx.fillRect(-s * 0.45, s * 0.65, s * 0.9, s * 0.2); ctx.strokeRect(-s * 0.45, s * 0.65, s * 0.9, s * 0.2);
      ctx.beginPath(); ctx.arc(-s * 0.6, -s * 0.45, s * 0.25, Math.PI * 0.5, Math.PI * 1.5); ctx.stroke();
      ctx.beginPath(); ctx.arc(s * 0.6, -s * 0.45, s * 0.25, -Math.PI * 0.5, Math.PI * 0.5); ctx.stroke();
      const g = (t * 0.8) % 1.4 - 0.2; // shine sweep
      ctx.globalCompositeOperation = 'source-atop';
      ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.beginPath(); ctx.moveTo(-s + g * 2 * s, -s); ctx.lineTo(-s + g * 2 * s + s * 0.25, -s); ctx.lineTo(-s + g * 2 * s - s * 0.35, s); ctx.lineTo(-s + g * 2 * s - s * 0.6, s); ctx.fill();
      ctx.restore(); ctx.globalCompositeOperation = 'source-over';
      bigText(ctx, '#1', w * 0.82, h * 0.2, h * 0.16, '#fff', '#78350F', 0.15);
    },
  };

  window.drawGif = function (canvas, kind, t) {
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    ctx.save(); ctx.clearRect(0, 0, w, h);
    ctx.beginPath(); ctx.roundRect(0, 0, w, h, Math.min(w, h) * 0.06); ctx.clip();
    DRAW[kind](ctx, w, h, t);
    ctx.restore();
  };
})();
