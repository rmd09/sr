# ЕГЭ информатика — Вариант 7 (М. Ишимов, в PDF подписан «Вариант 3»)
#
# ===== ОТВЕТЫ =====
#  1 — 37            10 — 21              19 — 106
#  2 — yzxw          11 — 110             20 — 105 206
#  3 — 540           12 — 250             21 — 204
#  4 — 18            13 — 832             22 — 8
#  5 — 17            14 — 147             23 — 0 !!!  (в 23.txt нет вершин 286, 727, 353 —
#  6 — 60            15 — 22                         файл не от этого условия)
#  7 — 86            16 — 8197200         24 — 21
#  8 — 66393         17 — 37896 193425    26 — 34075 33415
#  9 — 8751          18 — 2420 486        27 — 84 339150
#
# 25:
#   8007237770  114389113
#   8007247772  842161
#   8007247776  128521
#   8007277706  16751629
#   8007277718  363967171
# ==================
#
# Файлы задания (3.ods, 9.ods, 17.txt, 18.ods, 22.ods, 23.txt, 24.txt, 26.txt, 27.txt)
# должны лежать рядом с этим скриптом. Нужны pandas, odfpy, lxml.

from itertools import permutations, product
from functools import lru_cache
from math import dist
import pandas as pd


# ---------- 1 ----------
def t1():
    table = {(1, 3): 2, (1, 8): 6, (2, 5): 12, (2, 8): 31, (3, 4): 35,
             (3, 6): 3, (4, 6): 5, (5, 7): 17, (6, 7): 1, (7, 8): 93}
    w = {}
    for (a, b), d in table.items():
        w[(a, b)] = w[(b, a)] = d
    graph = ['AE', 'AH', 'HC', 'HG', 'CF', 'GF', 'GB', 'ED', 'EB', 'DB']
    letters = 'ABCDEFGH'
    g = {frozenset(e) for e in graph}
    res = set()
    for p in permutations(range(1, 9)):
        m = dict(zip(letters, p))
        if all((frozenset((x, y)) in g) == ((m[x], m[y]) in w)
               for x in letters for y in letters if x < y):
            res.add(w[(m['A'], m['H'])] + w[(m['H'], m['C'])])
    return res


# ---------- 2 ----------
def t2():
    F = lambda w, x, y, z: (not w and x and y and not z) or (not w and x and y and z) \
        or (not w and x and not y and not z)
    ans = []
    for r in product([0, 1], repeat=8):
        t = [(0, r[0], r[1], 0), (r[2], 1, r[3], r[4]), (1, 0, r[5], r[6])]
        if len(set(t)) < 3:
            continue
        for p in permutations('wxyz'):
            if all(F(**dict(zip(p, row))) for row in t):
                ans.append(''.join(p))
    return set(ans)


# ---------- 3 ----------
def t3():
    x = pd.read_excel('3.ods', engine='odf', sheet_name=None)
    mv, tov, mag = x['Движение_товаров'], x['Товар'], x['Магазин']
    d = mv.merge(tov, on='Артикул').merge(mag, on='ID магазина')
    d = d[(d['Наименование товара'].str.startswith('Средство для мытья посуды'))
          & (d['Адрес'].str.contains('Мира'))
          & (d['Тип операции'] == 'Поступление')
          & (d['Дата'] >= '2023-06-07') & (d['Дата'] <= '2023-06-14')]
    ml = (d['Количество упаковок, шт.'] * d['Количество в упаковке']).sum()
    return ml / 1000


# ---------- 4 ----------
def t4():
    def fano(codes):
        return all(not b.startswith(a) for a in codes for b in codes if a != b)
    words = [''.join(p) for L in range(1, 6) for p in product('01', repeat=L)]
    best = 10 ** 9
    for a in words:
        for k in words:
            for z in words:
                c = {'Т': '1', 'Н': '011', 'А': a, 'К': k, '3': z}
                if len(set(c.values())) == 5 and fano(list(c.values())):
                    best = min(best, sum(len(c[ch]) for ch in 'КАТАНКА'))
    return best


