import subprocess, os, sys, tempfile, shutil, glob
from subprocess import Popen

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
  """
  @kwarg filename - Will copy output to a filename
  @kwarg tail - Will print output to stdout while subprocess is running.
  @kwarg no_ascii - Will strip ASCII escape sequences, including color codes, from the `filename`.
  @kwarg buffered - If falsy will pass `cmd` as arguments to stdbuf and run `cmd` with unbuffered output.
  """
  filename = kwargs.get('filename', None)
  tail     = kwargs.get('tail', True)
  no_ascii = kwargs.get("no_ascii", False)
  buffered = kwargs.get("buffered", True)
  retcode  = None
  co_procs = []
  wrapper_cmd = []

  if not buffered:
    wrapper_cmd.extend(["stdbuf", "-oL"])

  with tempfile.NamedTemporaryFile("wb") as fd:
    try:
      proc = Popen(wrapper_cmd + cmd, stdout=fd, stderr=fd)
      if tail:
        tail_cmd = ["tail", "-f", fd.name, '--pid', str(proc.pid)]
        co_procs.append(Popen(tail_cmd, stdout=sys.stdout, stderr=sys.stderr))
      proc.wait()
      retcode = proc.returncode
    finally:
      for proc in co_procs:
        try:
          if proc.poll() == None: proc.terminate()
        except:
          pass
      if filename and filename != fd.name:
        shutil.copy(fd.name, filename)
    if filename and no_ascii:
      subprocess.call(['sed', '-i', 's,\\x1B\[[0-9;]*[a-zA-Z],,g', filename])
  return retcode

if __name__ == "__main__":
  clean('mycopy*')
  cmd = ['python', 'runme.py']
  print("Run with tail")
  exec_with_split(cmd, filename="mycopy.txt", buffered=False)

  print("Run no tail")
  exec_with_split(cmd, filename="mycopy2.txt", tail=False, no_ascii=True)
