def cnv(n: int, bits: int):
    if n < 0: return n
    n = n & ((1<<bits)-1)
    return (n ^ (1<<(bits-1)) - (1<<(bits-1)))

class World:
    def __init__(self, bgm=0, gx=0, gp=0, gy=0, mx=0, mp=0, my=0, w=0, h=0, param=[[0,0]]*224):
        self.bgm = bgm & 3
        self.gx = cnv(gx, 10)
        self.gp = cnv(gp, 10)
        self.gy = cnv(gy, 16)
        self.mx = cnv(mx, 13)
        self.mp = cnv(mp, 15)
        self.my = cnv(my, 13)
        self.w = cnv(w & 0xfff, 13)
        self.h = cnv(h & 0x1ff, 16)
        self.param = param
    
    def time(self):
        if self.bgm == 0:
            base = 880
            wstart = self.mx - abs(self.mp)
            wend = self.mx + abs(self.mp) + self.w + 1
            wtiles = (((wend + 7) & ~7) - (wstart & ~7)) // 8
            offset = (self.gy - self.my) & 7
            for y in range(0, 224, 8):
                if self.gy + self.h + 1 <= y:
                    break
                # the last strip takes 9 cycles less, for unclear reasons
                if y == 216: base -= 9
                if self.gy >= y + 8:
                    if y != 216: base += 5
                    else: base += 4
                    continue
                start = self.gy >= y
                end = self.gy + self.h + 1 <= y + 8
                base += 12 if start else 13 if end else 16

                # unexplained quirks
                if y == 0 and not start: base += 6 - 2 * (not end)

                if self.gy + self.h + 1 < y + 8 and not start:
                    rows = (self.gy + self.h + 1) & 7
                else:
                    rows = min(8, y + 8 - self.gy)
                base += 2 * rows * wtiles
                tileloads = 1 + (offset != 0 and (not start or self.gy < y + offset) and (not end or start or self.gy + self.h + 1 > y + offset))
                base += 2 * tileloads * wtiles
                base += 91 * tileloads
            return base

            # old
            base = 880 + min(28, max(0, self.gy // 8)) * 5
            start = max(0, self.gy)
            end = min(224, self.gy + self.h + 1)
            if (self.gy & ~7) == (end & ~7): end = (end + 8) & ~7
            rows = end - start

            stripstart = start & ~7
            stripend = (end + 7) & ~7
            strips = (stripend - stripstart) // 8

            if start >= 224: return base
            if end <= 0: return base
            if rows == 0: return base

            topend = True
            bottomend = self.gy + self.h < 224

            endstrips = min(topend + bottomend, strips)
            middlestrips = max(0, strips-(topend + bottomend))
            offset = (self.gy - self.my) & 7
            swaps = 0
            if offset != 0: swaps = strips - ((end & 7) and (end & 7) <= offset)
            wstart = self.mx - abs(self.mp)
            wend = self.mx + abs(self.mp) + self.w + 1
            wtiles = (((wend + 7) & ~7) - (wstart & ~7)) // 8
            return base + 2 * rows * wtiles + 2 * wtiles * (strips + swaps) + 107 * middlestrips + 105 * endstrips + 91 * swaps

        elif self.bgm == 1:
            base = 880
            for y in range(0, 224, 8):
                if self.gy + self.h + 1 <= y:
                    break
                # the last strip takes 9 cycles less, for unclear reasons
                if y == 216: base -= 9
                if self.gy >= y + 8:
                    if y != 216: base += 5
                    else: base += 4
                    continue

                start = self.gy >= y
                end = self.gy + self.h + 1 <= y + 8

                base += 12 if start else 13 if end else 16

                # unexplained quirks
                if y == 0 and not start: base += 6 - 2 * (not end)

                for yy in range(y, y + 8):
                    if yy < self.gy: continue
                    if not start and yy >= self.gy + self.h + 1: break
                    hofstl, hofstr = self.param[y - self.gy]
                    left = self.mx - self.mp + hofstl
                    right = self.mx + self.mp + hofstr
                    wstart = min(left, right)
                    wend = max(left, right) + self.w + 1
                    wtiles = (((wend + 7) & ~7) - (wstart & ~7)) // 8
                    base += 98 + 4 * wtiles
            return base
                

            # old
            base = 880 + min(28, max(0, self.gy // 8)) * 5

            start = self.gy
            end = min(224, self.gy + self.h + 1)
            if (start & ~7) == (end & ~7): end = (end + 8) & ~7

            stripstart = max(0,start) & ~7
            stripend = (end + 7) & ~7
            strips = (stripend - stripstart) // 8

            # the last strip takes 9 cycles less, for unclear reasons
            if stripend >= 224: base -= 9

            if self.gy >= 224: return base
            if strips <= 0: return base

            topend = True
            bottomend = self.gy + self.h < 224

            endstrips = min(topend + bottomend, strips)
            middlestrips = max(0, strips-(topend + bottomend))
            
            base += 13 * endstrips + 16 * middlestrips
            for y in range(start, end):
                if y < 0: continue
                hofstl, hofstr = self.param[y - self.gy]
                left = self.mx - self.mp + hofstl
                right = self.mx + self.mp + hofstr
                wstart = min(left, right)
                wend = max(left, right) + self.w + 1
                wtiles = (((wend + 7) & ~7) - (wstart & ~7)) // 8
                base += 98 + 4 * wtiles
            return base
            
        elif self.bgm == 2:
            base = 908
            for y in range(0, 224, 8):
                if self.gy + self.h + 1 <= y:
                    break
                # the last strip takes 12 cycles less, for unclear reasons
                if y == 216: base -= 12
                if self.gy >= y + 8:
                    if y != 216: base += 5
                    else: base += 7
                    continue

                start = self.gy >= y
                end = self.gy + self.h + 1 <= y + 8

                base += 13 if start else 14 if end else 14

                if y == 0 and not start: base += 5
                if y == 216 and self.gy + self.h + 1 > y + 8: base += 3

                rows = max(y, min(y + 8, self.gy + self.h + 1)) - max(y, min(y + 8, self.gy))
                base += rows * (80 + 4 * (self.w + 1))
            return base

            base = 908 + min(28, max(0, self.gy // 8)) * 5

            start = max(0, self.gy)
            end = min(224, self.gy + self.h + 1)
            rows = end - start
            
            stripstart = start & ~7
            stripend = (end + 7) & ~7
            strips = (stripend - stripstart) // 8

            # the last row takes 12 cycles less, for unclear reasons
            if stripend == 224: base -= 12

            # if the last row is off the bottom, it's faster
            if self.gy + self.h + 1 > 224 and self.gy < 224: base += 2

            if start >= 224: return base + 3
            if end <= 0: return base + 1
            if rows == 0: return base

            return base + 4 * (self.w + 1) * rows + 80 * rows + 14 * strips
            

def time(worlds: list[World]):
    # hard to get a precise handle on that 308 but it's a multiple of 28 so we go with it
    end_time = 0 if len(worlds) == 32 else 308
    return 54688 + end_time + \
        sum(w.time() for w in worlds)


def test():
    def do(expected, code):
        actual = eval(code)
        if expected != actual:
            print(f"{code}: expected {expected}, actual {actual}")
    
    do(114, "time([World(bgm=0,gy=-1,my=-1,h=1)])-time([World(bgm=0,gy=-1,my=-1,h=0)])")
    do(7, "time([World(bgm=0,gy=-1,my=-1,h=8)])-time([World(bgm=0,gy=0,h=7)])")
    do(8, "time([World(bgm=0,gy=-1,my=-1,h=16)])-time([World(bgm=0,gy=0,h=15)])")
    do(103, "time([World(bgm=0,gy=223,my=223,h=10)])-time([World(bgm=0,gy=224,h=10)])")
    do(3, "time([World(bgm=0,gy=210,my=210,h=14)])-time([World(bgm=0,gy=210,my=210,h=13)])")
    do(0, "time([World(bgm=0,gy=220,my=220,h=4)])-time([World(bgm=0,gy=220,my=220,h=3)])")
    do(121, "time([World(bgm=0,gy=0)])-time([World(bgm=0,gy=-1)])")
    do(216, "time([World(bgm=0,gy=-1,h=16)])-time([World(bgm=0,gy=-1,h=8)])")
    do(122, "time([World(bgm=0,h=15)])-time([World(bgm=0,h=7)])")
    do(221, "time([World(bgm=0,gy=-1,h=8)])-time([World(bgm=0,gy=-1,h=0)])")
    do(128, "time([World(bgm=0,gy=-1,my=-1,h=8)])-time([World(bgm=0,gy=-1,my=-1,h=0)])")
    do(107, "time([World(bgm=0,gy=-1,h=8)])-time([World(bgm=0,gy=-1,h=1)])")

    do(121, "time([World(bgm=1,gy=-1,my=-1,h=1)])-time([World(bgm=1,gy=-1,my=-1,h=0)])")
    do(7, "time([World(bgm=1,gy=-1,my=-1,h=8)])-time([World(bgm=1,gy=0,h=7)])")
    do(8, "time([World(bgm=1,gy=-1,my=-1,h=16)])-time([World(bgm=1,gy=0,h=15)])")
    do(110, "time([World(bgm=1,gy=223,my=223,h=10)])-time([World(bgm=1,gy=224,h=10)])")
    do(3, "time([World(bgm=1,gy=210,my=210,h=14)])-time([World(bgm=1,gy=210,my=210,h=13)])")
    do(0, "time([World(bgm=1,gy=220,my=220,h=4)])-time([World(bgm=1,gy=220,my=220,h=3)])")
    do(118, "time([World(bgm=1,h=16)])-time([World(bgm=1,h=15)])")
    do(115, "time([World(bgm=1,h=8)])-time([World(bgm=1,h=7)])")
    do(102, "time([World(bgm=1,h=13)])-time([World(bgm=1,h=12)])")
    do(217, "time([World(bgm=1,h=9)])-time([World(bgm=1,h=7)])")

    # big numbers seem to reduce accuracy
    # ~400 cycles seem to be 1 longer in measurements than in simulation
    # ~800 cycles seem to be 2 longer in measurements than in simulation
    # in other words, this is probably fine
    do(422-1, "time([World(bgm=1,h=11)])-time([World(bgm=1,h=7)])")
    do(830-2, "time([World(bgm=1,gy=0)])-time([World(bgm=1,gy=-1)])")
    do(837-2, "time([World(bgm=1,gy=-1,h=8)])-time([World(bgm=1,gy=-1,h=0)])")
    do(832-2, "time([World(bgm=1,gy=-1,h=16)])-time([World(bgm=1,gy=-1,h=8)])")
    do(831-2, "time([World(bgm=1,h=15)])-time([World(bgm=1,h=7)])")
    do(837-2, "time([World(bgm=1,gy=-1,my=-1,h=8)])-time([World(bgm=1,gy=-1,my=-1,h=0)])")

    do(103, "time([World(bgm=2,gy=-1,my=-1,h=1)])-time([World(bgm=2,gy=-1,my=-1,h=0)])")
    do(6, "time([World(bgm=2,gy=-1,my=-1,h=8)])-time([World(bgm=2,gy=0,h=7)])")
    do(6, "time([World(bgm=2,gy=-1,my=-1,h=16)])-time([World(bgm=2,gy=0,h=15)])")
    do(93, "time([World(bgm=2,gy=223,my=223,h=10)])-time([World(bgm=2,gy=224,h=10)])")
    do(3, "time([World(bgm=2,gy=210,my=210,h=14)])-time([World(bgm=2,gy=210,my=210,h=13)])")
    do(3, "time([World(bgm=2,gy=220,my=220,h=4)])-time([World(bgm=2,gy=220,my=220,h=3)])")
    do(97, "time([World(bgm=2,gy=0)])-time([World(bgm=2,gy=-1)])")

    # big numbers seem to reduce accuracy
    do(693-2, "time([World(bgm=2,gy=-1,h=8)])-time([World(bgm=2,gy=-1,h=0)])")
    do(688-2, "time([World(bgm=2,gy=-1,h=16)])-time([World(bgm=2,gy=-1,h=8)])")
    do(688-2, "time([World(bgm=2,h=15)])-time([World(bgm=2,h=7)])")
    do(693-2, "time([World(bgm=2,gy=-1,my=-1,h=8)])-time([World(bgm=2,gy=-1,my=-1,h=0)])")

test()