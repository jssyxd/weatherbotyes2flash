# Deploy runbook (paper)

```bash
export CHECKWX_API_KEY=...
python3 tests_reversal.py
python3 reversal_runner.py run --config config/yes2re_reversal.json --max-seconds 1200
```

Health: `data/yes2flash_health.json`  
Events: `data/yes2flash_events.jsonl`  
State: `data/yes2flash_state.json`
