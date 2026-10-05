"""app.py — Veritas AI · Maximum Power UI"""
from flask import Flask, request, jsonify, render_template_string
from predict import classify_article

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Veritas AI — Intelligence Platform</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
/* ═══════════════════════════════════════════════════════
   DESIGN SYSTEM
   60% → #040C1E (obsidian) — dominant background space
   30% → #0D1F45 / #122459 — surface cards, panels
   10% → #00C8FF (electric cyan) — brand accent, CTAs
   Highlight: #FFD93D (gold) for critical alerts
   ═══════════════════════════════════════════════════════ */
:root{
  /* 60% dominant */
  --bg0:#020810; --bg1:#040C1E; --bg2:#071429; --bg3:#0D1F45;
  /* 30% secondary */
  --s1:#112052; --s2:#1A3070; --s3:#1F3A82;
  /* 10% accent */
  --c:#00C8FF; --c2:#00A8D8; --c3:rgba(0,200,255,0.15);
  /* Semantic */
  --real:#00E5A0; --real2:rgba(0,229,160,0.12);
  --fake:#FF4B4B; --fake2:rgba(255,75,75,0.12);
  --warn:#FFD93D; --warn2:rgba(255,217,61,0.12);
  /* Text */
  --t1:#F0F4FF; --t2:#8899BB; --t3:#4A5A7A;
  /* Type */
  --fd:'Bebas Neue',sans-serif;
  --fb:'Outfit',sans-serif;
  --fm:'IBM Plex Mono',monospace;
  /* Spacing */
  --r:12px; --r2:18px; --r3:24px;
}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  font-family:var(--fb);
  background:var(--bg0);
  color:var(--t1);
  min-height:100vh;
  cursor:none;
  overflow-x:hidden;
}

/* ── Custom cursor ──────────────────────────────── */
#cursor{
  position:fixed;width:12px;height:12px;
  background:var(--c);border-radius:50%;
  pointer-events:none;z-index:9999;
  transform:translate(-50%,-50%);
  transition:width .15s,height .15s,background .15s;
  mix-blend-mode:screen;
}
#cursor-ring{
  position:fixed;width:36px;height:36px;
  border:1px solid rgba(0,200,255,0.4);border-radius:50%;
  pointer-events:none;z-index:9998;
  transform:translate(-50%,-50%);
  transition:all .08s linear;
}
body:has(button:hover) #cursor,
body:has(a:hover) #cursor{width:20px;height:20px;background:var(--warn);}

/* ── Canvas background ──────────────────────────── */
#bg-canvas{position:fixed;inset:0;z-index:0;opacity:.6;}

/* ── Scanline overlay ───────────────────────────── */
body::after{
  content:'';position:fixed;inset:0;z-index:1;
  background:repeating-linear-gradient(
    0deg,transparent,transparent 2px,
    rgba(0,0,0,0.03) 2px,rgba(0,0,0,0.03) 4px
  );pointer-events:none;
}

/* ── Main layout ────────────────────────────────── */
.layout{
  position:relative;z-index:2;
  max-width:1200px;margin:0 auto;padding:0 28px 80px;
}

