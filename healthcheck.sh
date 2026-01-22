#!/bin/sh
curl -fs --max-time 2 http://localhost:8000/health || exit 1
