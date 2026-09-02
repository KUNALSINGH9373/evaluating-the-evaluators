#!/usr/bin/env bash
# Build every figure, in the one order that is correct.
#
# Order matters. Several scripts have historically written the same filename, and the last
# writer silently won: charts.py's hero vs hero.py's, charts2.py's tier donut vs charts.py's
# bar, charts.py's institution bar vs tree.py's tree. Those duplicates are now disabled at
# source, but the rule stands — one figure, one owner, and the standalone scripts run last.
#
#   ./build_charts.sh              -> ../charts            (current palette)
#   ./build_charts.sh recoloured   -> ../charts/recoloured (alternate palette)
set -euo pipefail
cd "$(dirname "$0")"
R="$(cd .. && pwd)"

if [ "${1-}" = "legacy" ]; then
  export AISIEVAL_PALETTE=legacy
  export AISIEVAL_CHARTS_OUT="$R/charts/legacy"
elif [ -n "${1-}" ]; then
  export AISIEVAL_CHARTS_OUT="$R/charts/$1"
else
  export AISIEVAL_CHARTS_OUT="$R/charts"
fi
mkdir -p "$AISIEVAL_CHARTS_OUT"
echo "building into $AISIEVAL_CHARTS_OUT"

for s in charts.py charts2.py hero.py tree.py fig12_scope.py fig15b.py fig_finding.py fig_action_level.py fig_examples.py fig_examples2.py; do
  printf '  %-16s ' "$s"
  if python3 "$s" >/dev/null 2>/tmp/cb_err; then echo ok; else echo "FAILED"; sed 's/^/      /' /tmp/cb_err; FAILED=1; fi
done

# The NeurIPS set was NOT in this script and silently went stale on every rebuild. Three are
# generated here; the other seven are copies of main-set figures and are re-copied below, so the
# whole submission set regenerates from one command.
for f in nfig1_pipeline.py nfig2_matrix.py nfigA_access.py; do
  python3 "$f" >/dev/null 2>&1 && echo "  $f ok" || echo "  $f FAILED"
done
# The script already cd'd to its own directory at the top, so this must be relative to
# that, not to $0 again. Running `bash scripts/build_charts.sh` from the project root
# used to fail here after every figure had already been drawn.
cd "../charts" || exit 1
for pair in "05:fig3_pre_vs_post" "12:fig4_evaluator_scope" "25:figA1_what_is_a_finding" \
            "23:figA3_corpus_growth" "15b:figA4_shortfall_by_year" "13:figA5_institutions" \
            "22:figA6_domain_x_outcome"; do
  n="${pair%%:*}"; dst="${pair##*:}"
  src=$(ls ${n}_*.png 2>/dev/null | head -1)
  [ -n "$src" ] && cp "$src" "neurips/$dst.png" || echo "  !! no source for $n"
done
echo "  neurips set refreshed (3 generated + 7 copied)"
cd - >/dev/null || exit 1
echo "$(ls -1 "$AISIEVAL_CHARTS_OUT"/*.png | wc -l | tr -d ' ') figures"
[ -n "${FAILED:-}" ] && { echo "ONE OR MORE GENERATORS FAILED — figures are stale"; exit 1; }
exit 0
