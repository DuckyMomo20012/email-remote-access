<div align="center">

  <h1>Email Remote Access</h1>

  <p>
    Control remote computer using email
  </p>

<!-- Badges -->
<p>
  <a href="https://github.com/DuckyMomo20012/email-remote-access/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/DuckyMomo20012/email-remote-access" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/DuckyMomo20012/email-remote-access" alt="last update" />
  </a>
  <a href="https://github.com/DuckyMomo20012/email-remote-access/network/members">
    <img src="https://img.shields.io/github/forks/DuckyMomo20012/email-remote-access" alt="forks" />
  </a>
  <a href="https://github.com/DuckyMomo20012/email-remote-access/stargazers">
    <img src="https://img.shields.io/github/stars/DuckyMomo20012/email-remote-access" alt="stars" />
  </a>
  <a href="https://github.com/DuckyMomo20012/email-remote-access/issues/">
    <img src="https://img.shields.io/github/issues/DuckyMomo20012/email-remote-access" alt="open issues" />
  </a>
  <a href="https://github.com/DuckyMomo20012/email-remote-access/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/DuckyMomo20012/email-remote-access.svg" alt="license" />
  </a>
</p>

<h4>
    <a href="https://github.com/DuckyMomo20012/email-remote-access/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/DuckyMomo20012/email-remote-access">Documentation</a>
  <span> · </span>
    <a href="https://github.com/DuckyMomo20012/email-remote-access/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/DuckyMomo20012/email-remote-access/issues/">Request Feature</a>
  </h4>
</div>

<br />

<!-- Table of Contents -->

# :notebook_with_decorative_cover: Table of Contents

