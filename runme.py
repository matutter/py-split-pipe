import os, sys, time

# Set output to non-buffered
# This preserves order
#sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
#sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 0)

count = 3
while 1:
  sys.stdout.write( "\033[94m"+  "I am stdout %s \033[0m\n" % count)
  sys.stderr.write("I am stderr %s\n" % count)
  count -= 1
  if count <= 0:
    exit(0)
  time.sleep(1)