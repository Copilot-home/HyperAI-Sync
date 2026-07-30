# ═══════════════════════════════════════════════════════════
# 🎼 Symphony Control Center - Dockerfile
# Orchestrates 463 VSCode Extensions as Digital Organisms
# Creator: Andy (alpha_prime_omega) - Verification: 4287
# ═══════════════════════════════════════════════════════════

FROM python:3.11-slim

# Metadata
LABEL maintainer="Andy (alpha_prime_omega)"
LABEL version="2.1.0"
LABEL description="DAIOF Symphony Control Center for Extension Ecosystem"
LABEL verification="4287"

# System dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    sqlite3 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/cache /app/state

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DAIOF_CREATOR=Andy
ENV DAIOF_VERIFICATION_CODE=4287
ENV DAIOF_VERSION=2.1.0

# Expose ports
EXPOSE 5000 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run Symphony Control Center
CMD ["python", "symphony_controller.py"]
