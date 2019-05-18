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

# Own version, runs `tail` on a tempfile
# will copy to other file if kwarg `filename` is specified
# and will cleanup tempfile
def exec_with_split(cmd, **kwargs):
  filename = kwargs.get('filename', '')
  tail     = kwargs.get('tail', True)
  no_ascii = kwargs.get("no_ascii", False)
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
    if filename and no_ascii:
      subprocess.call(['sed', '-i', 's,\\x1B\[[0-9;]*[a-zA-Z],,g', filename])
  return retcode

if __name__ == "__main__":
  clean('mycopy*')
  cmd = ['python', 'runme.py']
  print("Run with tail")
  exec_with_split(cmd, filename="mycopy.txt")

  print("Run no tail")
  exec_with_split(cmd, filename="mycopy2.txt", tail=False, no_ascii=True)
