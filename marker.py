import sys, os, os.path
from distance import levenshtein as strdist
from queue import PriorityQueue


def main(argv):
    if len(argv) < 2:
        usage("marker: Need some args")
    action = argv[1]
    filen = argv[2] if len(argv) > 2 else None
    if action == 'set-mark':
        set_mark(filen, os.path.abspath(os.curdir))
    elif action == 'get-mark':
        print(get_mark(filen))
    else:
        usage("What's {0} supposed to do?".format(action))

def set_mark(filen, path):
    with open(markfile(), mode='w', encoding='utf-8') as marksf:
        marks = json.load(marksf)
        marks["marks"][filen] = os.path.join(path, filen)
        marksf.seek(0)
        json.dump(marks, marksf)

def get_mark(filen):
    with open(markfile(), mode='r', encoding='utf-8') as marksf:
        marks = json.load(marksf)
        if filen in marks["marks"]:
            return marks["marks"][filen]
        else:
            pq = PriorityQueue()
            for markn in marks["marks"]:
                pq.put(strdist(filen, markn), markn)
            bestfile = pq.get()
            marks["did-you-mean"] = {"file": bestfile, "expires"
            print(("marked: No mark for {0}; " +
                "Did you mean {u}{1}{n}? ({u}marked{n})").format(
                    filen, bestfile, u='\x1b[3m', n='\x1b[0m'),
                file=sys.stderr)
            exit(-1)


if __name__=='__main__':
    main(sys.argv)
    sys.exit(0)
