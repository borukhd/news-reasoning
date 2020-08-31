
count = 0
keys = []
linenumber = 0
perHeadline = {}
indFirst = {}
with open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/pretest/pretest3.csv') as lines:
    for line in lines:
        linenumber += 1
        listLine = line.replace('\r','').replace('\n','').split(',')
        listLine = [a.replace(';',',') for a in listLine]
        if linenumber == 1:
            count = 0
            for key in listLine:
                indFirst[key] = count
                count += 1
                keys.append(key)
        else:
            if listLine[indFirst['Study']] != '1':
                continue
            headline = listLine[indFirst['ItemNum']].split('_')[0]#listLine[indFirst['Headline']].partition('_')[2].partition('.')[0].replace('-','').replace(';',',').lower()
            if headline not in perHeadline.keys():
                perHeadline[headline] = {}
                for key in keys:
                    if 'F_' in key:
                        perHeadline[headline][key] = str(5.0 - float(listLine[indFirst[key]]))
                    else:
                        perHeadline[headline][key] = listLine[indFirst[key]]


keys = []
keysComb = []
indFirst = {}
indComb = {}
count = 0
counter = 0
donekeys = []
trialspec = []
output = open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/Study11dataReshaped.csv', "w+")
with open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study1/st1.csv') as lines:
    headlineKeys = ''
    line1 = True
    line2 = True
    for line in lines:
        listLine = line.replace('\r','').replace('\n','').replace("What type of social media accounts do you use (if any)?","accounts").replace("We are also interested in your *past* political preferences. Please select any of the following...","pastPolitical").replace("Would you consider sharing this story online (for example, through Facebook or Twitter)?","sharingContent").replace("Which of these types of content would you consider sharing on social media (if any)?","sharingType").replace("To the best of your knowledge, is the claim in the above headline accurate?","accurate").split(',')
        if line1:
            line1 = False
            for key in listLine:
                indFirst[key] = count
                keys.append(key)
                if key not in keys:
                    key = keys[count] + '_' 
                    key += listLine[count]
                if key not in indComb:
                    indComb[key] = []
                indComb[key].append(count)
                count += 1
                division = key.split('_')[0]
                division = key[:4]
                if 'DO' in key:
                    continue
                if ('Fake' in division or 'Real' in division) and not 'N' in key[:5] and len(key)>4:
                    found = False
                    for a in keysComb:
                        if a[0].split('_')[0] == key.split('_')[0]:
                            a.append(key)
                            found = True
                    if not found:# and not key == ' ':
                        keysComb.append([key])
                else:
                    keysComb.append([key])
            #keysComb = sorted(keysComb, key=len)
            #reversed(keysComb)
            outheader = 'task,_C,_L,_N,trial,sequence,choices,response,binaryResponse,responseCorrect,truthful,domain,response_type,'
            outheaderending = ''
            for a in keysComb:
                if len(a) > 1:
                    for i in a:
                        if str(i.split('_')[1:]) not in donekeys:
                            for f in i.partition('_')[2:]:
                                if f not in  ['C','L','N']:
                                    if f in ["1","2","RT_2","3"]:
                                        outheader += '_' + f.replace('2','accurate').replace('3','sharing').replace('1','familiar')
                                        outheader += ','
                            donekeys.append(str(i.split('_')[1:]))
                if len(a)== 1:
                    outheaderending += a[0][:20] + ','
            for a in sorted(perHeadline[headline].keys()):
                if 'F_' in a or 'Partisan' in a:
                    headlineKeys += a.replace('F_Trump','Familiarity_Republicans_Combined').replace('F_Clinton','Familiarity_Democrats_Combined') + ','
            output.write(outheader + outheaderending+headlineKeys[:-1] + '\n')
        else:
            skipLine = False
            outline = ''
            for key in keysComb:
                if len(key) == 1:
                    outline += listLine[indComb[key[0]][0]] +','
            doubleKeys = []
            for key in perHeadline.keys():
                doubleKeys.append(key)
            for key in doubleKeys:
                trials= listLine[indComb['DO_BR_FL_88'][0]]
                newsItem = key[0].split('_')[0]
                specout = 'S'+newsItem
                for f in  ['_C','_L','_N']:
                    puzzled =newsItem + f
                    put = listLine[indComb[puzzled]] if puzzled in indComb.keys() else '0'
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
                newsItem = key.split('_')[0]
                specout = newsItem
                if float(perHeadline[newsItem]['Partisanship_All_Combined'])>3.8:
                    specout += ',1,0,0'
                elif float(perHeadline[newsItem]['Partisanship_All_Combined'])<2.2:
                    specout += ',0,1,0'
                else: 
                    specout += ',0,0,1'
                index = str(trialList.index(newsItem)) if newsItem in trialList else '14' #+ str(any(char for char in trialList[14] if char not in newsItem))
                if 'e' in index:
                    print(index,trialList)
                    counter += 1
                    for a in trialList: 
                        if trialList.count(a) > 1:
                            print('twice', index, a, listLine[0], trialList)

                specout += (',' + index)*2
                noInformation = True
                for ind in indComb[newsItem + '_2']:
                    if listLine[ind] == ' ':
                        print(listLine[indComb['id'][0]])
                        continue
                    if int(listLine[ind]) > 2.5:
                        accurate = True
                        noInformation = False
                    if int(listLine[ind]) < 2.5:
                        accurate = False
                        noInformation = False
                if noInformation:
                    accurate = "NoAnswer"
                if accurate == "NoAnswer":
                    #break
                    responseCorrect = "NoAnswer"
                else:
                    responseCorrect = (accurate and 'R' in newsItem) or (not accurate and 'F' in newsItem)
                stringbel = '1' if 'R' in newsItem else '0'
                ccspecs = ',Accept|Reject,' + str('Accept' if accurate else 'Reject')+ ',' +str('1' if accurate else '0') + ',' +str('1' if responseCorrect else '0') +',' + stringbel + ',misinformation,single-choice,'
                if listLine[indFirst['Random']] == '1' or listLine[indFirst['Google']] == '1':
                    skipLine = True
                if accurate == "NoAnswer":
                    skipLine = True
                    ccspecs = ',NoAnswer,' + 'NoAnswer'+ ',' +"NoAnswer" + ',' +"NoAnswer"+',' + "NoAnswer" + ',misinformation,single-choice,'
                donekeys = []
                ccspecsadd = ''
                for a in ["_1","_2","_RT_2","_3"]: 
                    if a not in donekeys:
                        donekeys.append(a)
                    else:
                        continue
                    spec = a# a.replace('_2','accurate').replace('_3','sharing')
                    if not spec in trialspec:
                        trialspec.append(spec)
                    if a not in indComb.keys():
                        if a == "_1":
                            if listLine[indComb[newsItem + a][0]] == '0':
                                listLine[indComb[newsItem + a][0]] = '-1'
                            if listLine[indComb[newsItem + a][0]] == '1':
                                listLine[indComb[newsItem + a][0]] = '1'
                            if listLine[indComb[newsItem + a][0]] == '2':
                                listLine[indComb[newsItem + a][0]] = '0'
                            if listLine[indComb[newsItem + a][0]] == '3':
                                listLine[indComb[newsItem + a][0]] = '-1'
                        ccspecsadd +=  listLine[indComb[newsItem + a][0]] + ','
                    else:
                        #print('a',a,listLine[indComb[a][0]])
                        nonZeroFound = False
                        for i in indComb[a]:
                            print(a,listLine[i])
                            ccspecsadd += a+','
                            if listLine[i][:10] != '':
                                nonZeroFound = True
                                ccspecsadd += listLine[i][:10] + ',' 
                        if not nonZeroFound:
                            ccspecsadd += ','
                    #print(ccspecsadd)
                ccspecs += ccspecsadd
                outstring =  specout + ccspecs + outline 
                headlineString = ''
                for a in sorted(perHeadline[newsItem].keys()):
                    if 'F_' in a or 'artisan' in a:
                        headlineString += perHeadline[newsItem][a] + ','
                finalstring = outstring + headlineString[:-1] + '\n'
                if not skipLine:
                    output.write(finalstring)#.replace(',,',',-9999,').replace(',,',',-9999,'))
output.close()
print(counter)
