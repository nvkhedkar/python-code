import os
import re,shutil
import sys
import mimetypes
import getopt
import argparse


class LogArgumentParser(argparse.ArgumentParser):
  def error(self, msg):
    sys.exit(1)


parser = LogArgumentParser()

parser.description = '''find replace words in directory'''
parser.epilog = '''
Examples:
'''
parser.set_defaults(which='all')

parser.add_argument('-d', '--dir', help="directory to check",
                    type=str, default='.')
parser.add_argument('-i', '--in_word', help="word to find")
parser.add_argument('-o', '--out_word', help="word to replace")
parser.add_argument('-l', '--list_only', help="only show the words", action='store_true')
parser.add_argument('-b', '--backup', help="backup original file", action='store_true')
parser.add_argument('-sd', '--skip_dir', help="dirs to skip", action='append')
parser.add_argument('-sf', '--skip_file', help="file extensions to skip", action='append')

def read_file_to_list(full):
  try:
    with open(full, 'r') as f:
      lines = f.readlines()
      return lines
  except UnicodeDecodeError as e:
    # print(f'UnicodeDecodeError: Skip file {re.sub(os.path.dirname(args.dir), "", full)}')
    return None


def write_array_to_file(thelist,full_path_name):
  fo = open(full_path_name, "w")
  for ln in thelist:
    fo.write("%s" % ln)
  fo.close()


def find_n_replace(fw, rw, full):
  lines = read_file_to_list(full)
  if not lines: return

  if args.backup and not args.list_only:
    write_array_to_file(lines, full+'.orig')

  relpath = re.sub(os.path.dirname(args.dir), "", full)
  for i in range(len(lines)):
    ln = lines[i]
    if re.search(fw, ln):
      print(f'replacing: {relpath}: line {i+1}: {fw} with {rw}')
      lines[i] = re.sub(fw, rw, lines[i])

  if not args.list_only:
    write_array_to_file(lines, full)
  return


def skip_dir(dirname):
  if args.skip_dir:
    for sd in args.skip_dir:
      if sd in dirname.split('/'):
        return True
  return False


def main(argv):
  print(args)
  for root, dirnames, filenames in os.walk(args.dir):
    root = re.sub(r'\\', "/", root)
    relative = re.sub(args.dir, "", root)
    # print(relative)
    if skip_dir(relative): continue
    for filename in filenames:
      if re.search('^\.', filename): continue
      full = root + "/" + filename
      find_n_replace(args.in_word, args.out_word, full)
  # print(args.skip_dir, type(args.skip_dir))
  return

if __name__ == "__main__":
  args = parser.parse_args()
  main(sys.argv[1:])

os._exit(0)