/* ── Header ─────────────────────────────────────── */
header{
  position:sticky;top:0;z-index:100;
  display:flex;align-items:center;justify-content:space-between;
  padding:16px 28px;
  background:rgba(2,8,16,0.85);
  backdrop-filter:blur(24px) saturate(180%);
  border-bottom:1px solid rgba(0,200,255,0.1);
  margin:0 -28px 0;
}
.logo-wrap{display:flex;align-items:center;gap:14px;}
.logo-icon{
  width:42px;height:42px;
  background:linear-gradient(135deg,var(--c2),#0057FF);
  border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  position:relative;overflow:hidden;
  box-shadow:0 0 28px rgba(0,200,255,0.35);
}
.logo-icon::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,0.15),transparent);
}
.logo-text{
  font-family:var(--fd);font-size:1.7rem;letter-spacing:.05em;
  background:linear-gradient(90deg,var(--t1),var(--c));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.logo-sub{
  font-family:var(--fm);font-size:.62rem;
  color:var(--t2);letter-spacing:.14em;text-transform:uppercase;
  margin-top:-2px;
}
.header-right{display:flex;align-items:center;gap:16px;}
.live-badge{
  display:flex;align-items:center;gap:7px;
  font-family:var(--fm);font-size:.68rem;
  color:var(--real);letter-spacing:.1em;text-transform:uppercase;
  background:rgba(0,229,160,0.08);
  border:1px solid rgba(0,229,160,0.25);
  padding:6px 14px;border-radius:40px;
}
.live-dot{
  width:6px;height:6px;border-radius:50%;
  background:var(--real);
  box-shadow:0 0 8px var(--real);
  animation:blink 1.8s ease-in-out infinite;
}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
.nav-links{display:flex;gap:6px;}
.nav-btn{
  font-family:var(--fm);font-size:.68rem;
  color:var(--t2);letter-spacing:.1em;text-transform:uppercase;
  background:none;border:1px solid rgba(255,255,255,0.07);
  padding:6px 14px;border-radius:6px;cursor:none;
  transition:all .2s;
}
.nav-btn:hover{color:var(--c);border-color:rgba(0,200,255,0.3);}
kbd{
  font-family:var(--fm);font-size:.6rem;
  background:rgba(255,255,255,0.06);
  border:1px solid rgba(255,255,255,0.1);
  padding:1px 5px;border-radius:3px;
  margin-left:4px;color:var(--t3);
}

/* ── Hero ───────────────────────────────────────── */
.hero{
  text-align:center;
  padding:72px 0 56px;
  position:relative;
}
.hero-eyebrow{
  display:inline-flex;align-items:center;gap:8px;
  font-family:var(--fm);font-size:.7rem;color:var(--c);
  letter-spacing:.16em;text-transform:uppercase;
  margin-bottom:22px;
  opacity:0;animation:slideUp .6s .1s ease forwards;
}
.hero-eyebrow-line{width:28px;height:1px;background:var(--c);}
.hero h1{
  font-family:var(--fd);
  font-size:clamp(3rem,7vw,6rem);
  letter-spacing:.04em;line-height:.95;
  margin-bottom:20px;
  opacity:0;animation:slideUp .7s .2s ease forwards;
}
.hero h1 .line2{
  display:block;
  background:linear-gradient(90deg,var(--c) 0%,#8B5CF6 60%,var(--warn) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-size:200% auto;
  animation:gradShift 4s linear infinite;
}
@keyframes gradShift{0%{background-position:0%}100%{background-position:200%}}
.hero p{
  font-size:1.05rem;font-weight:300;color:var(--t2);
  max-width:520px;margin:0 auto 44px;line-height:1.75;
  opacity:0;animation:slideUp .7s .35s ease forwards;
}
@keyframes slideUp{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:translateY(0)}}

/* ── KPI strip ──────────────────────────────────── */
.kpi-strip{
  display:flex;justify-content:center;align-items:stretch;
  gap:1px;border-radius:var(--r2);overflow:hidden;
  border:1px solid rgba(0,200,255,0.12);
  max-width:680px;margin:0 auto;
  opacity:0;animation:slideUp .7s .5s ease forwards;
}
.kpi{
  flex:1;padding:16px 10px;
  background:rgba(13,31,69,0.7);
  text-align:center;
  position:relative;overflow:hidden;
  transition:background .25s;
}
.kpi:hover{background:rgba(26,48,112,0.8);}
.kpi::before{
  content:'';position:absolute;
  inset:0 0 auto 0;height:1px;
  background:linear-gradient(90deg,transparent,var(--c),transparent);
  opacity:0;transition:opacity .25s;
}
.kpi:hover::before{opacity:1;}
.kpi-val{
  font-family:var(--fd);font-size:1.85rem;
  letter-spacing:.04em;
  background:linear-gradient(135deg,var(--t1),var(--c));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.kpi-lbl{
  font-family:var(--fm);font-size:.58rem;
  color:var(--t3);letter-spacing:.12em;text-transform:uppercase;
  margin-top:3px;
}

/* ── Bento grid ─────────────────────────────────── */
.bento{
  display:grid;
  grid-template-columns:2fr 1fr;
  grid-template-rows:auto auto;
  gap:14px;
  margin-top:16px;
}
@media(max-width:768px){.bento{grid-template-columns:1fr;}}

/* ── Glass card base ────────────────────────────── */
.card{
  background:rgba(7,20,41,0.75);
  border:1px solid rgba(0,200,255,0.1);
  border-radius:var(--r2);
  padding:28px;
  position:relative;overflow:hidden;
  backdrop-filter:blur(16px);
  transition:border-color .3s,transform .2s,box-shadow .3s;
}
.card:hover{
  border-color:rgba(0,200,255,0.25);
  box-shadow:0 0 40px rgba(0,200,255,0.07);
}
/* Top shimmer */
.card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent 0%,rgba(0,200,255,0.5) 50%,transparent 100%);
  opacity:.5;
}
/* Depth corner accent */
.card::after{
  content:'';position:absolute;
  top:-40px;right:-40px;width:100px;height:100px;
  background:radial-gradient(circle,rgba(0,200,255,0.06),transparent 70%);
  pointer-events:none;
}
.card-span2{grid-column:1/-1;}

/* ── Card label ─────────────────────────────────── */
.clabel{
  display:flex;align-items:center;gap:8px;
  font-family:var(--fm);font-size:.65rem;
  color:var(--t3);letter-spacing:.14em;text-transform:uppercase;
  margin-bottom:18px;
}
.clabel-dot{
  width:5px;height:5px;border-radius:50%;
  background:var(--c);
  box-shadow:0 0 6px var(--c);
}

/* ── Input fields ───────────────────────────────── */
.input-group{margin-bottom:14px;}
.input-label{
  font-family:var(--fm);font-size:.62rem;
  color:var(--t3);letter-spacing:.12em;text-transform:uppercase;
  margin-bottom:7px;display:flex;align-items:center;
  justify-content:space-between;
}
.char-count{font-size:.6rem;color:var(--t3);transition:color .2s;}
.char-count.active{color:var(--c);}
.field-wrap{position:relative;}
.field-icon{
  position:absolute;left:14px;
  color:var(--t3);font-size:13px;pointer-events:none;
  transition:color .2s;
}
.field-icon.top{top:14px;}
.field-icon.mid{top:50%;transform:translateY(-50%);}
input[type=text],textarea{
  width:100%;
  background:rgba(2,8,16,0.6);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:var(--r);
  color:var(--t1);
  font-family:var(--fb);font-size:.92rem;font-weight:300;
  outline:none;resize:none;
  transition:border-color .2s,box-shadow .2s,background .2s;
}
input[type=text]{padding:12px 14px 12px 40px;}
textarea{padding:14px 14px 14px 40px;height:130px;line-height:1.65;}
input[type=text]:focus,textarea:focus{
  border-color:rgba(0,200,255,0.4);
  background:rgba(4,12,30,0.8);
  box-shadow:0 0 0 3px rgba(0,200,255,0.08),inset 0 1px 0 rgba(0,200,255,0.05);
}
input:focus+.field-icon,textarea:focus+.field-icon{color:var(--c);}
input::placeholder,textarea::placeholder{color:var(--t3);font-weight:300;}

/* ── Action row ─────────────────────────────────── */
.action-row{
  display:flex;align-items:center;
  flex-wrap:wrap;gap:10px;
  margin-top:20px;
}
.btn-primary{
  display:inline-flex;align-items:center;gap:9px;
  font-family:var(--fb);font-weight:600;font-size:.9rem;
  letter-spacing:.02em;
  color:#000;
  background:var(--c);
  border:none;cursor:none;
  padding:13px 28px;border-radius:var(--r);
  position:relative;overflow:hidden;
  transition:transform .15s,box-shadow .2s;
  box-shadow:0 4px 24px rgba(0,200,255,0.3);
}
.btn-primary::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,0.15),transparent);
}
.btn-primary:hover{
  transform:translateY(-2px);
  box-shadow:0 8px 32px rgba(0,200,255,0.45);
}
.btn-primary:active{transform:translateY(0);}
.btn-primary svg{transition:transform .25s;}
.btn-primary:hover svg{transform:translateX(4px);}

