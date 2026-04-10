---
title: Customer Support Env
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# Customer Support Resolution Environment (CSRE)

##  Live Demo
https://bhagavatkumar-customer-support-env-v2.hf.space/docs

---

## Overview
This project simulates a real-world customer support system where an AI agent interacts with user queries.

## Features
- Multi-step environment
- Reward-based learning
- Task-based evaluation
- FastAPI backend

---

## API Endpoints

- `/reset` → Start new task  
- `/state` → Get current state  
- `/step` → Take action  

---

## Example Step Input

```json
{
  "action_type": "respond",
  "content": "I will help you reset your password"
}
