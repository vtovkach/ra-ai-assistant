# Setup Instructions

This program requires two files to be placed inside the **config/** directory before running:

---

## 1. `api_key`
- This file must contain your **OpenAI API key**.
- The file should have **only one line**, for example:
  ```
  sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  ```

---

## 2. `questions`
- This file defines the set of questions used by the program.
- Each question must be **separated by a line starting with an asterisk (`*`)**.
- Each question itself should be on a **new line**.
- The document must **end with an asterisk (`*`)**.

### Example:
```
What goals did the resident discuss?
*
What resources were mentioned?
*
What follow-up actions are planned?
*
```
