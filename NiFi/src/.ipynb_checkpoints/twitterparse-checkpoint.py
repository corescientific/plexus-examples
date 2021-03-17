import json
from datetime import datetime
import sys

def main():

    data = " ".join(sys.stdin.readlines())
    data = json.loads(data)
    data['lat'] = eval(data['coord'])[0][0][1]
    data['lon'] = eval(data['coord'])[0][0][0]
    data['created_at'] = datetime.strptime(data['created_at'], "%a %b %d %H:%M:%S +0000 %Y").strftime('%Y-%m-%d %H:%M:%S')
    _ = data.pop('coord')
    sys.stdout.write(json.dumps(data))

if __name__ == "__main__":
    main()