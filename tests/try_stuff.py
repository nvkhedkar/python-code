import argparse, re

def check_validity_trs_file_path(arg_value, pat='[\w\d\:\-\.\\\/]{1,1024}'):
  recomp = re.compile(pat)
  if not recomp.match(arg_value) or not arg_value.endswith('.trs'):
    print('Invalid arg value')
    raise argparse.ArgumentError(f"Argument {arg_value} not in correct format")
  return arg_value

import shutil

total, used, free = shutil.disk_usage("c:/nvk")

print(f"Total: {(total // (2**30))} GiB {total}")
print("Used: %d GiB" % (used // (2**30)))
print("Free: %d GiB" % (free // (2**30)))

# print(check_validity_trs_file_path("../nak/any/dir/path/somefile.trs"))
