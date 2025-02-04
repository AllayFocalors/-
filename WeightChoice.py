import random as r
def GetConfig():
    global ready
    with open('config.txt','r',encoding='utf-8') as f:
        config = f.read()
        config = config.split('''\n''')
    return config

def Choice(config,Chosen,quan):
    if len(Chosen) <= quan:    
        ready = []
        for i in config:
            if i.split(' ')[0] in Chosen:
                continue
            else:
                for j in range(int(i.split(' ')[1])):
                    ready.append(i.split(' ')[0])
        # print(ready)
        if len(ready)>1:
            rNum = r.randint(0,len(ready)-1)
        else:
            rNum = 0
        
        if ready[rNum] in Chosen:
            print(f'重复,{ready[rNum]},{Chosen}')
            # print(f'Choice(Choice,{Chosen},{quan})')
            return Choice(config,Chosen,quan)
            
        else:
            return ready[rNum]
    else:
        return '已抽完'
