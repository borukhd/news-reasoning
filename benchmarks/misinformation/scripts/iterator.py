
count = 0
keys = []
linenumber = 0
perHeadline = {}
indFirst = {}
linePerName = {}
with open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/pretest/pretest3.csv') as lines:
    for line in lines:
        linenumber += 1
        listLine = line.replace('\r','').replace('\n','').split(',')
        listLine = [a.replace(';',',') for a in listLine]
        if linenumber == 1:
            firstLine = line[:-1]
            count = 0
            for key in listLine:
                indFirst[key] = count
                count += 1
                keys.append(key)
        else:
            headline = listLine[indFirst['ItemNum']]#listLine[indFirst['Headline']].partition('_')[2].partition('.')[0].replace('-','').replace(';',',').lower()
            if headline not in perHeadline.keys():
                perHeadline[headline] = {}
                for key in keys:
                    if 'amiliarity' in key:
                        perHeadline[headline][key] = str(4.0 - float(listLine[indFirst[key]]))
                    else:
                        perHeadline[headline][key] = listLine[indFirst[key]]
            if headline not in linePerName.keys():
                linePerName[headline] = line[:-1]


keys = []
ind = {}
count = 0
counter = 0
output = open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/Study11dataReshaped.csv', "w+")
with open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study1/st1.csv') as lines:
    line1 = True
    for line in lines:
        listLine = line.replace('\r','').replace('\n','').split(',')
        if line1:
            line1 = False
            for key in listLine:
                ind[key] = count
                count += 1
                division = key.split('_')[0]
                division = key[:4]
                if ('Fake' in division or 'Real' in division) and not 'N' in key[:5] and len(key)>4:
                    found = False
                    for a in keys:
                        if a[0].split('_')[0] == key.split('_')[0]:
                            a.append(key)
                            found = True
                    if not found:# and not key == ' ':
                        keys.append([key])
                else:
                    keys.append([key])
            keys = sorted(keys, key=len)
            reversed(keys)
            #output.write(str(keys).replace('[','').replace(']','').replace(' ','').replace(',',''))
            outheader = 'task,_C,_L,_N,trial,sequence,choices,response,binaryResponse,responseCorrect,truthful,domain,response_type,'
            donekeys = []
            for key in keys: 
                if len(key) > 1:
                    for a in key:
                        if str(a.split('_')[1:]) not in donekeys:
                            for f in a.split('_')[1:]:
                                if f not in  ['C','L','N']:
                                    outheader += '_' + f 
                            outheader += ','
                            donekeys.append(str(a.split('_')[1:]))
            outheader = outheader[:-2]
            for key in keys: 
                if len(key) == 1:
                    outheader += key[0] + ','
            output.write(outheader + firstLine + '\n')
        else:
            outline = ''
            for key in keys:
                if len(key) == 1:
                    outline += listLine[ind[key[0]]] + ','
            doubleKeys = []
            for key in keys:
                #allkeys = 
                if len(key) > 1:
                    doubleKeys.append(key)
            for key in doubleKeys:
                trials= listLine[ind['DO_BR_FL_88']]
                newsItem = key[0].split('_')[0]
                specout = newsItem
                for f in  ['_C','_L','_N']:
                    puzzled =newsItem + f
                    put = listLine[ind[puzzled]] if puzzled in ind else '0'
                    specout += ',' + put
                trialList = [n.replace('-',' ').split(' ')[0].replace('ake','Fake').replace('FF','F').replace('Fae','Fake').replace('e0','e10').replace('ea','Real').replace('ll','l').replace('RR','R').replace('Fak','Fake').replace('kk','k').replace('ee','e').replace('Ra','Rea').replace('Rea1','Real1')
                    for n in trials.replace('lR','l|R').replace('lF','l|F').replace('eF','e|F').replace('eR','e|R').split('|')]
                replace = False
                append = False
                for a in trialList: 
                    if trialList.count(a) > 1:
                        replace = True
                    if len(a)==4:
                        append = True
                if replace:
                    trialList = trialList[:14] + [trialList[14][:-2]+'1'+trialList[14][-1]] +trialList[15:]
                if append:
                    trialList = trialList[:14] + [trialList[14]+'1'] +trialList[15:]

                index = str(trialList.index(newsItem)) if newsItem in trialList else '14' #+ str(any(char for char in trialList[14] if char not in newsItem))
                if 'e' in index:
                    print(index,trialList)
                    counter += 1
                    for a in trialList: 
                        if trialList.count(a) > 1:
                            print('twice', index, a, listLine[0], trialList)

                specout += (',' + index)*2
                accurate = '1' in listLine[ind[newsItem + '_Accurate']]
                responseCorrect = (accurate and 'R' in newsItem) or (not accurate and 'F' in newsItem)
                stringbel = '1' if 'R' in newsItem else '0'
                ccspecs = ',Accept|Reject,' + str('Accept' if accurate else 'Reject')+ ',' +str('1' if accurate else '0') + ',' +str('1' if responseCorrect else '0') +',' + stringbel + ',misinformation,single-choice,'
                for a in key: 
                    ccspecs += listLine[ind[a]] + ','
                outstring =  specout+ ccspecs +outline 
                if 'N' in key[0]:
                    pretestsuffix = ''
                    for i in range(firstLine.count(',')):
                        pretestsuffix += ','
                else:
                    pretestsuffix = linePerName[key[0]]
                finalstring = outstring  + pretestsuffix + '\n'
                output.write(finalstring )#.replace(',,',',-9999,').replace(',,',',-9999,'))
                #print(outline + specout)
output.close()
print(counter)
