import json,subprocess,time,pathlib,re
base=pathlib.Path(__file__).resolve().parents[1]
loops=base/'reports'/'loops'
loops.mkdir(parents=True,exist_ok=True)

def sh(cmd):
    try:
        return subprocess.check_output(cmd,shell=True,text=True,stderr=subprocess.DEVNULL,timeout=8)
    except Exception:
        return ''

def collect(i):
    latest=sh("ls -1t ~/Library/Application\\ Support/Code/logs | head -n1").strip()
    logdir=f"~/Library/Application Support/Code/logs/{latest}" if latest else ""
    mcp=sh(f"rg -n 'mcpServer|telemetry|CodexMcpConnection|_doActivateExtension' {logdir} -g '*.log' | head -n 200") if latest else ''
    listens=sh("lsof -iTCP -sTCP:LISTEN -n -P | head -n 200")
    exts=sh("code --list-extensions | rg -i 'copilot|codeium|continue|tabnine|gitlens|openai' || true")
    disk=sh("df -h /System/Volumes/Data | awk 'NR==2{print $2\" \"$3\" \"$4\" \"$5}'").strip()
    out={
      'loop':i,
      'timestamp':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'latest_log':latest,
      'mcp_or_telemetry_lines':len([x for x in mcp.splitlines() if x.strip()]),
      'listening_ports':len([x for x in listens.splitlines()[1:] if x.strip()]),
      'ai_extension_sources':sorted(set([x.strip() for x in exts.splitlines() if x.strip()])),
      'disk_state':disk
    }
    score=0
    if out['mcp_or_telemetry_lines']>0: score+=1
    if out['listening_ports']>0: score+=1
    if len(out['ai_extension_sources'])>0: score+=1
    out['signal_health_score']=score
    (loops/f'loop_{i}.json').write_text(json.dumps(out,indent=2))
    return out

results=[]
for i in range(1,4):
    results.append(collect(i))
    time.sleep(2)
summary={
 'status':'pass',
 'loops':len(results),
 'avg_signal_health_score':sum(r['signal_health_score'] for r in results)/len(results),
 'latest':results[-1],
 'delta':{
   'mcp_or_telemetry_lines':results[-1]['mcp_or_telemetry_lines']-results[0]['mcp_or_telemetry_lines'],
   'listening_ports':results[-1]['listening_ports']-results[0]['listening_ports']
 }
}
(base/'reports'/'loop-summary.json').write_text(json.dumps(summary,indent=2))
print(base/'reports'/'loop-summary.json')
print(json.dumps(summary,indent=2))
