#测试apriori算法
import apriori

if __name__=="__main__":
	dataSet = apriori.loadDataSet()
	print(dataSet)
	C1 = apriori.createC1(dataSet)
	#print(C1)
	D=list(map(set,dataSet))
	#print(len(list(D)))
	L1,suppData0 = apriori.scanD(D,C1,0.5)
	print(L1)
	print(suppData0)

	print("=====================")
	L,suppData = apriori.apriori(dataSet,0.5)
	print(L)
	print(suppData)
	rules = apriori.generateRules(L,suppData,minConf=0.5)
	print("rules")
	print(rules)
