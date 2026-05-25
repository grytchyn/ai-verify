#!/bin/bash
cd /root/ai-compliance-unified
source venv/bin/activate
export DATABASE_URL="sqlite:///./data/app.db"
mkdir -p data
python -m app.main