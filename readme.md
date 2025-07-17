# BlockBuddy

A simple Python script to block distracting websites on macOS using `/etc/hosts`.

You can configure which sites to block, which days, and during what hours. It supports dry-run mode, and logging.

---

## 🔧 Setup

1. Clone the repo:
```bash
   git clone https://github.com/yourusername/BlockBuddy.git
   cd BlockBuddy
```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required package:

   ```bash
   pip install python-dotenv
   ```

4. Create a `.env` file:

   ```env
   BLOCKED_SITES=facebook.com,instagram.com,twitter.com
   BLOCK_DAYS=MON,TUE,WED,THU,FRI
   BLOCK_START=09:00
   BLOCK_END=20:00
   ```

---

## 🚀 Usage

Block websites (only during configured time):

```bash
sudo python3 blocker.py --block
```

Dry run (see what would be blocked):

```bash
sudo python3 blocker.py --block --dry-run
```

Unblock everything:

```bash
sudo python3 blocker.py --unblock
```

---

## 📒 Notes

* Only works on macOS.
* Requires `sudo` since it modifies system files.
* Logs actions to `blockbuddy.log`.

---

## ✅ Example `.env`
or Check .env_example file

```env
BLOCKED_SITES=facebook.com,youtube.com
BLOCK_DAYS=MON,TUE,WED,THU,FRI
BLOCK_START=09:00
BLOCK_END=20:00
```

---

## License

MIT – use it or improve it as you like.
