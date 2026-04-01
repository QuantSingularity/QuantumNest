FROM node:20-slim AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --omit=dev

COPY . .

# ── Runtime ───────────────────────────────────────────────────────────────────
FROM node:20-slim AS runtime

WORKDIR /app

RUN useradd --no-create-home --shell /bin/false nodeuser

COPY --from=builder /app /app

RUN chown -R nodeuser:nodeuser /app

USER nodeuser

EXPOSE 8545

CMD ["npx", "hardhat", "node", "--hostname", "0.0.0.0"]
