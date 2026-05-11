# VPSs: Commands And Examples

## Key Terms

- **Package manager**: Tool for installing software.
- **System service**: Background process managed by OS.

## Commands

```bash
ssh user@your-server-ip
sudo apt update && sudo apt upgrade -y
python3 --version
git --version
mkdir -p ~/projects/learning
```

## Worked Example

```bash
cd ~/projects/learning
git clone https://github.com/example/repo.git
cd repo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/data_loader.py
```

## Advanced

### Deeper Concepts
- Treat a VPS as a reproducible system, not a one-time setup task. The strongest workflow uses a checklist for users, packages, firewall rules, and SSH hardening so environments can be rebuilt quickly and safely.
- Separate concerns between operating-system administration (accounts, permissions, updates), network security (SSH configuration, ports, firewall), and application deployment (runtime, dependencies, process manager).
- Understand remote risk management: a single permissive SSH or sudo configuration can expose all hosted workloads, so baseline hardening should happen before any service is deployed.
- Build command fluency gradually: each command should have a clear purpose, expected output, and rollback procedure.

### Free Platforms and Courses
- [DigitalOcean initial server setup](https://www.digitalocean.com/community/tutorial-collections/initial-server-setup) for practical step-by-step hardening and first-login workflows.
- [DigitalOcean Linux series](https://www.digitalocean.com/community/tutorial_series/getting-started-with-linux) for free Linux fundamentals directly relevant to VPS administration.
- [OpenSSH manual index](https://www.openssh.com/manual.html) for authoritative SSH command and configuration references.
- [MIT OpenCourseWare](https://ocw.mit.edu/) for broader systems and computing theory that supports infrastructure decision-making.

### Practice Path
- Day 1: Launch a fresh VPS and document every setup action in a markdown runbook; include why each step is required.
- Day 2: Apply SSH hardening (key-only auth, disable root login where appropriate, adjust fail-safe access strategy) and verify from a second terminal.
- Day 3: Configure firewall rules and test connectivity for allowed and blocked ports.
- Day 4: Rebuild the server from scratch using your runbook and compare time, errors, and confidence versus the first attempt.

### Suggested Mini-Projects
- Create a "golden VPS bootstrap" checklist that another learner can execute in under 30 minutes.
- Deploy a small Python script as a persistent service and add restart and logging notes to your runbook.
- Write a troubleshooting matrix for common VPS problems (SSH refused, permission denied, package conflicts, firewall lockout).
