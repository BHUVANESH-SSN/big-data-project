# Setup with Virtual Environment

## For WSL/Linux

### Create and Activate Virtual Environment
```bash
cd ~/fraud-detection-bigdata  # or /mnt/c/fraud-detection-bigdata

# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
pip install kafka-python

# You should see (venv) in your prompt now
```

### Run Producer and Consumer
**Always activate venv first in each terminal:**

**Terminal 1 - Consumer:**
```bash
cd ~/fraud-detection-bigdata
source venv/bin/activate
python kafka_consumer.py
```

**Terminal 2 - Producer:**
```bash
cd ~/fraud-detection-bigdata
source venv/bin/activate
python kafka_producer.py
```

**Terminal 3 - View Results:**
```bash
cd ~/fraud-detection-bigdata
source venv/bin/activate
python view_results.py
```

### Deactivate venv when done:
```bash
deactivate
```

---

## For Windows PowerShell (if you decide to use Windows Kafka)

### Create and Activate Virtual Environment
```powershell
cd C:\fraud-detection-bigdata

# Create venv
python -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install kafka-python
```

### Run Producer and Consumer
```powershell
# Terminal 1 - Consumer
cd C:\fraud-detection-bigdata
.\venv\Scripts\Activate.ps1
python kafka_consumer.py

# Terminal 2 - Producer
cd C:\fraud-detection-bigdata
.\venv\Scripts\Activate.ps1
python kafka_producer.py
```

### Deactivate:
```powershell
deactivate
```

---

## Quick Reference:

**Activate venv (Linux/WSL):** `source venv/bin/activate`
**Activate venv (Windows):** `.\venv\Scripts\Activate.ps1`
**Deactivate:** `deactivate`

✅ This keeps kafka-python isolated and won't conflict with other projects!
