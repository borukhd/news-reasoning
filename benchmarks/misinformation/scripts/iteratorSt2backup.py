
keys = []
keysComb = []
indFirst = {}
indComb = {}
count = 0
counter = 0
donekeys = []
output = open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/Study1dataReshaped.csv', "w+")
with open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/Data/Study1data.csv') as lines:
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
                #print('start',keys)
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
            keysComb = sorted(keysComb, key=len)
            reversed(keysComb)
            #output.write(str(keys).replace('[','').replace(']','').replace(' ','').replace(',',''))
            outheader = 'task,_C,_L,_N,trial,sequence,choices,response,binaryResponse,responseCorrect,truthful,domain,response_type,'
            outheaderending = ''
            for a in keysComb:
                if len(a) > 1:
                    for i in a:
                        if str(i.split('_')[1:]) not in donekeys:
                            for f in i.split('_')[1:]:
                                if f not in  ['C','L','N']:
                                    outheaderending += '_' + f
                            outheaderending += ','
                            donekeys.append(str(i.split('_')[1:]))
                if len(a) == 1:
                    outheader += a[0][:10] + ','
            output.write(outheader+outheaderending[:-1] + '\n')
        else:
            outline = ''
            for key in keysComb:
                if len(key) == 1:
                    outline += listLine[indComb[key[0]][0]][:10] + ','
            #print(listLine[indComb['id'][0]], outline)
            doubleKeys = []
            for key in keysComb:
                #allkeys = 
                if len(key) > 1:
                    doubleKeys.append(key)
            for key in doubleKeys:
                newsItem = key[0].split('_')[0]
                specout = newsItem
                for f in  ['_C','_L','_N']:
                    puzzled =newsItem + f
                    put = listLine[indComb[puzzled]] if puzzled in indComb else '0'
                    specout += ',' + put
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
                    break
                    responseCorrect = "NoAnswer"
                else:
                    responseCorrect = (accurate and 'R' in newsItem) or (not accurate and 'F' in newsItem)
                stringbel = '1' if 'R' in newsItem else '0'
                ccspecs = ',Accept|Reject,' + str('Accept' if accurate else 'Reject')+ ',' +str('1' if accurate else '0') + ',' +str('1' if responseCorrect else '0') +',' + stringbel + ',misinformation,single-choice,'
                for a in key: 
                    for i in indComb[a]:
                        ccspecs += listLine[i][:10] +','
                outstring =  specout + ccspecs + outline
                finalstring = outstring[:-1] + '\n'
                output.write(finalstring)#.replace(',,',',-9999,').replace(',,',',-9999,'))
output.close()
print(counter)
