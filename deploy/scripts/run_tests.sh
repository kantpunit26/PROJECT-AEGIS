#!/bin/bash
# ==============================================================================
# PROJECT AEGIS 2.0 — AUTOMATED TEST SUITE RUNNER
# ==============================================================================
set -e

echo "[AEGIS 2.0] Running backend test suite..."
pytest backend/tests -v --durations=10

echo "[AEGIS 2.0] All automated tests passed successfully."
