import json,sys
d=json.load(open(sys.argv[1]+'/music_views/per_second_levels.json'))
def f(x,th): return '#' if x>th else '.'
print('t   mix   wid  V  D  B  O   (V>-40,D>-45,B>-45,O>-45)')
for r in d:
    print(f"{r['t']//60}:{r['t']%60:02d} {r['dbfs']:6.1f} {r['width']:.2f} {f(r['vocals'],-40)}{f(r['drums'],-45)}{f(r['bass'],-45)}{f(r['other'],-45)} V{r['vocals']:.0f} D{r['drums']:.0f} B{r['bass']:.0f} O{r['other']:.0f}")