# ---------- 5 ----------
def t5():
    for n in range(1, 1000):
        b = bin(n)[2:]
        b += bin(b.count('1') % 3)[2:]
        b += str(b.count('1') % 2)
        if int(b, 2) > 116:
            return n


# ---------- 6 ----------
def t6():
    # Повтори 7 [Вперёд 10 Направо 30 Вперёд 12 Направо 150]:
    # за 2 повтора фигура замыкается — параллелограмм
    import math
    x = y = 0.0
    ang = 90.0  # смотрит вверх
    pts = [(x, y)]
    for _ in range(7):
        for cmd, v in (('f', 10), ('r', 30), ('f', 12), ('r', 150)):
            if cmd == 'f':
                x += v * math.cos(math.radians(ang))
                y += v * math.sin(math.radians(ang))
                pts.append((round(x, 9), round(y, 9)))
            else:
                ang -= v
    poly = []
    for p in pts:
        if p not in poly:
            poly.append(p)
    s = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return int(abs(s) / 2 + 1e-9)


# ---------- 7 ----------
def t7():
    photo = 640 * 480 * 12          # 4096 цветов = 12 бит
    return 1601536 * 200 // photo


# ---------- 8 ----------
def t8():
    cnt = 0
    for d in product(range(12), repeat=5):
        if d[0] == 0:
            continue
        if d.count(3) == 1 and sum(c > 9 for c in d) <= 2:
            cnt += 1
    return cnt


# ---------- 9 ----------
def t9():
    df = pd.read_excel('9.ods', engine='odf', header=None, sheet_name=0)
    cnt = 0
    for row in df.itertuples(index=False):
        a = sorted(row)
        if (a[0] + a[-1]) ** 2 > a[1] ** 2 + a[2] ** 2 + a[3] ** 2:
            cnt += 1
    return cnt


# ---------- 10 ----------
def t10():
    from ipaddress import ip_address
    ip = int(ip_address('216.130.232.30'))
    net = int(ip_address('216.130.232.0'))
    best = 33
    for L in range(33):
        mask = (2 ** 32 - 1) ^ (2 ** (32 - L) - 1)
        if ip & mask == net:
            best = min(best, L)
    return best


# ---------- 11 ----------
def t11():
    alph = 10 + 52 + 8164
    bits = (alph - 1).bit_length()
    for L in range(1, 10000):
        byt = (L * bits + 7) // 8
        if 835 * byt > 156 * 1024:
            return L


# ---------- 12 ----------
def t12():
    tape = {i: '0' for i in range(500)}
    tape.update({i: '1' for i in range(500, 1000)})
    prog = {('q0', 'L'): ('L', 'R', 'q1'), ('q0', '1'): ('1', 'R', 'q1'),
            ('q0', '0'): ('0', 'R', 'q1'),
            ('q1', 'L'): ('L', 'S', 'q1'), ('q1', '1'): ('0', 'N', 'q0'),
            ('q1', '0'): ('1', 'R', 'q0')}   # 'L' = λ
    pos, st = -1, 'q0'
    while True:
        sym = tape.get(pos, 'L')
        w, mv, st = prog[(st, sym)]
        tape[pos] = w
        if mv == 'S':
            break
        pos += {'R': 1, 'L': -1, 'N': 0}[mv]
    return list(tape.values()).count('1')


# ---------- 13 ----------
def t13():
    def B(n):
        return int(str(n).replace('1', '3'))

    @lru_cache(None)
    def f(a, b):
        if a == b:
            return 1
        if a > b:
            return 0
        r = f(a + 1, b)
        if '1' in str(a):
            r += f(B(a), b)
        return r
    return f(10, 37) * f(37, 93)


# ---------- 14 ----------
def t14():
    base = 8 ** 368 - 8 ** 303 + 64 ** 8 + 3 * 8 ** 14

    def cnt(n):
        c = 0
        while n:
            c += n % 8 > 5
            n //= 8
        return c
    x = 1
    while cnt(base - x) >= 77:
        x += 1
    return x


# ---------- 15 ----------
def t15():
    B = lambda x: 17 <= x <= 58
    C = lambda x: 29 <= x <= 80
    pts = [i / 4 for i in range(0, 400)]
    best = 10 ** 9
    for a1 in range(0, 100):
        for a2 in range(a1, 100):
            A = lambda x: a1 <= x <= a2
            if all((B(x)) or not (C(x) and not A(x)) for x in pts):
                best = min(best, a2 - a1)
    return best


