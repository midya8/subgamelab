import argparse,json,sys
from .engine import solve
from .verify import verify
from .schema import loads

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['solve','verify']);p.add_argument('path',nargs='?',default='-');a=p.parse_args()
    try:
        text=sys.stdin.read() if a.path=='-' else open(a.path).read();x=loads(text)
        out=solve(x) if a.command=='solve' else {'valid':verify(x)}
        print(json.dumps(out,sort_keys=True,separators=(',',':')))
    except (ValueError,KeyError,TypeError,OSError) as e:print(str(e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
