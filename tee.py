import subprocess, os, sys, tempfile, shutil, glob

def clean(*args):
  deleted = []
  for arg in args:
    for f in glob.glob(arg):
      try:
        os.remove(f)
        deleted.append(f)
      except:
        pass
  print('Deleted: ' + ', '.join(deleted))

# From SO, kinda sucks but the idea of running `tee`
# in parallel is a simple solution
def test1():

    # Unbuffer output (this ensures the output is in the correct order)
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    tee = subprocess.Popen(["tee", "copy.txt"], stdin=subprocess.PIPE)
    # Writing to stderr or stdout pipes to tee.stdin
    os.dup2(tee.stdin.fileno(), sys.stdout.fileno())
    os.dup2(tee.stdin.fileno(), sys.stderr.fileno())

    cmd = ['cat', 'sample.txt']
    subprocess.call(cmd, stdout=tee.stdin, stderr=tee.stdin)
    subprocess.call(['node', 'test.js'], stdout=tee.stdin, stderr=tee.stdin)

# Own version, runs `tail` on a tempfile
# will copy to other file if kwarg `filename` is specified
# and will cleanup tempfile
def exec_with_split(cmd, **kwargs):
  filename = kwargs.get('filename', '')
  tail     = kwargs.get('tail', True)
  retcode  = None
  co_procs = []

  with tempfile.NamedTemporaryFile("wb") as fd:
    if tail:
      co_procs.append(
        subprocess.Popen(["tail", "-f", fd.name], stdout=sys.stdout, stderr=sys.stderr))
    try:
      proc = subprocess.Popen(cmd, stdout=fd, stderr=fd)
      proc.wait()
      retcode = proc.returncode
    finally:
      for proc in co_procs:
        try:
          if proc.poll() == None: proc.terminate()
        except:
          pass
      if filename:
        shutil.copy(fd.name, filename)
  return retcode


def test2():
  clean('mycopy*')
  cmd = ['python', 'runme.py']
  print("Run with tail")
  exec_with_split(cmd, filename="mycopy.txt")

  print("Run no tail")
  exec_with_split(cmd, filename="mycopy2.txt", tail=False)

if __name__ == "__main__":
    if 0:
        test1()
    if 1:
        test2()