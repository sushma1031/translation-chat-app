## Introduction

This is a real-time chat application featuring language translation. It is hybrid Next.js + Python app that uses Next.js as the frontend and Flask as the API backend. It supports:

- text translation
- image text extraction and translation
- audio transcription, translation and synthesis
- english subtitle generation for videos

## How It Works

The Python/Flask server is mapped into to Next.js app under `/api/`.

This is implemented using [`next.config.js` rewrites](https://github.com/vercel/examples/blob/main/python/nextjs-flask/next.config.js) to map any request to `/api/:path*` to the Flask API, which is hosted in the `/api` folder.

On localhost, the rewrite will be made to the `127.0.0.1:5328` port, which is where the Flask server is running.

## Getting Started

First, install the dependencies:

```bash
npm install
pip install -r requirements.txt
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

The Flask server will be running on [http://127.0.0.1:5328](http://127.0.0.1:5328)
