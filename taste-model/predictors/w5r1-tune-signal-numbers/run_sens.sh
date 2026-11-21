cd /home/user/Listener/taste-model
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
for set in base,oat,stale rj; do
 W5_SET=$set python3 -W ignore -m evalkit.run --fast --refs ref_w4r1_listening --dump-scores /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf5/builder-r1-tune-signal-numbers/runs/sens_${set//,/_}.pkl predictors/w5r1-tune-signal-numbers/predict.py > /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf5/builder-r1-tune-signal-numbers/runs/sens_${set//,/_}.txt 2>&1
done
date -u +%T > /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf5/builder-r1-tune-signal-numbers/runs/sens_end.txt