# ---------- 16 ----------
def t16():
    F = {1: 1}
    for n in range(2, 2026):
        F[n] = 2 * n * F[n - 1]
    from fractions import Fraction
    return Fraction(F[2025], Fraction(F[2024], 4048) + F[2023])


# ---------- 17 ----------
def t17():
    a = [int(s) for s in open('17.txt')]
    m = min(x for x in a if 100 <= x <= 999 and x % 10 == 3)
    res = [abs(x - y) for x, y in zip(a, a[1:]) if x != y and abs(x - y) >= m]
    return len(res), max(res)


# ---------- 18 ----------
def t18():
    import zipfile
    from lxml import etree
    TBL = '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}'
    STY = '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}'
    FO = '{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}'
    OFF = '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}'
    root = etree.fromstring(zipfile.ZipFile('18.ods').read('content.xml'))
    borders = {}
    for s in root.iter(STY + 'style'):
        p = s.find(STY + 'table-cell-properties')
        if p is None:
            continue
        borders[s.get(STY + 'name')] = {side for side in ('top', 'bottom', 'left', 'right')
                                        if 'thick' in (p.get(FO + 'border-' + side) or '')}
    grid, walls = [], []
    for row in root.iter(TBL + 'table'):
        for r in row.iter(TBL + 'table-row'):
            vals, ws = [], []
            for c in r:
                v = c.get(OFF + 'value')
                if v is None:
                    continue
                vals.append(int(float(v)))
                ws.append(borders.get(c.get(TBL + 'style-name'), set()))
            if vals:
                grid.append(vals)
                walls.append(ws)
        break
    n = len(grid)

    def can_right(i, j):
        return j + 1 < n and 'right' not in walls[i][j] and 'left' not in walls[i][j + 1]

    def can_down(i, j):
        return i + 1 < n and 'bottom' not in walls[i][j] and 'top' not in walls[i + 1][j]

    NEG = None
    mx = [[NEG] * n for _ in range(n)]
    mn = [[NEG] * n for _ in range(n)]
    mx[0][0] = mn[0][0] = grid[0][0]
    for i in range(n):
        for j in range(n):
            if mx[i][j] is None:
                continue
            for (a, b, ok) in ((i, j + 1, can_right(i, j)), (i + 1, j, can_down(i, j))):
                if ok:
                    mx[a][b] = max(mx[a][b] if mx[a][b] is not None else -1, mx[i][j] + grid[a][b])
                    mn[a][b] = min(mn[a][b] if mn[a][b] is not None else 10 ** 9, mn[i][j] + grid[a][b])
    ends = [(i, j) for i in range(n) for j in range(n)
            if mx[i][j] is not None and not can_right(i, j) and not can_down(i, j)]
    return max(mx[i][j] for i, j in ends), min(mn[i][j] for i, j in ends)


# ---------- 19–21 ----------
TARGET = 431


def moves(h):
    a, b = h
    return [(a + 2, b), (a * 2, b), (a, b + 2), (a, b * 2)]


@lru_cache(None)
def game(h):
    # >0: выигрывает ходящий за game ходов; <0: проигрывает
    if sum(h) >= TARGET:
        return 0
    r = [game(m) for m in moves(h)]
    neg = [x for x in r if x <= 0]
    if neg:
        return -max(neg) + 1
    return -max(r)


def t19():
    for s in range(1, 422):
        if any(game(m) == 1 for m in moves((9, s)) if sum(m) < TARGET):
            return s


def t20():
    return [s for s in range(1, 422) if game((9, s)) == 2][:2]


def t21():
    for s in range(1, 422):
        if game((9, s)) == -2:
            return s


# ---------- 22 ----------
def t22():
    df = pd.read_excel('22.ods', engine='odf')
    t = {}
    dep = {}
    for _, r in df.iterrows():
        i = int(r.iloc[0])
        t[i] = int(r.iloc[1])
        dep[i] = [int(x) for x in str(r.iloc[2]).replace(' ', '').split(';') if int(x) != 0]

    @lru_cache(None)
    def fin(i):
        return t[i] + max((fin(d) for d in dep[i]), default=0)
    m = max(fin(i) for i in t)
    return max(i for i in t if fin(i) == m)


