
count = 0
keys = []
linenumber = 0
perHeadline = {}
indFirst = {}
with open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/pretest/Pretest5results.csv') as lines:
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
        elif linenumber == 2:
            count = 0
            for key in listLine:
                keys[count] = keys[count] + '_' + key if keys[count] != '' else key
                indFirst[keys[count]] = count
                count += 1
        elif linenumber == 3:
            count = 0
            for key in listLine:
                keys[count] = keys[count] + '_' + key if keys[count] != '' else key
                indFirst[keys[count]] = count
                count += 1
        else:
            headline = listLine[indFirst['Headline']].partition('_')[2].partition('.')[0].replace('-','').replace(';',',').lower()
            if headline not in perHeadline.keys():
                perHeadline[headline] = {}
                for key in keys:
                    perHeadline[headline][key] = listLine[indFirst[key]]


keys = []
keysComb = []
indFirst = {}
indComb = {}
count = 0
counter = 0
donekeys = []
trialspec = []
output = open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/Study1dataReshaped.csv', "w+")
with open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/Data/Study1data.csv') as lines:
    headlineKeys = ''
    line1 = True
    line2 = True
    for line in lines:
        listLine = line.replace('\r','').replace('\n','').replace("What type of social media accounts do you use (if any)?","accounts").replace("We are also interested in your *past* political preferences. Please select any of the following...","pastPolitical").replace("Would you consider sharing this story online (for example, through Facebook or Twitter)?","sharingContent").replace("Which of these types of content would you consider sharing on social media (if any)?","sharingType").replace("To the best of your knowledge, is the claim in the above headline accurate?","accurate").split(',')
        if line1:
            line1 = False
            for key in listLine:
                indFirst[key] = count
                count += 1
                keys.append(key)
        elif line2:
            line2 = False
            count = 0
            for key in listLine:
                if key not in keys:
                    key = keys[count] + '_' 
                    key += listLine[count]
                if key not in indComb:
                    indComb[key] = []
                indComb[key].append(count)
                count += 1
                division = key.split('_')[0]
                division = key[:4]
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
                prefix = key.split('_')[0]
                if prefix in keys:
                    if len(keys[indFirst[prefix]]) < 4 and ('R' in prefix or 'F' in prefix):
                        title = listLine[indFirst[prefix]].partition(' ')[2].replace(';',',')
                        for headline in perHeadline.keys():
                            if title == headline:
                                perHeadline[prefix.replace('R','Real').replace('F','Fake')] = perHeadline[headline]
            #keysComb = sorted(keysComb, key=len)
            #reversed(keysComb)
            outheader = 'task,_C,_L,_N,trial,sequence,choices,response,binaryResponse,responseCorrect,truthful,domain,response_type,'
            outheaderending = ''
            for a in keysComb:
                if len(a) > 1:
                    for i in a:
                        if str(i.split('_')[1:]) not in donekeys:
                            for f in i.split('_')[1:]:
                                if f not in  ['C','L','N']:
                                    outheader += '_' + f 
                            outheader += ','
                            donekeys.append(str(i.split('_')[1:]))
                if len(a)== 1:
                    outheaderending += a[0][:20] + ','
            for a in sorted(perHeadline[headline].keys()):
                if 'Combined' in a or '_Partisan' in a:
                    headlineKeys += a + ','
            output.write(outheader + outheaderending+headlineKeys[:-1] + '\n')
        else:
            skipLine = False
            outline = ''
            for key in keysComb:
                if len(key) == 1:
                    outline += listLine[indComb[key[0]][0]] + ','
            doubleKeys = []
            for key in keysComb:
                if len(key) > 1:
                    doubleKeys.append(key)
            for key in doubleKeys:
                newsItem = key[0].split('_')[0]
                specout = newsItem
                """
                for f in  ['_C','_L','_N']:
                    puzzled =newsItem + f
                    put = listLine[indComb[puzzled]] if puzzled in indComb else '0'
                    specout += ',' + put
                """
                if float(perHeadline[newsItem]['Partisanship_All_Combined'])>3.7:
                    specout += ',1,0,0'
                elif float(perHeadline[newsItem]['Partisanship_All_Combined'])<2.3:
                    specout += ',0,1,0'
                else: 
                    specout += ',0,0,0'
                trialList = ['Fake'+str(i) for i in range(1,19)] + ['Real'+str(i) for i in range(1,19)]
                index = str(trialList.index(newsItem)) if newsItem in trialList else '14' #+ str(any(char for char in trialList[14] if char not in newsItem))
                if 'e' in index:
                    print(index,trialList)
                    counter += 1
                    for a in trialList: 
                        if trialList.count(a) > 1:
                            print('twice', index, a, listLine[0], trialList)

                specout += (',' + index)*2
                noInformation = True
                for ind in indComb[newsItem + '_accurate']:
                    if listLine[ind] == '1':
                        accurate = True
                        noInformation = False
                    if listLine[ind] == '0':
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
                for a in ["_accurate","_sharing","_RT_1_Timing-First Click","_RT_2_Timing-Last Click","_RT_3_Timing-Page Submit","_RT_4_Timing-Click Count"]: 
                    a = key[0][:key[0].index('_')] + a
                    if a not in donekeys:
                        donekeys.append(a)
                    else:
                        continue
                    spec = a[a.index('_')+1:]
                    if not spec in trialspec:
                        trialspec.append(spec)
                    if a not in indComb.keys():
                        #print(a)
                        ccspecsadd += ','
                    else:
                        #print('a',a,listLine[indComb[a][0]])
                        nonZeroFound = False
                        for i in indComb[a]:
                            #print(a,listLine[i])
                            #ccspecsadd += a+','
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
                    if 'Combined' in a or '_Partisan' in a:
                        headlineString += perHeadline[newsItem][a] + ','
                finalstring = outstring + headlineString[:-1] + '\n'
                if not skipLine:
                    output.write(finalstring)#.replace(',,',',-9999,').replace(',,',',-9999,'))
output.close()
print(counter)