.btn-ghost{
  display:inline-flex;align-items:center;gap:7px;
  font-family:var(--fb);font-size:.85rem;font-weight:400;
  color:var(--t2);
  background:none;
  border:1px solid rgba(255,255,255,0.08);
  cursor:none;padding:12px 18px;border-radius:var(--r);
  transition:all .2s;
}
.btn-ghost:hover{
  color:var(--t1);
  border-color:rgba(255,255,255,0.18);
  background:rgba(255,255,255,0.04);
}
.shortcut{
  font-family:var(--fm);font-size:.58rem;
  background:rgba(255,255,255,0.06);
  border:1px solid rgba(255,255,255,0.1);
  padding:2px 6px;border-radius:4px;
  color:var(--t3);
}

/* ── Right panel: quick guide ───────────────────── */
.guide-card{
  display:flex;flex-direction:column;gap:10px;
}
.guide-item{
  display:flex;align-items:flex-start;gap:12px;
  padding:12px;border-radius:var(--r);
  background:rgba(2,8,16,0.4);
  border:1px solid rgba(255,255,255,0.05);
  transition:border-color .2s,background .2s;
  cursor:none;
}
.guide-item:hover{
  border-color:rgba(0,200,255,0.2);
  background:rgba(0,200,255,0.04);
}
.guide-icon{
  width:32px;height:32px;border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-size:15px;flex-shrink:0;
}
.guide-icon.g1{background:rgba(0,229,160,0.12);}
.guide-icon.g2{background:rgba(255,75,75,0.12);}
.guide-icon.g3{background:rgba(255,217,61,0.12);}
.guide-title{font-size:.82rem;font-weight:500;margin-bottom:2px;}
.guide-desc{font-size:.75rem;color:var(--t2);line-height:1.5;}

/* ── Radar scanner animation ────────────────────── */
#scan-overlay{
  display:none;
  position:fixed;inset:0;z-index:200;
  background:rgba(2,8,16,0.92);
  backdrop-filter:blur(8px);
  align-items:center;justify-content:center;
  flex-direction:column;gap:28px;
}
#scan-overlay.active{display:flex;}
.radar-wrap{position:relative;width:180px;height:180px;}
.radar-ring{
  position:absolute;border-radius:50%;border-style:solid;
  border-color:rgba(0,200,255,0.15);
  border-width:1px;
}
.r1{inset:0;}
.r2{inset:20px;}
.r3{inset:40px;}
.r4{inset:60px;}
.radar-sweep{
  position:absolute;inset:0;border-radius:50%;
  background:conic-gradient(from 0deg,transparent 340deg,rgba(0,200,255,0.6) 360deg);
  animation:radarSpin 1.8s linear infinite;
}
@keyframes radarSpin{to{transform:rotate(360deg)}}
.radar-dot{
  position:absolute;width:4px;height:4px;border-radius:50%;
  background:var(--c);box-shadow:0 0 8px var(--c);
}
.rd1{top:25%;left:60%;animation:blip 1.8s .4s ease-in-out infinite;}
.rd2{top:60%;left:30%;animation:blip 1.8s .9s ease-in-out infinite;}
.rd3{top:45%;left:75%;animation:blip 1.8s 1.3s ease-in-out infinite;}
@keyframes blip{0%,100%{opacity:0;transform:scale(0)}40%,60%{opacity:1;transform:scale(1)}}
.radar-crosshair{
  position:absolute;inset:0;
  display:flex;align-items:center;justify-content:center;
}
.radar-crosshair::before,.radar-crosshair::after{
  content:'';position:absolute;background:rgba(0,200,255,0.2);
}
.radar-crosshair::before{width:1px;height:100%;}
.radar-crosshair::after{width:100%;height:1px;}
.scan-text{
  font-family:var(--fm);font-size:.75rem;
  color:var(--c);letter-spacing:.15em;text-transform:uppercase;
}
.scan-steps{
  display:flex;flex-direction:column;gap:6px;width:260px;
}
.scan-step{
  display:flex;align-items:center;gap:10px;
  font-family:var(--fm);font-size:.7rem;color:var(--t3);
  transition:color .3s;
}
.scan-step.active{color:var(--t1);}
.scan-step.done{color:var(--real);}
.step-dot{
  width:6px;height:6px;border-radius:50%;
  background:var(--t3);flex-shrink:0;transition:background .3s;
}
.scan-step.active .step-dot{background:var(--c);box-shadow:0 0 8px var(--c);}
.scan-step.done .step-dot{background:var(--real);box-shadow:0 0 6px var(--real);}

/* ── Results: bento ─────────────────────────────── */
#result-section{display:none;}

.result-bento{
  display:grid;
  grid-template-columns:repeat(12,1fr);
  grid-auto-rows:auto;
  gap:12px;
  margin-top:16px;
}

/* Verdict card — spans 7 cols */
.rc-verdict{
  grid-column:span 7;
  padding:32px;
}
/* Clickbait card — spans 5 cols */
.rc-cb{
  grid-column:span 5;
  padding:32px;
}
/* Metrics row — 4 equal cells */
.rc-metric{
  grid-column:span 3;
  padding:22px;
  text-align:center;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
}
/* Analysis card full width */
.rc-full{
  grid-column:span 12;
  padding:26px;
}
@media(max-width:768px){
  .rc-verdict,.rc-cb,.rc-metric,.rc-full{grid-column:1/-1;}
}

