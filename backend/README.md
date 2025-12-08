# FastAPI Backend

This is a FastAPI application.

## Installation

First, navigate to the `backend` directory:

```bash
cd backend
```

To install the project dependencies, make sure you have `uv` installed, then run:

```bash
uv sync
```

## How to run the application

To run the application with automatic code reloading (useful during development):

```bash
uv run uvicorn main:app --reload
```

To run the application without reloading:

```bash
uv run uvicorn main:app
```
