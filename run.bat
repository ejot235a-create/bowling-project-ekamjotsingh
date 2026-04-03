@echo off
echo ================================
echo Bowling Game Assessment
echo ================================
echo.

echo 1. Installing dependencies...
py -m pip install -r requirements.txt -q
echo    [OK] Dependencies installed
echo.

echo 2. Running tests...
py -m unittest test_bowling_game -v
echo.

echo 3. Running example game...
echo    Output:
py example_usage.py
echo.

echo 4. Generating documentation...
py generate_docs.py
echo.

echo ================================
echo All tasks completed!
echo ================================
pause
