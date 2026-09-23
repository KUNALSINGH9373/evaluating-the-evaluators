#!/usr/bin/env bash
# The ICLR figure set: vector PDFs, MATS colours, no in-figure titles or captions, larger type.
#
# Every difference from the default build is an environment variable read by palette.py, so
# there is one code path and one set of numbers behind both sets. Nothing here is a fork.
#
#   AISIEVAL_CHART_FORMAT=pdf     vector output; pdf.fonttype 42 keeps the text selectable
#                                 and searchable inside the compiled paper
#   AISIEVAL_PALETTE=mats         the MATS design tokens, read from matsprogram.org's CSS
#   AISIEVAL_CHART_TITLES=off     a figure title belongs in \caption, not baked into artwork
#   AISIEVAL_CHART_NOTES=off      so does every explanatory sentence — CAPTIONS.md collects them
#   AISIEVAL_CHART_FONTSCALE      every explicit fontsize= is multiplied by this
#   AISIEVAL_CHART_PAD            savefig pad_inches, cut from 0.42 to trim the white margin
set -euo pipefail
cd "$(dirname "$0")"
R="$(cd .. && pwd)"

export AISIEVAL_CHARTS_OUT="${AISIEVAL_CHARTS_OUT:-$R/charts/ICLR}"
export AISIEVAL_CHART_FORMAT=pdf
export AISIEVAL_PALETTE=mats
export AISIEVAL_CHART_TITLES=off
export AISIEVAL_CHART_NOTES=off
export AISIEVAL_CHART_FONTSCALE="${AISIEVAL_CHART_FONTSCALE:-1.18}"
export AISIEVAL_CHART_PAD="${AISIEVAL_CHART_PAD:-0.06}"

mkdir -p "$AISIEVAL_CHARTS_OUT"
echo "building the ICLR set into $AISIEVAL_CHARTS_OUT"
echo "  pdf · MATS palette · no titles · no captions · fontscale $AISIEVAL_CHART_FONTSCALE"

FAILED=""
for s in charts.py charts2.py hero.py tree.py fig_developer.py fig12_scope.py fig15b.py \
         fig_finding.py fig_action_level.py fig_examples.py fig_examples2.py \
         nfig1_pipeline.py nfig2_matrix.py nfigA_access.py; do
  printf '  %-22s ' "$s"
  if python3 "$s" >/dev/null 2>/tmp/cb_iclr_err; then echo ok
  else echo "FAILED"; sed 's/^/      /' /tmp/cb_iclr_err; FAILED=1; fi
done

python3 write_captions.py
echo "$(find "$AISIEVAL_CHARTS_OUT" -name '*.pdf' | wc -l | tr -d ' ') PDFs"
[ -n "$FAILED" ] && { echo "ONE OR MORE GENERATORS FAILED — the set is incomplete"; exit 1; }
exit 0
