#!/bin/bash
# render in fresh processes of BATCH takes each until the queue is drained
cd /home/claude/narr
for i in $(seq 1 40); do
  BATCH=12 /home/claude/cbx/bin/python render.py >> render_full.log 2>&1
  tail -c 300000 render_full.log | tr '\r' '\n' | grep -a '^todo' | tail -1 | grep -q '^todo 0$' && break
done
echo LOOPDONE >> render_full.log
