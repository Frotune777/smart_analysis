# AngelOne Broker Setup Guide

## Required Credentials

### Stored in `.env` file (One-time setup):
1. **ANGEL_API_KEY** - Your API Key from AngelOne Developer Portal ✅

### Requested during authentication (Each login):
2. **Client Code** - Your AngelOne User ID (e.g., A12345)
3. **Trading PIN** - Your 4-digit Trading PIN
4. **TOTP Code** - 6-digit code from your authenticator app

> **Following OpenAlgo's secure pattern**: Only API Key is stored, sensitive credentials requested when needed!

---

## Quick Setup (3 Steps)

### Step 1: Get Your API Key
From your screenshot, you have the API KEY (shown with dots). Copy it!

### Step 2: Configure in `.env`
```bash
# Edit .env file
ACTIVE_BROKER=angel
ANGEL_API_KEY=your_api_key_from_screenshot
BROKER_API_KEY=your_api_key_from_screenshot
```

### Step 3: Authenticate When Needed
When you use trading features, the system will ask for:
- Client Code (your user ID)
- Trading PIN (4 digits)
- TOTP (6 digits from authenticator)

This is your **4-digit Trading PIN** (NOT your login password)

**If you don't remember it:**
1. Go to AngelOne App/Website
2. Settings → Security → Reset Trading PIN
3. Verify via OTP
4. Set new 4-digit PIN

### 4. Setup TOTP (If not already enabled)

**Enable 2FA:**
1. AngelOne App → Settings → Security
2. Enable "Two-Factor Authentication"
3. Scan QR code with Google Authenticator
4. Save the setup (you'll enter the 6-digit code during login)

---

## Configuration Steps

### 1. Create `.env` file

```bash
cd /home/fortune/Desktop/Python_Projects/trader_start
cp .env.example .env
```

### 2. Edit `.env` file

```bash
# Active Broker Selection
ACTIVE_BROKER=angel

# AngelOne Credentials
ANGEL_API_KEY=your_api_key_from_screenshot
ANGEL_CLIENT_CODE=A12345
ANGEL_PASSWORD=1234
# Note: TOTP will be requested during authentication

# Legacy (auto-set)
BROKER_API_KEY=your_api_key_from_screenshot
```

### 3. Configure in Dashboard

1. Open Dashboard: `streamlit run dashboard.py`
2. Go to **"Broker Configuration"**
3. Select **"AngelOne"**
4. Enter your credentials:
   - API Key: (from screenshot)
   - Client Code: Your user ID
   - Password: Your 4-digit PIN
5. Click **"💾 Save Credentials"**

### 4. Authenticate (When Needed)

When you need to authenticate:
1. System will prompt for TOTP
2. Open your authenticator app
3. Enter the current 6-digit code
4. Click "Authenticate"

---

## Example `.env` Configuration

```bash
ACTIVE_BROKER=angel

ANGEL_API_KEY=AbCdEfGh1234567890
ANGEL_CLIENT_CODE=A12345
ANGEL_PASSWORD=1234

BROKER_API_KEY=AbCdEfGh1234567890
```

---

## Security Notes

- ✅ `.env` file is gitignored (safe from version control)
- ✅ TOTP not stored (requested each time for security)
- ✅ Credentials encrypted in transit
- ⚠️ Keep `.env` file permissions restricted (chmod 600)

---

## Troubleshooting

### "Invalid Client Code"
- Check format (usually starts with letter + numbers)
- Verify from AngelOne app/website

### "Invalid Trading PIN"
- This is 4-digit PIN, not login password
- Reset if forgotten via AngelOne app

### "TOTP Authentication Failed"
- Ensure time is synced on your device
- TOTP codes expire every 30 seconds
- Try the next code if current one fails

### "API Key Invalid"
- Copy exact key from AngelOne developer portal
- No spaces or extra characters
- Check if API key is active

---

## What's Different from OpenAlgo?

Following OpenAlgo's best practice:
- **Static credentials** (API Key, Client Code, Password) → Stored in `.env`
- **Dynamic credentials** (TOTP) → Requested during authentication

This is more secure and user-friendly!