- [About the Project](#star2-about-the-project)
  - [Screenshots](#camera-screenshots)
  - [Tech Stack](#space_invader-tech-stack)
  - [Features](#dart-features)
  - [Environment Variables](#key-environment-variables)
- [Getting Started](#toolbox-getting-started)
  - [Prerequisites](#bangbang-prerequisites)
  - [Run Locally](#running-run-locally)
- [Usage](#eyes-usage)
- [Roadmap](#compass-roadmap)
- [Contributing](#wave-contributing)
  - [Code of Conduct](#scroll-code-of-conduct)
- [FAQ](#grey_question-faq)
- [License](#warning-license)
- [Contact](#handshake-contact)
- [Acknowledgements](#gem-acknowledgements)

<!-- About the Project -->

## :star2: About the Project

<!-- Screenshots -->

### :camera: Screenshots

<div align="center">
  <img src="https://placehold.co/600x400?text=Your+Screenshot+here" alt="screenshot" />
</div>

<!-- TechStack -->

### :space_invader: Tech Stack

<details>
  <summary>Client</summary>
  <ul>
    <li><a href="https://www.python.org/">Python</a></li>
    <li><a href="https://python-socketio.readthedocs.io/en/latest/index.html">SocketIO</a></li>
    <li><a href="https://docs.python.org/3/library/tkinter.html">Tkinter</a></li>
    <li><a href="https://dearpygui.readthedocs.io/en/latest/">Dear PyGui</a></li>
  </ul>
</details>

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="https://www.python.org/">Python</a></li>
    <li><a href="https://python-socketio.readthedocs.io/en/latest/index.html">SocketIO</a></li>
    <li><a href="https://fastapi.tiangolo.com/">FastAPI</a></li>
    <li><a href="https://www.uvicorn.org/">uvicorn</a></li>
  </ul>
</details>

<!-- Features -->

### :dart: Features

- **Client App:** A simple GUI app to control remote computer

  - Shutdown/logout:
    - [x] Shutdown computer.
    - [x] Logout computer.
  - MAC address:
    - [x] Get computer's MAC address.
  - Livescreen:
    - [x] Live stream computer's screen.
    - [x] Save screenshot.
  - Directory:
    - [x] List all files in a directory.
    - [x] Copy files to client computer.
    - [x] Copy files to server computer.
    - [x] Delete files.
  - App process:
    - [x] List all processes.
    - [x] List applications.
    - [x] Kill processes.
  - Registry:
    - [x] Create registry key.
    - [x] Delete registry key.
    - [x] Get registry value.
    - [x] Set registry value.

- **Mail App:** A simple GUI app to control remote computer using email

  - Shutdown/logout:
    - [x] Shutdown computer.
    - [x] Logout computer.
  - MAC address:
    - [x] Get computer's MAC address.
  - Livescreen:
    - [ ] Live stream computer's screen.
    - [x] Save screenshot.
  - Directory:
    - [x] List all files in a directory.
    - [ ] Copy files to client computer.
    - [ ] Copy files to server computer.
    - [ ] Delete files.
  - App process:
    - [x] List all processes.
    - [x] List applications.
    - [ ] Kill processes.
  - Registry:
    - [ ] Create registry key.
    - [ ] Delete registry key.
    - [ ] Get registry value.
    - [ ] Set registry value.

<!-- Env Variables -->

### :key: Environment Variables

To run this project, you will need to add the following environment variables to
your `.env` file:

- **App configs:**

  `TEST_VAR`: Description of this environment variable.

E.g:

```
# .env
TEST_VAR="my secret key"
```

You can also check out the file `.env.example` to see all required environment
variables.

<!-- Getting Started -->

## :toolbox: Getting Started

<!-- Prerequisites -->

### :bangbang: Prerequisites

- Python: `>= 3.9`.

- This project uses [Poetry](https://python-poetry.org/) as package manager:

  Linux, macOS, Windows (WSL)

  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

  Read more about installation on
  [Poetry documentation](https://python-poetry.org/docs/master/#installation).

<!-- Run Locally -->

### :running: Run Locally

Clone the project:

```bash
git clone https://github.com/DuckyMomo20012/email-remote-access.git
```

Go to the project directory:

```bash
cd email-remote-access
```

Install dependencies:

```bash
poetry install
```

OR:

Export Poetry dependencies to file `requirements.txt`:

```bash
poetry export -f requirements.txt --output requirements.txt
```

> **Note**: You can add option: `--dev` to include development dependencies.

Then install dependencies with `pip`:

```bash
pip install -r requirements.txt
```

---

Activate the virtual environment:

```bash
poetry shell
```

Start the program:

- **Server:**

  ```bash
  poe dev
  ```

  OR

  ```bash
  poe dev server
  ```

- **Client App:**

  ```bash
  poe dev client
  ```

- **Mail App:**

  ```bash
  poe dev mail
  ```

- **Dear PyGui Demo:**

  ```bash
  poe dev demo
  ```

<!-- Usage -->

## :eyes: Usage

- **Server:**

  Run the server:

  ```bash
  poe dev
  ```

  OR

  ```bash
  poe dev server
  ```

  The server will run on with port `5656` and with host `0.0.0.0`, which is
  **the IP address of your local machine**.

- **Client App:**

  Run the client app:

  ```bash
  poe dev client
  ```

  Connect to the server by entering the server's IP address and port:

  - **IP address:** The IP address of your server machine.
  - **Port:** `5656`.

- **Mail App:**

  > **Note**: To use this app, you need to provide the `credentials.json` file
  > in the `src/mail` directory. Please follow the instructions in the page:
  > [Python quickstart](https://developers.google.com/gmail/api/quickstart/python)
  > to create your own App and download the `credentials.json` file.

  Run the mail app:

  ```bash
  poe dev mail
  ```

  If this is the first time you run the app, you will be asked to authorize the
  app. The app will open a browser window and ask you to log in to your Google
  account.

  After you log in, you will be asked to give the app permissions:

  - **Read all resources and their metadata—no write operations.**
  - **Send messages only. No read or modify privileges on mailbox.**

  The token will be saved in the file `token.json` in the `src/mail` directory.

  > **Warning**: The file `credentials.json` and `token.json` are **sensitive
  > files**, **DO NOT** share them with anyone.

  Connect to the server by entering the server's IP address and port:

  - **IP address:** The IP address of your server machine.
  - **Port:** `5656`.

- **Dear PyGui Demo:**

  Run the demo:

  ```bash
  poe dev demo
  ```

  The demo will demonstrate all the features of the Dear PyGui library.

- **CLI:**

  ```bash
  Usage: cli.py [OPTIONS] [SERVICE]:[server|client|mail]

  Arguments:
    [SERVICE]:[server|client|mail]  Service to run  [default: server]

  Options:
    --help  Show this message and exit.
  ```

<!-- Roadmap -->

## :compass: Roadmap

- [ ] Rebuild the server with `Dear PyGui`.
- [ ] Rebuild the client app with `Dear PyGui`.
- [ ] Support more features for Mail App.
  - [ ] Copy files to client computer.
  - [ ] Copy files to server computer.
  - [ ] Delete files.

<!-- Contributing -->

## :wave: Contributing

Contributions are always welcome!

<!-- Code of Conduct -->

### :scroll: Code of Conduct

Please read the
[Code of Conduct](https://github.com/DuckyMomo20012/email-remote-access/blob/main/CODE_OF_CONDUCT.md).

<!-- FAQ -->

## :grey_question: FAQ

- Why do you migrate to `SocketIO`?

  - The server and client app are built with normal `socket`, the dataflow is
    somewhat harder to track, debug and maintain. So I decided to migrate to
    `SocketIO` for better dataflow management.

- Why do you migrate to `Dear PyGui`?

  - The server and client app are built with `tkinter`, which is a bit hard to
    use and maintain. The `tkinter`'s `mainloop` is quite hard to close
    manually, and it's not shutdown properly when the program is closed. So I
    decided to migrate to `Dear PyGui` for better UI and better dataflow
    management.

<!-- License -->

## :warning: License

Distributed under MIT license. See
[LICENSE](https://github.com/DuckyMomo20012/email-remote-access/blob/main/LICENSE)
for more information.

<!-- Contact -->

## :handshake: Contact

Duong Vinh - [@duckymomo20012](https://twitter.com/duckymomo20012) -
tienvinh.duong4@gmail.com

Project Link:
[https://github.com/DuckyMomo20012/email-remote-access](https://github.com/DuckyMomo20012/email-remote-access).

<!-- Acknowledgments -->

## :gem: Acknowledgements

Here are useful resources and libraries that we have used in our projects:

- [Awesome Readme Template](https://github.com/Louis3797/awesome-readme-template):
  A detailed template to bootstrap your README file quickly.
- [Dear PyGui](https://dearpygui.readthedocs.io/en/latest/): Dear PyGui is an
  easy-to-use, dynamic, GPU-Accelerated, cross-platform graphical user interface
  toolkit(GUI) for Python. It is “built with”
  [Dear ImGui](https://github.com/ocornut/imgui).
- [SocketIO](https://python-socketio.readthedocs.io/en/latest/): Python client
  and server for Socket.IO.
- [FastAPI](https://fastapi.tiangolo.com/): FastAPI framework, high performance,
  easy to learn, fast to code, ready for production.
- [uvicorn](https://www.uvicorn.org/): An ASGI web server, for Python.
