python -m black .
if ($LASTEXITCODE -ne 0) { exit 1 }

python -m flake8 .
if ($LASTEXITCODE -ne 0) { exit 1 }

python -m mypy .
if ($LASTEXITCODE -ne 0) { exit 1 }
