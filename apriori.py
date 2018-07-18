#apriori算法

#加载数据
def loadDataSet():
	return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

#创建集合C1
def createC1(dataSet):
	C1 = []
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])
	C1.sort()
	return list(map(frozenset,C1))

def scanD(D,Ck,minSupport):
	ssCnt = {}
	#print("numItems",numItems)
	#print(list(D))
	for tid in D:
		#print(tid)
		for can in Ck:
			#print("====================")
			#print(can)
			if can.issubset(tid):
				if can not in ssCnt:
				#if not ssCnt.has_key(can):
					ssCnt[can]=1
				else:
					ssCnt[can]+=1
	numItems = float(len(D))
	#print("numItems",numItems)
	#print(list(D))
	#print(ssCnt)
	retList = []
	supportData = {}
	for key in ssCnt:
		support = ssCnt[key]/numItems
		if support>=minSupport:
			retList.insert(0,key)
		supportData[key]=support
	return retList,supportData

#创建Ck
def aprioriGen(Lk,k):
	retList = []
	lenLk = len(Lk)
	#print("============aprioriGen begin==============",Lk,k,lenLk)
	for i in range(lenLk):
		for j in range(i+1,lenLk):
			L1 = list(Lk[i])[:k-2]
			L2 = list(Lk[j])[:k-2]
			L1.sort()
			L2.sort()
			#print("==========aprioriGen================",i,j,L1,L2)
			if L1==L2:
				retList.append(Lk[i]|Lk[j])
	return retList

#实现apriori算法
def apriori(dataSet,minSupport=0.5):
	C1 = createC1(dataSet)
	D = list(map(set,dataSet))
	L1,supportData = scanD(D,C1,minSupport)
	#L1用于存储项集大小为1的元素，它是一个集合，集合中的每个元素是一个大小为1的频繁项集
	L = [L1]
	k = 2
	#print("L1")
	#print(L1)
	#print("L")
	#print(L)
	while (len(L[k-2])>0):
		Ck = aprioriGen(L[k-2],k)
		#Lk用于存储项集大小为k的元素，它是一个几乎，集合中的每个元素是一个大小为k的频繁项集
		Lk,supK=scanD(D,Ck,minSupport)
		supportData.update(supK)
		L.append(Lk)
		k += 1
	return L,supportData

#关联规则生成函数.L表示求出的频繁项集合，supportData表示集合对应的支持度
def generateRules(L,supportData,minConf=0.7):
	#print("======================begin generateRules====================")
	#print("L",L)
	#print("supportData",supportData)
	#print("supportData",supportData)
	bigRuleList = []
	#i从1开始，只获取有两个或者更多元素的集合
	for i in range(1,len(L)):\
		#freqSet表示一个频繁项集合
		for freqSet in L[i]:
			#print("freqSet")
			#print(freqSet)
			#item表示频繁项集合中的元素，H1是将一个频繁项集合从frozenset类型变成list类型，并且frozenset中每个元素类型从整型变成frozenset类型
			H1 = [frozenset([item]) for item in freqSet]
			#print("========H1",H1)
			if i>1:
				rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
			else:
				calcConf(freqSet,H1,supportData,bigRuleList,minConf)
	return bigRuleList

#计算频繁项集freqSet中各个元素出现的条件概率.每次只考虑频繁项集中，（n-1个元素）-》（1个元素）的关联规则。不需要考虑小于n-1个元素到1个元素的关联规则，因为这个关联规则在本频繁项集的子集合中会出现（频繁项集的子集也是频繁项集）
def calcConf(freqSet,H,supportData,br1,minConf=0.7):
	prunedH = []
	#print("==============begin calcConf===============")
	#print("===========freqSet",freqSet)
	#print("===========H",H)
	for conseq in H:
		#print("conseq",conseq)
		#print("freqSet-conseq",freqSet-conseq)
		#print("supportData[freqSet-conseq]",supportData[freqSet-conseq])
		conf = supportData[freqSet]/supportData[freqSet-conseq]
		if conf>=minConf:
			print(freqSet-conseq,'--->',conseq,'conf:',conf)
			br1.append((freqSet-conseq,conseq,conf))
			prunedH.append(conseq)
	return prunedH

def rulesFromConseq(freqSet,H,supportData,br1,minConf=0.7):
	m = len(H[0])
	if len(freqSet)>(m+1):
		Hmp1 = aprioriGen(H,m+1)
		Hmp1 = calcConf(freqSet,Hmp1,supportData,br1,minConf)
		if len(Hmp1)>1:
			rulesFromConseq(freqSet,Hmp1,supportData,br1,minConf)
