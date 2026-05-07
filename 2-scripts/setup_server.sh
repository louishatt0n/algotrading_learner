#!/usr/bin/env bash
# setup_server.sh -- safer automated server setup for algo trading
#
# Usage:
#   chmod +x setup_server.sh
#   ./setup_server.sh
#
# Optional:
#   REQUIREMENTS_FILE=/root/learning/requirements.txt ./setup_server.sh

set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Please run as root (or with sudo)." >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

echo "=== Updating system packages ==="
apt-get update
apt-get upgrade -y

echo "=== Installing Docker ==="
apt-get install -y docker.io ca-certificates curl
systemctl enable docker
systemctl start docker

echo "=== Verifying Docker ==="
docker --version
systemctl is-active --quiet docker && echo "Docker service is active."

echo "=== Installing Miniconda ==="
if [[ ! -x "/root/miniconda3/bin/conda" ]]; then
  wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
  bash /tmp/miniconda.sh -b -p /root/miniconda3
  rm -f /tmp/miniconda.sh
fi

# Initialize conda for interactive shells.
if ! grep -q "miniconda3/bin/conda shell.bash hook" /root/.bashrc; then
  /root/miniconda3/bin/conda init bash >/dev/null
fi

# Use conda without relying on "source ~/.bashrc" in this script.
eval "$(/root/miniconda3/bin/conda shell.bash hook)"

echo "=== Configuring conda base environment ==="
/root/miniconda3/bin/conda config --set auto_activate_base true >/dev/null

echo "=== Installing Python packages into conda base ==="
/root/miniconda3/bin/conda run -n base python -m pip install --upgrade pip

REQUIREMENTS_FILE="${REQUIREMENTS_FILE:-./requirements.txt}"
if [[ -f "${REQUIREMENTS_FILE}" ]]; then
  echo "Using requirements file: ${REQUIREMENTS_FILE}"
  /root/miniconda3/bin/conda run -n base python -m pip install -r "${REQUIREMENTS_FILE}"
else
  echo "requirements.txt not found at ${REQUIREMENTS_FILE}"
  echo "Installing core packages directly."
  /root/miniconda3/bin/conda run -n base python -m pip install \
    numpy pandas matplotlib scikit-learn python-binance requests
fi

echo "=== Ensuring Jupyter is available in base ==="
/root/miniconda3/bin/conda run -n base python -m pip install jupyter

echo "=== Setup complete ==="
echo "Next steps:"
echo "1) source /root/.bashrc"
echo "2) conda activate base"
echo "3) python -m pip list"
