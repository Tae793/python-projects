# 🎮 Twitch API Vibe-Coding Challenge

**Project**: Display the top live *Valorant* streams using Python and the Twitch API

---

## ✅ Your Mission

Use Python to fetch and display:

- The names of the top live Valorant streamers  
- Their stream titles  
- Current viewer counts  
- Links to their Twitch channels  

---

## 🧱 What You’ll Use

- Python (`requests` library)  
- Twitch API (Helix endpoints)  
- JSON parsing  
- Vibe-coding energy ⚡  

---

## 🛠️ Setup Instructions

- Ideally, use WSL and install Python there (see [here](https://learn.microsoft.com/en-us/windows/python/web-frameworks) for a guide)
- Install git inside WSL if it's not already there
- Clone this git repo
- Copy the .env-example file to a new file: .env

### Log in to Twitch and set up MFA

- Log in to Twitch
- If you don't have MFA set up already you'll need to:
  - Click on your profile icon in the top-right of the screen and click on Settings
  - Click Security and Privacy
  - Click Set Up Two-Factor Authentication
  - Click Enable 2FA and follow the instructions

### Create a Twitch Developer App
- Go to: [https://dev.twitch.tv/console/apps](https://dev.twitch.tv/console/apps)  
- Click **Register Your Application**  
  - Name: *anything you like* (this must be globally unique)
  - OAuth Redirect URL: `http://localhost`  
  - Category: *Application Integration*
  - Client Type: *Confidential*

### Generate a Client Secret
- Click the `Manage` button on your new Application
- Click the `New Secret` button
- Copy and paste both the Client ID and the Client Secret into the relevant space in the `.env` file
- Run the following in a terminal to load these into your environment:
  ```
  set -a && source .env && set +a
  ```

---

### Get an Access Token (1-time setup)

Using the same terminal run:

```bash
curl -X POST 'https://id.twitch.tv/oauth2/token' \
  -d "client_id=${TWITCH_CLIENT_ID}" \
  -d "client_secret=${TWITCH_CLIENT_SECRET}" \
  -d "grant_type=client_credentials"
```

- Copy the **access token** and paste it in the relevant space in the `.env` file
- Load the variables in the file into your environment again:
  ```
  set -a && source .env && set +a
  ```

---

### Run it!

```bash
python twitch_api_vibecoding.py
```

---

## 💡 Bonus Challenges

- ✅ Show only streamers with more than 5000 viewers
- ✅ Display stream duration or language
- ✅ Try a different game (e.g., Apex Legends)
- ✅ Make it a Flask app and show results in a browser

---

## 🧠 DevOps / Platform Engineer Tie-In

- **APIs** power modern platforms  
- **Monitoring Twitch streams** = like watching service traffic  
- **Rate limits** = like performance scaling  
- **CI/CD** = How Twitch rolls out new features to streamers  

---

## 💬 Final Tip

If you get stuck, ask for help — that’s what DevOps engineers do every day.

**Happy hacking!**  
