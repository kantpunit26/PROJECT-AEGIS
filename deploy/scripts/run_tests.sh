#!/bin/bash
# ==============================================================================
# PROJECT AEGIS — AUTOMATED TEST SUITE RUNNER
# ==============================================================================
set -e

echo "[AEGIS] Running backend test suite..."
pytest backend/tests -v --durations=10

echo "[AEGIS] All automated tests passed successfully."

