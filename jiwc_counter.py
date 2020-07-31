import argparse
from os.path import dirname, isfile, join
from os import listdir
import os
from importlib import import_module
from collections import Counter
import pandas as pd


class JIWC_Counter:
	def __init__(self, args):
		self.args = args
		self.infile = args.doc
		# print(self.infile)
		self.categs = {'悲しい':'Sad', '不安':'Anxiety', '怒り':'Anger', '嫌悪感':'Disgust',
		 '信頼感':'Trust', '驚き':'Surprise', '楽しい':'Joy'}
		self.pos = ['名詞', '動詞', '形容詞', '副詞']
		self.prefix = 'JIWC-B_'+args.ver+'.csv'
		self.check_files()
		tok_list = self.get_tokens(args.doc)
		# print(len(tok_list), tok_list)
		words_by_categ = self.count_categories(tok_list)
		self.print_output(words_by_categ)

		
	def check_files(self):
		cur_dir = os.getcwd()
		all_files = [a for a in listdir(cur_dir) if isfile(join(cur_dir,a))]
		files_exist = True if self.prefix in all_files else False
		if not files_exist:
			print(self.prefix)
			print('JIWC dictionaries not found...\nProgram terminating.')
			exit()


	def get_tokens(self, doc):
		infile = None
		try:
			input_file=open(doc, 'r')
			infile = input_file.readlines()
			input_file.close()
		except:
			print('There is a problem with the filepath.')
			exit()

		tokenized = None
		try:
			tokenizer = jumanpp_tokenizer(infile, self.pos)
			print('Tokenizing files with jumanpp...')
			tokenized = tokenizer.tokenize()
		except Exception as e1:
			try:
				print('Error occurred when tokenizing with pyknp.Jumanpp. (Installing Juman++ recommended if not already installed.'+
					'\nCheck GitHub page for more info)')
				print(e1)
				tokenizer = mecab_tokenizer(infile)
				print('Tokenizing files with mecab...')
				tokenized = tokenizer.tokenize()
			except Exception as e2:
				print('Error occurred when tokenizing MeCab.\nProgram terminating.')
				print(e2)
				exit()
		return tokenized


	def count_categories(self, tok_list):
		categ_out = {a:[{}, 0] for a in self.categs.keys()}
		df = pd.read_csv('JIWC-B_'+ self.args.ver +'.csv')
		df.fillna('', inplace=True)
		emos = df.shape[1] - 1
		JIWC_dic = {}
		emotion = 'emo' 
		for i in df.iterrows():
			vals=  i[1]
			JIWC_dic[vals[0]] = {emotion+str(a+1):vals[a+1] for a in range(emos)}
		tok_counts = Counter(tok_list)
		for i, j in tok_counts.items():
			if i in JIWC_dic.keys():
				for k in range(emos):
					emo = JIWC_dic[i][emotion+str(k+1)]
					if emo != '':
						categ_out[emo][0][i] = j
						categ_out[emo][1] += j
		return categ_out


	def print_output(self, categ_out):
		block = ['=' for a in range(40)]
		print(''.join(block))
		categ_eng = {a.lower()[:3]:a for a in self.categs.values()}
		rev_categs = {}
		for i, j in self.categs.items():
			rev_categs[j] = i
		if self.args.print_categ is not None and len(self.args.print_categ)>0:
			for m in self.args.print_categ:
				# print('printing category words')
				if m.lower()[:3] in categ_eng.keys():
					categ = rev_categs[categ_eng[m.lower()[:3]]]
					allwords_ = list(categ_out[categ][0].keys())
					print('{0}/{1} words (Total: {2}) : '.format(categ, self.categs[categ], len(allwords_)), end=' ')
					for n in allwords_[:self.args.num]:
						print(n, end=', ')
					print('\n')
				
		print(''.join(block))
		print("Total Counts by Category")
		print()
		for i, j  in categ_out.items():
			print('{0}/{1}: {2}'.format(i, self.categs[i], j[1]))


class jumanpp_tokenizer(object):

	"""tokenize with Jumanpp"""
	def __init__(self, infile, pos):
		self.pyk = import_module('pyknp')
		self.infile = infile
		self.valid_pos = pos
	

	def tokenize(self):
		tokens = []
		jumanpp = self.pyk.Juman()
		for line in self.infile:
			clean_line = line.replace(' ', '　')
			result = jumanpp.analysis(clean_line).mrph_list()
			tokens.extend([a.midasi for a in result  if a.hinsi in self.valid_pos])
		return tokens


class mecab_tokenizer:

	"""tokenize with MeCab"""
	def __init__(self, infile):
		self.infile = infile
		print('importing')
		self.MeCab = import_module('MeCab')
		print('import succeeded')

	
	def tokenize(self):
		tokens = []	
		wakati = self.MeCab.Tagger("-Owakati")
		for line in self.infile:
			tokens.extend(wakati.parse(line).split())
		return tokens


def main():
	arg_parser = argparse.ArgumentParser(description='process documents')
	arg_parser.add_argument('--doc', type=str, help='path of the file to process')
	arg_parser.add_argument('--ver', choices=['2017', '2018', '2019'], help='version of JIWC dictionary(year)')
	arg_parser.add_argument('--print_categ', nargs='+', help='write one or more values from [sad, anx, ang ,dis, tru, sur, joy]')
	arg_parser.add_argument('--num', type=int, help='specifies the number of words in a category to print using --print_categ')
	args = arg_parser.parse_args()
	jiwc_counter = JIWC_Counter(args)


if __name__ == '__main__':
	main()
