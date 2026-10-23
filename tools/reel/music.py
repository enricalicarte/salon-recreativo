#!/usr/bin/env python3
"""Pista synthwave 120 BPM sincronizada con la línea de tiempo del reel."""
import numpy as np, wave, sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/af2b990b-fbcc-57a3-9b7e-c5746bcaaae9/scratchpad/reel')
from render import SEQ, TOTAL, FPS, BEAT
SR = 44100; BPM = 120; B = 60 / BPM
DUR = TOTAL / FPS + 0.5
N = int(SR * DUR); t = np.arange(N) / SR
mix = np.zeros(N)
rng = np.random.default_rng(3)

def place(sig, at):
    i = int(at * SR); j = min(N, i + len(sig))
    if i < N: mix[i:j] += sig[:j - i]

def env(n, a, d, s=0.0, r=0.05, sus=0.0):
    e = np.zeros(n); A, D, R = int(a * SR), int(d * SR), int(r * SR)
    e[:A] = np.linspace(0, 1, A)
    e[A:A + D] = np.linspace(1, s, D)
    e[A + D:] = s
    if R and R < n: e[-R:] *= np.linspace(1, 0, R)
    return e

def kick(v=1.0):
    n = int(.35 * SR); tt = np.arange(n) / SR
    f = 42 + 120 * np.exp(-tt * 28)
    return v * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)

def hat(v=.35, op=False):
    n = int((.25 if op else .06) * SR)
    return v * rng.standard_normal(n) * np.exp(-np.arange(n) / SR * (14 if op else 90))

def snare(v=.6):
    n = int(.22 * SR); tt = np.arange(n) / SR
    return v * (rng.standard_normal(n) * np.exp(-tt * 18) * .7 + np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 30))

def saw(f, n, det=.006):
    tt = np.arange(n) / SR; s = np.zeros(n)
    for k in (-1, 0, 1):
        ph = (tt * f * (1 + det * k)) % 1; s += 2 * ph - 1
    return s / 3

def bass(f, dur, v=.5):
    n = int(dur * SR); s = saw(f, n, .003) * env(n, .005, .12, .6, .04)
    # filtro simple (media móvil) para suavizar
    k = 24; s = np.convolve(s, np.ones(k) / k, 'same'); return v * s

def lead(f, dur, v=.22):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = (saw(f, n, .01) * .6 + np.sin(2 * np.pi * f * 2 * tt) * .3) * env(n, .01, .15, .5, .08)
    s = np.convolve(s, np.ones(10) / 10, 'same'); return v * s

def pad(freqs, dur, v=.12):
    n = int(dur * SR); tt = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        s += saw(f, n, .012) + .4 * np.sin(2 * np.pi * f * tt + .5 * np.sin(2 * np.pi * .3 * tt))
    s = np.convolve(s, np.ones(40) / 40, 'same')
    return v * s / len(freqs) * env(n, .6, .2, .9, .6)

def riser(dur, v=.5):
    n = int(dur * SR); tt = np.arange(n) / SR
    noise = rng.standard_normal(n); k = 6
    noise = noise - np.convolve(noise, np.ones(k) / k, 'same')  # agudos
    return v * noise * (tt / dur) ** 2.5

def impact(v=.9):
    n = int(1.2 * SR); tt = np.arange(n) / SR
    return v * (np.sin(2 * np.pi * (55 + 40 * np.exp(-tt * 6)) * tt) * np.exp(-tt * 3) + rng.standard_normal(n) * np.exp(-tt * 12) * .4)

# acordes (Am – F – C – G) en Hz, una progresión por 4 compases
A = lambda m, o=0: 440 * 2 ** ((m - 9) / 12 + o)  # m = semitono desde C
CHORDS = [([9, 12, 16], 9), ([5, 9, 12], 5), ([0, 4, 7], 0), ([7, 11, 14], 7)]  # (triada, bajo)
MEL = [9, 12, 16, 14, 12, 9, 7, 9, 12, 16, 19, 16, 14, 12, 9, 7]

# secciones (en beats)
starts = {s['kind'] + str(s.get('idx', '')): s['start'] / FPS for s in SEQ}
intro_end = SEQ[1]['start'] / FPS
cam_start = [s for s in SEQ if s['kind'] == 'title' and s['idx'] == 4][0]['start'] / FPS
grid_start = [s for s in SEQ if s['kind'] == 'grid'][0]['start'] / FPS
outro_start = [s for s in SEQ if s['kind'] == 'outro'][0]['start'] / FPS
end = TOTAL / FPS

total_beats = int(end / B) + 1
for b in range(total_beats):
    tb = b * B; bar = b // 4; beat = b % 4
    chord, root = CHORDS[bar % 4]
    full = tb >= intro_end and tb < outro_start + 2 * B
    # pad siempre (más suave en intro)
    if beat == 0:
        place(pad([A(m, -1) for m in chord] + [A(chord[0], 0)], 4 * B, .10 if tb < intro_end else .14), tb)
    if tb < intro_end:
        if beat in (0, 2): place(kick(.6), tb)
        continue
    if tb >= outro_start + 2 * B:
        if beat == 0 and bar % 2 == 0: place(kick(.5), tb)
        continue
    place(kick(1.0), tb)
    if beat in (1, 3): place(snare(.5), tb)
    for h in range(2):
        place(hat(.3 if h == 0 else .18), tb + h * B / 2)
    if beat == 3: place(hat(.25, True), tb + B * .75)
    # bajo: corcheas con octava
    for e in range(2):
        f = A(root, -2) * (2 if e == 1 and beat % 2 == 1 else 1)
        place(bass(f, B / 2 * .9, .45), tb + e * B / 2)
    # melodía a partir del capítulo 1 (cada 2 compases) y más densa en cámara
    if tb >= cam_start - 8 * B:
        m = MEL[(b * 2) % len(MEL)]; place(lead(A(m, 0), B * .9, .2), tb)
        m2 = MEL[(b * 2 + 1) % len(MEL)]; place(lead(A(m2, 0), B * .45, .16), tb + B / 2)
    elif b % 2 == 0:
        m = MEL[(b // 2) % len(MEL)]; place(lead(A(m, 0), B * 1.8, .18), tb)

# risers e impactos en cada título de capítulo + grid + outro
for s in SEQ:
    if s['kind'] in ('title', 'grid', 'outro'):
        ts = s['start'] / FPS
        place(riser(1.5, .35), ts - 1.5); place(impact(.8 if s['kind'] != 'outro' else 1.0), ts)
place(impact(.7), 0.0)
# whoosh/clic sutil en cada corte de clip
for s in SEQ:
    if s['kind'] == 'clip':
        place(hat(.5, True) * .6, s['start'] / FPS)

# master: suave saturación, fade out final
mix = np.tanh(mix * 1.1) * .85
fo = int(2.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
mix = np.clip(mix, -1, 1)
with wave.open(f'/tmp/claude-0/-home-claude/af2b990b-fbcc-57a3-9b7e-c5746bcaaae9/scratchpad/reel/music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    st = np.stack([mix, mix], 1); w.writeframes((st * 32767).astype(np.int16).tobytes())
print('music ok', DUR)
