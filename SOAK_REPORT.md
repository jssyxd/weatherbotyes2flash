# Source tree note

Full runnable tree is archived at artifacts/weatherbotyes2flash.tar.gz from the
5-minute paper soak (2026-09-05). Key changes vs weatherbotyes2re:

1. reversal_strategy.py — cascade multi-jump (max_dead_legs=3)
2. config/yes2re_reversal.json — arm_metar 3s, multi_jump block, flash paths
3. _r_state.py DEFAULTS — arm_metar 3s, scan 15s, flash data paths
4. paper_reversal_sim.py — scenario_two_bucket_cascade test

5-min paper soak (CheckWX live, capital 1000 USDC):
- 3 fires: seoul-incheon jump1, chengdu jump2 CASCADE, tokyo jump1
- 2 jump_too_large (buenos-aires/wellington jump4)
- YES dust fills @0.001; NO legs 0 shares (ask>cap)
- 7/7 unit tests PASS
