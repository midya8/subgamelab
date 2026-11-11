import tempfile,subprocess,sys,json,pathlib,os
from tools.make_cases import controls
from subgamelab import solve
root=pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 t=pathlib.Path(t);v=t/'venv';subprocess.run([sys.executable,'-m','venv',str(v)],check=True);py=v/'bin/python';subprocess.run([str(py),'-m','pip','install',str(root)],check=True,stdout=subprocess.DEVNULL)
 origins=json.loads(subprocess.check_output([str(py),'-c','import json,subgamelab,subgamelab.engine,subgamelab.schema,subgamelab.verify,subgamelab.__main__;import sys;print(json.dumps([m.__file__ for n,m in sys.modules.items() if n=="subgamelab" or n.startswith("subgamelab.")]))'],cwd=t,text=True));assert len(origins)==5 and all(str(v) in f for f in origins)
 count=bad=0
 for name,x in controls():
  expected=solve(x);path=t/'input.json';path.write_text(json.dumps(x))
  for cmd in [[str(py),'-m','subgamelab'],[str(v/'bin/subgamelab')]]:
   out=json.loads(subprocess.check_output(cmd+['solve',str(path)],cwd=t,text=True));assert out==expected
   cert=t/'cert.json';cert.write_text(json.dumps(out));assert json.loads(subprocess.check_output(cmd+['verify',str(cert)],cwd=t,text=True))=={'valid':True}
   out['profiles'][0]['nash']=not out['profiles'][0]['nash'];cert.write_text(json.dumps(out));p=subprocess.run(cmd+['verify',str(cert)],cwd=t,capture_output=True);assert p.returncode==2;bad+=1
  count+=1
 print(json.dumps(dict(module_origins=len(origins),controls=count,entrypoints=2,rejected_forgeries=bad)))
