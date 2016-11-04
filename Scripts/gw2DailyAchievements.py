import urllib.request
import json

items = json.loads(
    urllib.request.urlopen(r'https://api.guildwars2.com/v2/achievements/daily').read().decode('UTF-8')
)
count = 0
for eventType in items.keys():
    for event in items[eventType]:
        buf = json.loads(
            urllib.request.urlopen(
                r'https://api.guildwars2.com/v2/achievements?ids=' + str(event['id'])
            ).read().decode('UTF-8')
        )
        for a in buf:
            for b in a.keys():
                event.setdefault(b, a[b])
        for a in event['rewards']:
            buf = json.loads(
                urllib.request.urlopen(
                    r'https://api.guildwars2.com/v2/items/' + str(a['id'])
                ).read().decode('UTF-8')
            )
            event['rewards'].pop(
                event['rewards'].index(a)
            )
            event['rewards'].append(buf)
        buf = items[eventType].index(event)
        items[eventType].pop(buf)
        items[eventType].insert(buf,event)
        count += 1
        print('Loaded: '+str(count)+' events')
print(items)