/* Verdict display */
.verdict-label{
  font-family:var(--fm);font-size:.62rem;
  color:var(--t3);letter-spacing:.14em;text-transform:uppercase;
  margin-bottom:12px;
}
.verdict-big{
  font-family:var(--fd);
  font-size:5rem;letter-spacing:.06em;
  line-height:1;margin-bottom:6px;
  transition:color .4s;
  position:relative;display:inline-block;
}
/* Glitch effect on verdict */
.verdict-big.glitch::before,.verdict-big.glitch::after{
  content:attr(data-text);
  position:absolute;top:0;left:0;
  width:100%;height:100%;
  font-family:var(--fd);font-size:inherit;
}
.verdict-big.glitch::before{
  color:var(--fake);clip-path:polygon(0 20%,100% 20%,100% 40%,0 40%);
  transform:translateX(-2px);animation:glitch1 .3s ease forwards;
}
.verdict-big.glitch::after{
  color:var(--c);clip-path:polygon(0 60%,100% 60%,100% 80%,0 80%);
  transform:translateX(2px);animation:glitch2 .3s ease forwards;
}
@keyframes glitch1{0%,100%{clip-path:polygon(0 20%,100% 20%,100% 40%,0 40%)}
  50%{clip-path:polygon(0 25%,100% 25%,100% 35%,0 35%);transform:translateX(-4px)}}
@keyframes glitch2{0%,100%{clip-path:polygon(0 60%,100% 60%,100% 80%,0 80%)}
  50%{clip-path:polygon(0 65%,100% 65%,100% 75%,0 75%);transform:translateX(4px)}}

.verdict-big.real{color:var(--real);}
.verdict-big.fake{color:var(--fake);}

.confidence-row{
  display:flex;align-items:baseline;gap:8px;
  margin-bottom:18px;
}
.conf-num{
  font-family:var(--fd);font-size:2.2rem;color:var(--t1);
}
.conf-label{font-size:.82rem;color:var(--t2);}

/* Layered progress bar */
.progress-track{
  height:8px;background:rgba(255,255,255,0.05);
  border-radius:4px;overflow:visible;
  position:relative;margin-bottom:20px;
}
.progress-fill{
  height:100%;border-radius:4px;width:0%;
  transition:width 1.2s cubic-bezier(.4,0,.2,1);
  position:relative;
}
.progress-fill::after{
  content:'';position:absolute;right:-1px;top:50%;transform:translateY(-50%);
  width:12px;height:12px;border-radius:50%;
  border:2px solid var(--bg1);
  background:inherit;
  box-shadow:0 0 10px currentColor;
}
.progress-fill.real{background:linear-gradient(90deg,rgba(0,229,160,.4),var(--real));}
.progress-fill.fake{background:linear-gradient(90deg,rgba(255,75,75,.4),var(--fake));}

.verdict-tags{display:flex;gap:8px;flex-wrap:wrap;}
.vtag{
  font-family:var(--fm);font-size:.62rem;
  letter-spacing:.08em;text-transform:uppercase;
  padding:4px 10px;border-radius:20px;
}
.vtag-model{background:rgba(0,200,255,0.1);color:var(--c);border:1px solid rgba(0,200,255,0.2);}
.vtag-real{background:var(--real2);color:var(--real);border:1px solid rgba(0,229,160,0.2);}
.vtag-fake{background:var(--fake2);color:var(--fake);border:1px solid rgba(255,75,75,0.2);}

/* Clickbait gauge */
.cb-gauge-wrap{
  display:flex;flex-direction:column;align-items:center;
  margin:8px 0 16px;
}
.arc-svg{overflow:visible;}
.arc-bg{fill:none;stroke:rgba(255,255,255,0.06);stroke-width:8;stroke-linecap:round;}
.arc-fill{
  fill:none;stroke-width:8;stroke-linecap:round;
  stroke-dasharray:220;stroke-dashoffset:220;
  transition:stroke-dashoffset 1.4s cubic-bezier(.4,0,.2,1),stroke .4s;
  transform-origin:80px 80px;transform:rotate(-210deg);
}
.arc-center-val{
  font-family:var(--fd);font-size:1.6rem;
  fill:var(--t1);text-anchor:middle;dominant-baseline:middle;
}
.arc-center-lbl{
  font-family:'IBM Plex Mono',monospace;font-size:8px;
  fill:var(--t3);text-anchor:middle;dominant-baseline:middle;
  text-transform:uppercase;letter-spacing:1.5px;
}
.cb-risk-badge{
  font-family:var(--fm);font-size:.7rem;
  letter-spacing:.12em;text-transform:uppercase;
  padding:5px 14px;border-radius:20px;font-weight:500;
  margin-top:8px;
}
.cb-desc-text{
  font-size:.8rem;color:var(--t2);text-align:center;
  line-height:1.6;margin-top:10px;
}

/* Metric cards */
.metric-value{
  font-family:var(--fd);font-size:2.2rem;letter-spacing:.04em;
  background:linear-gradient(135deg,var(--t1),var(--c));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin-bottom:4px;
}
.metric-label{
  font-family:var(--fm);font-size:.58rem;
  color:var(--t3);letter-spacing:.12em;text-transform:uppercase;
}
.metric-bar{
  width:40px;height:2px;background:rgba(0,200,255,0.3);
  border-radius:1px;margin:8px auto 0;
}

/* Analysis bar chart */
.bar-chart{display:flex;flex-direction:column;gap:10px;}
.bar-row{display:flex;align-items:center;gap:12px;}
.bar-name{font-family:var(--fm);font-size:.66rem;color:var(--t2);width:90px;text-align:right;flex-shrink:0;}
.bar-track{flex:1;height:6px;background:rgba(255,255,255,0.04);border-radius:3px;overflow:hidden;}
.bar-fill-anim{height:100%;border-radius:3px;width:0%;transition:width 1s cubic-bezier(.4,0,.2,1);}
.bar-val{font-family:var(--fm);font-size:.66rem;color:var(--t1);width:40px;flex-shrink:0;}

