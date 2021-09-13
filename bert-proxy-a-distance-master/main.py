"""
Main driver code

Example: 

python main.py /science/image/nlp-datasets/creoles/proxy/english-emergency.src /science/image/nlp-datasets/creoles/proxy/english-newswire.src /science/image/nlp-datasets/creoles/proxy/english.vocab
"""


import argparse # option parsing
from src.dataset import Dataset
from src.model import SVM


def process_command_line():
  """
  Return a 1-tuple: (args list).
  `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
  """

  parser = argparse.ArgumentParser(description='usage') # add description
  # positional arguments
  parser.add_argument('d1s', metavar='domain1-source', type=str, help='domain 1 source')

  parser.add_argument('d2s', metavar='domain2-source', type=str, help='domain 2 source')

  #parser.add_argument('v', metavar='vocab', type=str, help='shared bpe vocab')

  # optional arguments
  parser.add_argument('-b', '--batch-size', dest='b', type=int, default=32, help='batch_size')

  args = parser.parse_args()
  return args


def main(domain1_source, domain2_source, batch_size):
    data_iterator = Dataset(domain1_source,
                            domain2_source,
                            batch_size=batch_size)
    model = SVM(batch_size, 768)# data_iterator.get_vocab_size())
    model.fit(data_iterator) 
    print('INFO: testing...')
    test_mae = model.test(data_iterator, mae=True)
    print('INFO: test MAE: ', test_mae)
    print('INFO: PAD value: ', 2. * (1. - 2. * test_mae))


if __name__ == '__main__':

    args = process_command_line()
    main(args.d1s, args.d2s,  args.b)
