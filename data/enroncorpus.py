# Adapted from Radim Rehurek's wikicorpus code. See https://github.com/piskvorky/gensim/blob/develop/gensim/corpora/wikicorpus.py

"""

  Convert a file system of emails to (sparse) vectors. The input is the root\
of the file system to walk. All files are in plain text.

This creates three files:

* `OUTPUT_PREFIX_wordids.txt`: mapping between words and their integer ids
* `OUTPUT_PREFIX_bow.mm`: bag-of-words (word counts) representation, in Matrix Matrix format
* `OUTPUT_PREFIX_tfidf.mm`: TF-IDF representation

The output Matrix Market files can then be compressed (e.g., by bzip2) to save \
disk space; gensim's corpus iterators can work with compressed input, too.

`VOCABULARY_SIZE` controls how many of the most frequent words to keep (after
removing tokens that appear in more than 10%% of all documents).

"""

import email
import logging
import itertools
import sys
import os.path
import re
import bz2
import string
import pickle
from pattern.en import parse

from gensim import interfaces, matutils, utils
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
# cannot import whole gensim.corpora, because that imports wikicorpus...
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.textcorpus import TextCorpus
from gensim.corpora.mmcorpus import MmCorpus
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import re
import csv
import email
logger = logging.getLogger('gensim.corpora.wikicorpus')



# Emails are first scanned for all distinct word types (~900,000). The types
# that appear in more than 10% of articles are removed and from the rest, the
# DEFAULT_DICT_SIZE most frequent types are kept (default 100k).
DEFAULT_DICT_SIZE = 100000

# Ignore emails shorter than ARTICLE_MIN_CHARS characters (after preprocessing)
ARTICLE_MIN_CHARS = 500

# HELPER FUNCTIONS
punctre = re.compile('[%s]' % re.escape(string.punctuation))

def is_int(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

def walk_os(root):
  for dirname, dirnames, filenames in os.walk(root):
    for filename in filenames:
      yield os.path.join(dirname,filename)

def gen_open(filenames):
  for name in filenames:
    with open(name, encoding="windows-1252") as f:
      yield email.message_from_file(f)._payload

def strip_punct(files):
  for file in files:
    nopunct = punctre.sub('',file)
    yield nopunct

stop_words = set(stopwords.words('english'))
stop_words.update({"image", "please", "com", "from", "www"})

def tok(content):
  """
  Return a list of tokens in an email. Ignore words shorter than 2 or longer
  than 15.
  """
  #content.lower()
  return [lemmatizer.lemmatize(token) for token in utils.tokenize(content,lower=True,errors='ignore') if 2<len(token)<=15 and token not in stop_words]

class EnronCorpus(TextCorpus):
  def __init__(self, root_name, no_below=20, keep_words=DEFAULT_DICT_SIZE, dictionary=None):
    """
    Initialize the corpus. This scans through all the emails once, to determine the corpus
    vocabulary. (only the first `keep_words` most frequent words that appear in at least
    `no_below` documents are kept).
    """
    self.root_name = root_name
    if dictionary is None:
      self.dictionary = Dictionary(self.get_texts())
      self.dictionary.filter_extremes(no_below=no_below, no_above=0.1, keep_n=keep_words)
    else:
      self.dictionary = dictionary
    self.metadata = None

  def get_texts(self, return_raw=False):
    """
    Walk the file system, strip punctuation, normalize all numbers to be '2'.
    """
    filenames = walk_os(self.root_name)
    opened_files = gen_open(filenames)
    stripped_files = strip_punct(opened_files)
    length = 0
    for email in stripped_files:
      if len(email) > ARTICLE_MIN_CHARS:
        length+=1
        print( 'Iteration: %i' % length)
        yield tok(email)
    self.length = length # cache corpus length


if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
  logging.root.setLevel(level=logging.INFO)
  logger.info("running %s" % ' '.join(sys.argv))

  program = os.path.basename(sys.argv[0])

  # check and process input arguments
  # argv[1] = input (i.e. root of tree), argv[2] = output
  # optional argv[3] = keep_words
  if len(sys.argv) < 3:
    print(globals()['__doc__'] % locals())
    #sys.exit(1)
  input, output = sys.argv[1:3]
  if len(sys.argv) > 3:
    keep_words = int(sys.argv[3])
  else:
    keep_words = DEFAULT_DICT_SIZE

  # build dictionary. only keep 100k most frequent words (out of total ~900k unique tokens)
  #id2token = Dictionary.load_from_text(output + '_wordids.txt')
  # print(id2token)
  #enron = EnronCorpus(input,keep_words=keep_words)#, dictionary=id2token)

  # # save dictionary and bag-of-words (term-document frequency matrix)
  #enron.dictionary.save_as_text(output+'_wordids.txt')
  #MmCorpus.serialize(output+'_bow.mm',enron,progress_cnt=10000)
  # del enron

  # initialize corpus reader and word->id mapping
  id2token = Dictionary.load_from_text(output + '_wordids.txt')
  corpus = MmCorpus(output + '_bow.mm')
  # build tfidf
  from gensim.models.ldamulticore import LdaMulticore
  from gensim.models import HdpModel
  #hdp = HdpModel(corpus, id2token)
  lda = LdaMulticore(corpus, id2word=id2token, num_topics=50, workers=11, passes=10)

  with open("model_hdp_enron", "ab") as pick:
    pickle.dump(hdp,pick)


  logger.info("finished running %s" % program)
