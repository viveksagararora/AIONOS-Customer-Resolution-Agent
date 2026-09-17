# AIONOS Customer Resolution Agent

## Overview
Customer-facing resolution agent for airline disruption scenarios.

The system evaluates customer requests using predefined airline policies and determines:

- Eligible actions
- Restricted actions
- Escalation requirements

## Features

- Flight cancellation handling
- Flight delay compensation
- Refund processing
- Rebooking support
- Escalation detection
- Policy-based decision engine

## Tech Stack

- Python
- Streamlit

## Project Structure

app.py
data.py
rule_engine.py
response_generator.py

## Run Locally

pip install -r requirements.txt

streamlit run app.py

## Test Scenarios

- Priya Nair (Cancelled Flight)
- Arvind Kulkarni (4 Hour Delay)
- Meher Kaur (6 Hour Delay + Fare Difference)
