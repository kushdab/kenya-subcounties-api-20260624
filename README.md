# Kenya Subcounties API

A RESTful API providing geographic administrative data for Kenyan counties and their respective sub-counties.

## Features
- List all counties
- Get sub-counties by county name
- Search for sub-counties globally
- Health check endpoint

## API Endpoints
- `GET /api/v1/health`: Check API status
- `GET /api/v1/counties`: List all 47 counties
- `GET /api/v1/counties/<county_name>`: Get sub-counties for specific county
- `GET /api/v1/search/subcounties/<query>`: Search for sub-counties

## Installation
1. `pip install -r requirements.txt`
2. `python app.py`