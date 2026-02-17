# ASE GradeWatcher

As a 2nd-year **Economic Cybernetics (CSIE)** student at ASE Bucharest, I’ve learned that the most stressful part of an exam isn't the test itself - it's the endless waiting for the results. 
We've all been there: waking up at 3 AM just to hit "Refresh" on the Webstudent portal, hoping the OOP or Statistics grade finally appeared. After a few sleepless nights, I decided to let a script do the "heavy lifting" for me. That’s how **GradeWatcher** was born.

### What it Does
This isn't just a script - it's a fully autonomous monitoring system:
* **Automatic Login:** Navigates the ASE Webstudent portal, handling the tricky ASP.NET ViewState and session cookies.
* **Intelligent Scanning:** It doesn't just check the page; it parses the grade table and compares it with a local "memory" to detect even the slightest change.
* **Discord Alerts:** The second a professor uploads a grade, I get an instant notification on my private Discord server.
* **Cloud-Native:** It doesn't run on my laptop. It lives in the cloud via GitHub Actions, running 24/7.

### The Tech Stack
* **Language:** Python 3.x
* **Scraping:** BeautifulSoup4 & Requests
* **Automation:** GitHub Actions (CI/CD)
* **Data Persistence:** JSON-based state tracking

---

### Lessons Learned
Building this taught me more than any textbook could:
1. **Real-world Scraping:** Handling legacy web portals and security tokens.
2. **DevOps & Automation:** Moving a local script to a fully automated cloud environment.
3. **Security Best Practices:** Managing sensitive credentials using GitHub Secrets.

---

### Educational Disclaimer
This project was developed strictly for **educational purposes** to demonstrate automation and web scraping techniques. 
* **Respect the University:** Users must respect the terms and conditions of the ASE Bucharest Webstudent portal. 
* **Fair Use:** The script is configured with a reasonable delay to ensure it does not overwhelm the university's servers. 
* **Responsibility:** I do not encourage or support any use of this tool that violates university policies or data privacy.

---

### Setup
1. Fork this repository (Keep it **Private**).
2. Add your credentials to GitHub Secrets (`STUDENT_USER`, `STUDENT_PASS`, `DISCORD_WEBHOOK`).
3. The workflow triggers automatically based on the schedule in `.github/workflows/main.yml`.