# ---------- 23 ----------  !!! вершин 286/727/353 в файле нет, программа честно даёт 0
def t23():
    g = {}
    for line in open('23.txt'):
        if line.split():
            a, b = map(int, line.split())
            g.setdefault(a, []).append(b)

    @lru_cache(None)
    def paths(a, b):
        if a == b:
            return 1
        return sum(paths(c, b) for c in g.get(a, []))
    return paths(286, 727) * paths(727, 353)


# ---------- 24 ----------
def t24():
    s = open('24.txt').read().strip()
    D, S = '03', '+-'
    best = 0
    i, n = 0, len(s)
    while i < n:
        # максимальный участок с чередованием цифра/знак
        j = i + 1
        while j < n and ((s[j] in D) != (s[j - 1] in D)):
            j += 1
        st = i
        if s[st] in S:
            if st + 1 < j and s[st + 1] == '0':   # у нуля нет знака
                st += 1
        en = j
        if s[en - 1] in S:
            en -= 1
        if en > st and s[st] in D or (en - st >= 2 and s[st] in S):
            best = max(best, en - st)
        i = j
    return best


# ---------- 25 ----------
def t25():
    def prime_divs(n):
        ps, d, m = [], 2, n
        while d * d <= m:
            if m % d == 0:
                ps.append(d)
                while m % d == 0:
                    m //= d
            d += 1 if d == 2 else 2
        if m > 1 and m != n:
            ps.append(m)
        return ps

    def is_prime(n):
        if n < 2:
            return False
        d = 2
        while d * d <= n:
            if n % d == 0:
                return False
            d += 1
        return True

    def cnt777(n):
        s = str(n)
        return sum(s[i:i + 3] == '777' for i in range(len(s) - 2))

    res = []
    n = 8007209180
    while len(res) < 5:
        n += 1
        if cnt777(n) != 1:
            continue
        ps = prime_divs(n)
        M = min(ps) + max(ps) if ps else 0
        if M > 100000 and is_prime(M):
            res.append((n, M))
    return res


# ---------- 26 ----------
def t26():
    f = open('26.txt')
    N, M, K = map(int, f.readline().split())
    occ = {}
    for _ in range(N):
        r, c = map(int, f.readline().split())
        occ.setdefault(c, []).append(r)
    best = (-1, 0)  # (кол-во свободных перед местом, -ряд)
    for c in range(1, K + 1):
        rows = [0] + sorted(occ.get(c, [])) + [M + 1]
        for a, b in zip(rows, rows[1:]):
            if b - a >= 2:                 # есть свободные ряды a+1..b-1
                seat = b - 1
                free = b - a - 2
                best = max(best, (free, -seat))
    return -best[1], best[0]


# ---------- 27 ----------
def t27():
    P = []
    for line in open('27.txt'):
        p = line.replace(',', '.').split()
        if len(p) < 6:
            continue
        x, y, vx, vy, m = map(float, p[:5])
        P.append((x, y, m * (vx * vx + vy * vy) / 2, p[5]))
    P.sort(key=lambda q: q[2])
    gaps = sorted(range(1, len(P)), key=lambda i: P[i][2] - P[i - 1][2])[-4:]
    cuts = [0] + sorted(gaps) + [len(P)]
    cl = [P[a:b] for a, b in zip(cuts, cuts[1:])]
    assert all(c[-1][2] - c[0][2] <= 3.11 for c in cl)
    centers = [min(c, key=lambda p: sum(abs(p[2] - q[2]) for q in c)) for c in cl]
    q1 = min(dist(a[:2], b[:2]) for c in cl for a in c for b in c
             if a is not b and a[3] == b[3] == 'IV' and dist(a[:2], b[:2]) > 0)
    q2 = min(c[2] for c in centers)
    return int(q1 * 10000), int(q2 * 10000)


if __name__ == '__main__':
    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
              19, 20, 21, 22, 23, 24, 25, 26, 27]:
        print(k, globals()[f't{k}']())