/* History log */
.hist-list{display:flex;flex-direction:column;gap:8px;max-height:220px;overflow-y:auto;}
.hist-list::-webkit-scrollbar{width:2px;}
.hist-list::-webkit-scrollbar-thumb{background:rgba(0,200,255,0.2);border-radius:1px;}
.hist-row{
  display:flex;align-items:center;gap:12px;
  padding:11px 14px;border-radius:var(--r);
  background:rgba(2,8,16,0.4);
  border:1px solid rgba(255,255,255,0.05);
  transition:border-color .2s,background .2s;
  cursor:none;
}
.hist-row:hover{
  border-color:rgba(0,200,255,0.15);
  background:rgba(0,200,255,0.03);
}
.hist-indicator{
  width:3px;height:32px;border-radius:2px;flex-shrink:0;
}
.hist-indicator.real{background:var(--real);}
.hist-indicator.fake{background:var(--fake);}
.hist-indicator.warn{background:var(--warn);}
.hist-title-text{flex:1;font-size:.84rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.hist-meta{font-family:var(--fm);font-size:.64rem;color:var(--t3);}
.hist-verdict-badge{
  font-family:var(--fd);font-size:.9rem;letter-spacing:.06em;
  padding:3px 10px;border-radius:6px;
}
.hvb-real{color:var(--real);background:var(--real2);}
.hvb-fake{color:var(--fake);background:var(--fake2);}
.hvb-warn{color:var(--warn);background:var(--warn2);}

/* Footer */
footer{
  text-align:center;padding:28px;
  font-family:var(--fm);font-size:.65rem;
  color:var(--t3);letter-spacing:.08em;
  border-top:1px solid rgba(255,255,255,0.05);
  position:relative;z-index:2;
}

/* Animations */
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
.fade-up{animation:fadeUp .5s ease forwards;}
@keyframes countUp{from{opacity:0;transform:scale(.8)}to{opacity:1;transform:scale(1)}}

/* Focus styles for keyboard nav */
*:focus-visible{
  outline:2px solid var(--c);
  outline-offset:3px;
}
</style>
</head>
<body>

<!-- Custom cursor -->
<div id="cursor"></div>
<div id="cursor-ring"></div>

<!-- Animated particle canvas -->
<canvas id="bg-canvas"></canvas>

<!-- Radar scan overlay -->
<div id="scan-overlay">
  <div class="radar-wrap">
    <div class="radar-ring r1"></div>
    <div class="radar-ring r2"></div>
    <div class="radar-ring r3"></div>
    <div class="radar-ring r4"></div>
    <div class="radar-sweep"></div>
    <div class="radar-dot rd1"></div>
    <div class="radar-dot rd2"></div>
    <div class="radar-dot rd3"></div>
    <div class="radar-crosshair"></div>
  </div>
  <div class="scan-text" id="scan-stage">Initialising scan…</div>
  <div class="scan-steps">
    <div class="scan-step" id="ss1"><div class="step-dot"></div>Preprocessing text pipeline</div>
    <div class="scan-step" id="ss2"><div class="step-dot"></div>TF-IDF vectorisation (5,000 features)</div>
    <div class="scan-step" id="ss3"><div class="step-dot"></div>PAC model inference · Module A</div>
    <div class="scan-step" id="ss4"><div class="step-dot"></div>Cosine dissimilarity · Module B</div>
    <div class="scan-step" id="ss5"><div class="step-dot"></div>Aggregating dual-module output</div>
  </div>
</div>

<!-- ── HEADER ─────────────────────────────────── -->
<header>
  <div class="logo-wrap">
    <div class="logo-icon">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
        <path d="M12 2L3 7v5c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7L12 2z"
          fill="rgba(0,200,255,0.3)" stroke="#00C8FF" stroke-width="1.5"/>
        <path d="M9 12l2 2 4-4" stroke="#00C8FF" stroke-width="1.8" stroke-linecap="round"/>
      </svg>
    </div>
    <div>
      <div class="logo-text">Veritas AI</div>
      <div class="logo-sub">Intelligence Platform · v2.0</div>
    </div>
  </div>
  <div class="header-right">
    <div class="live-badge"><div class="live-dot"></div>System Online</div>
    <div class="nav-links">
      <button class="nav-btn" onclick="focusTitle()" title="Jump to input">Analyse<kbd>A</kbd></button>
      <button class="nav-btn" onclick="clearAll()" title="Clear all">Clear<kbd>C</kbd></button>
      <button class="nav-btn" onclick="runDemo()" title="Load demo">Demo<kbd>D</kbd></button>
    </div>
  </div>
</header>

<div class="layout">

  <!-- ── HERO ───────────────────────────────────── -->
  <section class="hero">
    <div class="hero-eyebrow">
      <div class="hero-eyebrow-line"></div>
      Dual-Engine News Intelligence
      <div class="hero-eyebrow-line"></div>
    </div>
    <h1>
      DETECT THE<br/>
      <span class="line2">MISINFORMATION</span>
    </h1>
    <p>Passive-Aggressive Classifier + Semantic Clickbait Analysis.<br/>
       Real-time verdict in under 5ms. No GPU required.</p>

    <div class="kpi-strip">
      <div class="kpi"><div class="kpi-val">93.7%</div><div class="kpi-lbl">Accuracy</div></div>
      <div class="kpi"><div class="kpi-val">0.981</div><div class="kpi-lbl">ROC-AUC</div></div>
      <div class="kpi"><div class="kpi-val">44.9K</div><div class="kpi-lbl">Trained On</div></div>
      <div class="kpi"><div class="kpi-val">&lt;5ms</div><div class="kpi-lbl">Inference</div></div>
      <div class="kpi"><div class="kpi-val">2</div><div class="kpi-lbl">Modules</div></div>
    </div>
  </section>

  <!-- ── INPUT BENTO ────────────────────────────── -->
  <div class="bento">

    <!-- Main input card -->
    <div class="card" style="grid-column:span 2;grid-row:1">
      <div class="clabel"><div class="clabel-dot"></div>Submit Article for Analysis</div>

      <div class="input-group">
        <div class="input-label">
          <span>Article Headline</span>
          <span class="char-count" id="title-count">0 / 200</span>
        </div>
        <div class="field-wrap">
          <span class="field-icon mid">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </span>
          <input type="text" id="title" maxlength="200"
            placeholder="Paste the article headline here…"
            aria-label="Article headline"
            oninput="updateCount('title','title-count',200)"/>
        </div>
      </div>

      <div class="input-group">
        <div class="input-label">
          <span>Article Body Text</span>
          <span class="char-count" id="body-count">0 / 5000</span>
        </div>
        <div class="field-wrap">
          <span class="field-icon top">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10 9 9 9 8 9"/>
            </svg>
          </span>
          <textarea id="body" maxlength="5000"
            placeholder="Paste the full article body text here for comprehensive dual-module analysis…"
            aria-label="Article body text"
            oninput="updateCount('body','body-count',5000)"></textarea>
        </div>
      </div>

      <div class="action-row">
        <button class="btn-primary" onclick="analyse()" id="analyse-btn" aria-label="Analyse article (keyboard: Enter)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
          </svg>
          Run Analysis
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </button>
        <button class="btn-ghost" onclick="runDemo()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
          Demo
          <span class="shortcut">D</span>
        </button>
        <button class="btn-ghost" onclick="clearAll()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 102.13-9.36L1 10"/>
          </svg>
          Clear
          <span class="shortcut">C</span>
        </button>
      </div>
    </div>

    <!-- Guide card -->
    <div class="card guide-card" style="grid-column:1;grid-row:2">
      <div class="clabel"><div class="clabel-dot"></div>What to expect</div>
      <div class="guide-item">
        <div class="guide-icon g1">✓</div>
        <div>
          <div class="guide-title">REAL + Low Clickbait</div>
          <div class="guide-desc">Credible source, headline matches body. High confidence typical.</div>
        </div>
      </div>
      <div class="guide-item">
        <div class="guide-icon g2">✕</div>
        <div>
          <div class="guide-title">FAKE + High Clickbait</div>
          <div class="guide-desc">Fabricated content with sensationalist framing.</div>
        </div>
      </div>
      <div class="guide-item">
        <div class="guide-icon g3">⚠</div>
        <div>
          <div class="guide-title">REAL + High Clickbait</div>
          <div class="guide-desc">Factual body but misleading headline. Veritas AI's novel detection.</div>
        </div>
      </div>
    </div>

    <!-- History card -->
    <div class="card" id="hist-card" style="grid-column:2;grid-row:2;display:none;">
      <div class="clabel"><div class="clabel-dot"></div>Session History</div>
      <div class="hist-list" id="hist-list" role="log" aria-live="polite"></div>
    </div>
  </div>

  <!-- ── RESULTS ────────────────────────────────── -->
  <section id="result-section" aria-live="polite">
    <div class="result-bento" id="result-bento">

      <!-- Verdict card (7 cols) -->
      <div class="card rc-verdict fade-up" id="card-verdict" style="animation-delay:.0s">
        <div class="verdict-label">Module A · Veracity Classification</div>
        <div class="verdict-big" id="vbig" data-text="—">—</div>
        <div class="confidence-row">
          <div class="conf-num" id="conf-num">0%</div>
          <div class="conf-label">confidence score</div>
        </div>
        <div class="progress-track">
          <div class="progress-fill" id="prog-fill"></div>
        </div>
        <div class="verdict-tags" id="vtags"></div>
      </div>

      <!-- Clickbait card (5 cols) -->
      <div class="card rc-cb fade-up" id="card-cb" style="animation-delay:.08s">
        <div class="verdict-label">Module B · Clickbait Detection</div>
        <div class="cb-gauge-wrap">
          <svg class="arc-svg" width="160" height="120" viewBox="0 0 160 110">
            <path class="arc-bg" d="M 20 95 A 60 60 0 1 1 140 95"/>
            <path class="arc-fill" id="arc-fill" stroke="#00C8FF"
              d="M 20 95 A 60 60 0 1 1 140 95"
              pathLength="220"/>
            <text class="arc-center-val" id="arc-val" x="80" y="72">—</text>
            <text class="arc-center-lbl" id="arc-lbl" x="80" y="88">score</text>
          </svg>
        </div>
        <div style="text-align:center">
          <div class="cb-risk-badge" id="cb-risk-badge">—</div>
          <div class="cb-desc-text" id="cb-desc-text">—</div>
        </div>
      </div>

      <!-- 4 metric cards -->
      <div class="card rc-metric fade-up" style="animation-delay:.16s">
        <div class="metric-value" id="m-prec">—</div>
        <div class="metric-label">Precision</div>
        <div class="metric-bar"></div>
      </div>
      <div class="card rc-metric fade-up" style="animation-delay:.20s">
        <div class="metric-value" id="m-recall">—</div>
        <div class="metric-label">Recall</div>
        <div class="metric-bar"></div>
      </div>
      <div class="card rc-metric fade-up" style="animation-delay:.24s">
        <div class="metric-value" id="m-f1">—</div>
        <div class="metric-label">F1-Score</div>
        <div class="metric-bar"></div>
      </div>
      <div class="card rc-metric fade-up" style="animation-delay:.28s">
        <div class="metric-value">0.981</div>
        <div class="metric-label">ROC-AUC</div>
        <div class="metric-bar"></div>
      </div>

      <!-- Bar chart analysis -->
      <div class="card rc-full fade-up" style="animation-delay:.32s">
        <div class="clabel"><div class="clabel-dot"></div>Performance Breakdown</div>
        <div class="bar-chart" id="bar-chart"></div>
      </div>

    </div>
  </section>

</div>

<footer>
  Veritas AI · INT4203E Artificial Intelligence · INTI International University ·
  January 2026
  <span style="margin-left:16px;color:rgba(0,200,255,0.4)">
    Press <kbd style="background:rgba(0,200,255,0.08);border:1px solid rgba(0,200,255,0.2);padding:1px 5px;border-radius:3px;font-family:var(--fm);font-size:.58rem">?</kbd>
    for keyboard shortcuts
  </span>
</footer>

<script>
/* ── Cursor ──────────────────────────────────────── */
const cur = document.getElementById('cursor');
const curR = document.getElementById('cursor-ring');
let mx=0,my=0,rx=0,ry=0;
document.addEventListener('mousemove',e=>{
  mx=e.clientX; my=e.clientY;
  cur.style.left=mx+'px'; cur.style.top=my+'px';
});
(function animRing(){
  rx+=(mx-rx)*.12; ry+=(my-ry)*.12;
  curR.style.left=rx+'px'; curR.style.top=ry+'px';
  requestAnimationFrame(animRing);
})();

/* ── Particle canvas ─────────────────────────────── */
(function(){
  const c=document.getElementById('bg-canvas');
  const ctx=c.getContext('2d');
  let W,H,pts=[];
  function resize(){
    W=c.width=window.innerWidth;
    H=c.height=window.innerHeight;
  }
  resize();
  window.addEventListener('resize',resize);
  const N=70;
  for(let i=0;i<N;i++) pts.push({
    x:Math.random()*W, y:Math.random()*H,
    vx:(Math.random()-.5)*.3, vy:(Math.random()-.5)*.3,
    r:Math.random()*1.5+.5
  });
  function draw(){
    ctx.clearRect(0,0,W,H);
    for(let i=0;i<N;i++){
      const p=pts[i];
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<0||p.x>W) p.vx*=-1;
      if(p.y<0||p.y>H) p.vy*=-1;
      ctx.beginPath();
      ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle='rgba(0,200,255,0.35)';
      ctx.fill();
      for(let j=i+1;j<N;j++){
        const q=pts[j];
        const dx=p.x-q.x, dy=p.y-q.y;
        const d=Math.sqrt(dx*dx+dy*dy);
        if(d<120){
          ctx.beginPath();
          ctx.moveTo(p.x,p.y); ctx.lineTo(q.x,q.y);
          ctx.strokeStyle=`rgba(0,200,255,${.12*(1-d/120)})`;
          ctx.lineWidth=.4;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  draw();
})();

/* ── Char counter ────────────────────────────────── */
function updateCount(fieldId,countId,max){
  const len=document.getElementById(fieldId).value.length;
  const el=document.getElementById(countId);
  el.textContent=`${len} / ${max}`;
  el.classList.toggle('active',len>0);
}

/* ── Keyboard shortcuts ──────────────────────────── */
document.addEventListener('keydown',e=>{
  if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA') return;
  if(e.key==='a'||e.key==='A') focusTitle();
  if(e.key==='c'||e.key==='C') clearAll();
  if(e.key==='d'||e.key==='D') runDemo();
  if(e.key==='Enter') analyse();
  if(e.key==='?') showShortcuts();
});
document.addEventListener('keydown',e=>{
  if((e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA')&&e.key==='Enter'&&e.ctrlKey){
    analyse();
  }
});

function focusTitle(){
  document.getElementById('title').focus();
}

/* ── Demo articles ───────────────────────────────── */
const demos=[
  {
    title:'Aliens Land in Nilai — Residents Flee in Terror as Government Denies Everything',
    body:'Residents of Nilai, Negeri Sembilan reported an unusual atmospheric phenomenon on Tuesday evening when a large lenticular cloud formation appeared above the town centre at approximately 9:15 PM. The disc-shaped cloud, caused by stable moist air flowing over elevated terrain, was visible for approximately 40 minutes before dissipating. Local meteorologist Dr. Farah Aziz confirmed that lenticular clouds are a well-documented weather event and pose no hazard. Several residents photographed the formation and shared images on social media. No unusual activity was recorded by air traffic control at KLIA.'
  },
  {
    title:'BREAKING: WHO Confirms 5G Towers Are Spreading COVID-19 Variants, Governments Cover It Up',
    body:'Anonymous government insiders have come forward with explosive evidence that 5G cellular towers are being used to spread mutated variants of COVID-19 through radio frequency emissions. Whistleblowers claim telecommunications companies signed secret agreements with pharmaceutical giants to ensure continuous vaccine demand. Scientists who attempted to publish findings were allegedly silenced by journal editors. The public is urged to wrap routers in aluminum foil and avoid standing within 50 meters of any cellular infrastructure.'
  },
  {
    title:"Malaysia's Inflation Rate Eases to 1.5% in February 2024 as Food Prices Stabilise",
    body:"Malaysia's headline inflation rate moderated to 1.5 percent in February 2024, down from 1.8 percent in January, according to data released by the Department of Statistics Malaysia. The easing was primarily driven by a slowdown in food and non-alcoholic beverages inflation, which declined to 2.1 percent from 2.6 percent. Core inflation held steady at 1.8 percent. Bank Negara Malaysia maintained its overnight policy rate at 3.0 percent, citing stable domestic demand and a manageable inflation outlook."
  }
];
let demoIdx=0;
function runDemo(){
  const d=demos[demoIdx++%demos.length];
  document.getElementById('title').value=d.title;
  document.getElementById('body').value=d.body;
  updateCount('title','title-count',200);
  updateCount('body','body-count',5000);
  focusTitle();
}

/* ── Scan animation ──────────────────────────────── */
const steps=['ss1','ss2','ss3','ss4','ss5'];
const stepLabels=['Preprocessing text…','Vectorising with TF-IDF…','Module A · PAC inference…','Module B · Clickbait score…','Aggregating results…'];
async function runScanAnim(){
  const overlay=document.getElementById('scan-overlay');
  overlay.classList.add('active');
  steps.forEach(s=>{
    const el=document.getElementById(s);
    el.className='scan-step';
  });
  for(let i=0;i<steps.length;i++){
    document.getElementById('scan-stage').textContent=stepLabels[i];
    if(i>0) document.getElementById(steps[i-1]).className='scan-step done';
    document.getElementById(steps[i]).className='scan-step active';
    await sleep(380);
  }
  document.getElementById(steps[steps.length-1]).className='scan-step done';
  await sleep(300);
  overlay.classList.remove('active');
}
function sleep(ms){return new Promise(r=>setTimeout(r,ms));}

/* ── Main analyse ────────────────────────────────── */
const hist=[];
async function analyse(){
  const title=document.getElementById('title').value.trim();
  const body=document.getElementById('body').value.trim();
  if(!title&&!body){ shake(); return; }

  document.getElementById('result-section').style.display='none';
  await runScanAnim();

  let data;
  try{
    const r=await fetch('/predict',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({title,body})
    });
    data=await r.json();
  } catch(e){
    alert('Server error — make sure train.py was run first.');
    return;
  }
  renderResult(data,title);
}

/* ── Render ──────────────────────────────────────── */
const descMap={
  LOW:'Headline accurately reflects article content. No deceptive framing detected.',
  MODERATE:'Some semantic divergence detected. Recommend reading the full article.',
  HIGH:'Strong headline–body mismatch. High probability of clickbait framing.'
};
const modelStats={
  REAL:{prec:'0.941',recall:'0.931',f1:'0.936'},
  FAKE:{prec:'0.934',recall:'0.943',f1:'0.938'}
};

function renderResult(d,title){
  const v=d.verdict;
  const cls=v==='REAL'?'real':'fake';
  const conf=Math.round(d.confidence*1000)/10;
  const cb=d.cb_score;
  const cbR=d.cb_risk;

  /* Verdict card */
  const vbig=document.getElementById('vbig');
  vbig.textContent=v;
  vbig.setAttribute('data-text',v);
  vbig.className=`verdict-big ${cls} glitch`;
  setTimeout(()=>vbig.classList.remove('glitch'),500);

  document.getElementById('conf-num').textContent=conf+'%';
  const pf=document.getElementById('prog-fill');
  pf.className=`progress-fill ${cls}`;
  pf.style.width='0%';
  setTimeout(()=>pf.style.width=conf+'%',80);

  /* Tags */
  const tags=document.getElementById('vtags');
  tags.innerHTML=`
    <div class="vtag vtag-model">PAC + TF-IDF</div>
    <div class="vtag ${v==='REAL'?'vtag-real':'vtag-fake'}">${v==='REAL'?'Authentic Signal':'Fabrication Detected'}</div>
    <div class="vtag vtag-model">Confidence ${conf}%</div>
  `;

  /* Clickbait arc */
  const arcFill=document.getElementById('arc-fill');
  const cbColor=cbR==='HIGH'?'#FF4B4B':cbR==='MODERATE'?'#FFD93D':'#00E5A0';
  arcFill.style.stroke=cbColor;
  const offset=220-(220*cb);
  arcFill.style.strokeDashoffset=220;
  setTimeout(()=>arcFill.style.strokeDashoffset=offset,100);
  document.getElementById('arc-val').textContent=cb.toFixed(2);

  const rb=document.getElementById('cb-risk-badge');
  rb.textContent=`Clickbait Risk: ${cbR}`;
  rb.className='cb-risk-badge';
  rb.style.background=cbR==='HIGH'?'rgba(255,75,75,0.12)':cbR==='MODERATE'?'rgba(255,217,61,0.12)':'rgba(0,229,160,0.12)';
  rb.style.color=cbR==='HIGH'?'var(--fake)':cbR==='MODERATE'?'var(--warn)':'var(--real)';
  rb.style.border=`1px solid ${cbR==='HIGH'?'rgba(255,75,75,0.3)':cbR==='MODERATE'?'rgba(255,217,61,0.3)':'rgba(0,229,160,0.3)'}`;
  document.getElementById('cb-desc-text').textContent=descMap[cbR];

  /* Metrics */
  const st=modelStats[v]||modelStats.REAL;
  document.getElementById('m-prec').textContent=st.prec;
  document.getElementById('m-recall').textContent=st.recall;
  document.getElementById('m-f1').textContent=st.f1;

  /* Bar chart */
  const bars=[
    {name:'Precision',val:parseFloat(st.prec),color:'var(--c)'},
    {name:'Recall',val:parseFloat(st.recall),color:'var(--c)'},
    {name:'F1-Score',val:parseFloat(st.f1),color:'var(--c)'},
    {name:'ROC-AUC',val:.981,color:'#8B5CF6'},
    {name:'Accuracy',val:.937,color:cls==='real'?'var(--real)':'var(--fake)'},
    {name:'CB F1',val:.883,color:'var(--warn)'},
  ];
  document.getElementById('bar-chart').innerHTML=bars.map(b=>`
    <div class="bar-row">
      <div class="bar-name">${b.name}</div>
      <div class="bar-track">
        <div class="bar-fill-anim" style="background:${b.color}" data-pct="${b.val*100}"></div>
      </div>
      <div class="bar-val">${b.val.toFixed(3)}</div>
    </div>`).join('');
  requestAnimationFrame(()=>{
    document.querySelectorAll('.bar-fill-anim').forEach(el=>{
      setTimeout(()=>el.style.width=el.dataset.pct+'%',100);
    });
  });

  /* Show result */
  const rs=document.getElementById('result-section');
  rs.style.display='block';
  rs.scrollIntoView({behavior:'smooth',block:'start'});

  /* History */
  const cbCls=cbR==='HIGH'?'warn':cls;
  hist.unshift({v,cls:cbCls,title:title||'(body only)',
    cb:cb.toFixed(3),conf:conf+'%'});
  if(hist.length>6) hist.pop();
  const hc=document.getElementById('hist-card');
  hc.style.display='block';
  document.getElementById('hist-list').innerHTML=hist.map(h=>`
    <div class="hist-row" role="listitem">
      <div class="hist-indicator ${h.cls}"></div>
      <div class="hist-title-text">${esc(h.title)}</div>
      <div class="hist-meta">CB ${h.cb}</div>
      <div class="hist-verdict-badge hvb-${h.cls}">${h.v}</div>
    </div>`).join('');
}

function clearAll(){
  ['title','body'].forEach(id=>{
    document.getElementById(id).value='';
    updateCount(id,id+'-count',id==='title'?200:5000);
  });
  document.getElementById('result-section').style.display='none';
}

function shake(){
  const c=document.querySelector('.card');
  let i=0;const seq=[9,-9,7,-7,4,-4,0];
  const iv=setInterval(()=>{
    c.style.transform=`translateX(${seq[i++]}px)`;
    if(i>=seq.length){clearInterval(iv);c.style.transform='';}
  },55);
}

function showShortcuts(){
  alert('Keyboard Shortcuts:\n\nA → Focus input\nD → Load demo article\nC → Clear all\nEnter → Run analysis\nCtrl+Enter → Run analysis (from textarea)');
}

function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
</script>
</body>
</html>"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    result = classify_article(data.get("title", ""), data.get("body", ""))
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
