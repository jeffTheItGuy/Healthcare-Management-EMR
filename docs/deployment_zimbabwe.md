# Deployment Guide — Zimbabwe

## Hardware Requirements

| Environment | CPU | RAM | Storage | Notes |
|---|---|---|---|---|
| Dev / Small Clinic | 2-core | 8GB | 100GB SSD | Single server |
| District Hospital | 4-core | 16GB | 500GB SSD | UPS + generator required |
| Central Hospital | 8-core | 32GB | 1TB SSD RAID | Separate DB server recommended |

## Power & Connectivity

- **UPS**: 1500VA minimum (30 min runtime)
- **Generator**: Auto-start diesel, tested weekly
- **Network**: Static IP or DDNS; 4G failover (NetOne/Telecel/Econet)

## Single-Server Deployment

```bash
git clone https://github.com/yourorg/zim-emr.git
cd zim-emr
cp .env.example .env
# Edit .env with production credentials
sudo sysctl -w vm.overcommit_memory=1
docker compose -f docker-compose.prod.yml up -d