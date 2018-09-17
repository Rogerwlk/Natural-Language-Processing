from collections import Counter

class Eval:
    def __init__(self, gold, pred):
        assert len(gold)==len(pred)
        self.gold = gold
        self.pred = pred

    def accuracy(self):
        numer = sum(1 for p,g in zip(self.pred,self.gold) if p==g)
        return numer / len(self.gold)

    def print_mx(self):
    	pair = []
    	for i in range(len(self.gold)):
    		pair.append(self.gold[i]+'-'+self.pred[i])
    	c = Counter(pair)
    	lang_list = ['ARA', 'DEU', 'FRA', 'HIN', 'ITA', 'JPN', 'KOR', 'SPA', 'TEL', 'TUR', 'ZHO']
    	print(','+','.join(lang_list))
    	for i in lang_list:
    		print(i, end=',')
    		for j in lang_list:
    			print(c[str(i)+'-'+str(j)], end=',')
    		print()