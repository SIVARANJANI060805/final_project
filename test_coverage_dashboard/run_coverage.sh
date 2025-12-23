#!/bin/bash
coverage run -m pytest
coverage json -o coverage.json
