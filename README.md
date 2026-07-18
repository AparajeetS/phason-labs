# Phason Labs

Source for the Phason Labs research website.

## Controlled evidence

The site publishes a frozen synthetic benchmark of the public `traintools` and
`mbe-eval` PyPI releases. Its protocol, reproduction script, run-level data,
summary, correction log, and withheld MBE report live under
`public/evidence/traintools-controlled-2026-07-18/`.

The website reports only results that passed their predeclared gates. The MBE
table is disclosed but excluded from promotional claims because its random
negative control missed the frozen point-estimate threshold.

## Development

Requires Node.js 22.13 or newer.

```bash
npm ci
npm run build
npm test
```

The application uses vinext and is deployed through OpenAI Sites.
