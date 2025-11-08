# 🔑 API Key Setup Instructions

## Quick Setup

### Option 1: Edit config.py directly (Simplest)

1. Open `src/config.py`
2. Find this line:
   ```python
   GROQ_API_KEY: Optional[str] = os.getenv(
       "GROQ_API_KEY",
       "put-your-groq-api-key-here"  # ⚠️ REPLACE THIS
   )
   ```
3. Replace `"put-your-groq-api-key-here"` with your actual API key
4. **Important:** Don't commit this change to GitHub!

### Option 2: Use Environment Variable (Recommended for GitHub)

**Windows PowerShell:**
```powershell
$env:GROQ_API_KEY="your-actual-api-key-here"
python main.py
```

**Linux/Mac:**
```bash
export GROQ_API_KEY="your-actual-api-key-here"
python main.py
```

### Option 3: Use .env file (Best Practice)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your key:
   ```
   GROQ_API_KEY=your-actual-api-key-here
   ```

3. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```

4. The `.env` file is already in `.gitignore` (won't be pushed to GitHub)

## Getting Your API Key

1. Visit: https://console.groq.com/
2. Sign up for a free account
3. Go to: https://console.groq.com/keys
4. Click "Create API Key"
5. Copy your key (starts with `gsk_...`)

## Free Tier Limits

- **100,000 tokens per day**
- If you hit the limit, wait 24 hours or upgrade

## Recommended Model (Uses Fewer Tokens)

In `src/config.py`, change:
```python
LLM_MODEL = "llama-3.1-8b-instant"  # Faster, uses fewer tokens
```

Instead of:
```python
LLM_MODEL = "llama-3.3-70b-versatile"  # More powerful, uses more tokens
```

## Security Best Practices

✅ **DO:**
- Use environment variables for API keys
- Keep `.env` in `.gitignore`
- Use `.env.example` to show required variables

❌ **DON'T:**
- Commit API keys to GitHub
- Share API keys publicly
- Hardcode keys in source files (except for local testing)

## Troubleshooting

**Error: "The api_key client option must be set"**
- You haven't set your API key
- Follow Option 1, 2, or 3 above

**Error: "Rate limit reached"**
- You've used your daily 100k token quota
- Wait 24 hours or upgrade your plan
- Use a smaller model (llama-3.1-8b-instant)

**Key not working after setting environment variable:**
- Restart your terminal/PowerShell
- Make sure there are no extra spaces in the key
- Check that the key starts with `gsk_`
