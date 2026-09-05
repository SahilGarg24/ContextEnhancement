@echo off
REM ============================================================
REM  Key Entities Ranking — run utility
REM  Edit config.txt with your paths, then double-click this file
REM ============================================================
echo Starting Key Entities Ranking...
python ranking_utility.py

echo.
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Ranking failed. See output above for details.
) else (
    echo Done. Output files:
    echo   measure_ranks.csv
    echo   dimattr_ranks.csv
)
pause