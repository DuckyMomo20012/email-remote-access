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
  - [Server](#server)
  - [Server App](#server-app)
  - [Client App](#client-app)
  - [Mail App](#mail-app)
    - [Authorize the app](#authorize-the-app)
    - [Send mail](#send-mail)
    - [Instruction format](#instruction-format)
    - [Supported instructions](#supported-instructions)
    - [Execute instructions](#execute-instructions)
  - [Dear PyGui Demo](#dear-pygui-demo)
  - [CLI](#cli)
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

- Server App:

<div align="center">
  <img src="https://user-images.githubusercontent.com/64480713/234619906-c093e3a7-d396-4e17-93ab-75bc9fe4e52c.png" alt="server_app_screenshot" />
</div>

- Client App:

<div align="center">
  <img src="https://user-images.githubusercontent.com/64480713/234620646-cd42fc24-a787-4572-9725-b14ce9648be9.png" alt="client_app_screenshot" />
</div>

- Mail App:

<div align="center">
  <img src="https://user-images.githubusercontent.com/64480713/234620319-cc0a6ec3-00b4-41b5-928c-3133c5b7cdcf.png" alt="mail_app_screenshot" />
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
    - [ ] Live stream computer's screen. (Won't do)
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

Install dependencies with `pip`:

```bash
pip install -r requirements.txt
```

<details>
<summary>Export dependencies from </code>pyproject.toml</code></summary>

Export Poetry dependencies to file `requirements.txt`:

```bash
poetry export -f requirements.txt --output requirements.txt
```

> **Note**: You can add option: `--dev` to include development dependencies.

</details>

---

Activate the virtual environment:

```bash
poetry shell
```

Start the program:

- **Server App:**

  ```bash
  poe dev
  ```

  OR

  ```bash
  poe dev server
  ```

- **Server App (legacy):**

  ```bash
  poe dev server:legacy
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
  poe demo
  ```

<!-- Usage -->

## :eyes: Usage

### Server:

You will have to start the server manually by running the
`src/server/server.py`:

```bash
python src/server/server.py
```

### Server App

Run the server:

```bash
poe dev
```

OR

```bash
poe dev server
```

After the app starts, you will have to start the server manually by clicking the
`Start server` button.

The server will run on with port `5656` and with host `0.0.0.0`, which is **the
IP address of your local machine**.

To stop the server, click the `Stop server` button.

<details>
<summary>Behind the scene</summary>

We you click the `Start server` button, the app will start an `uvicorn` server
in different process, and store the process ID for later use.

When you click the `Stop server` button, the app will find child process with
the ID stored before and kill it, then terminate the parent process.

</details>

### Client App

Run the client app:

```bash
poe dev client
```

Connect to the server by entering the server's IP address and port:

- **IP address:** The IP address of your server machine.
- **Port:** `5656`.

### Mail App

> **Note**: To use this app, you need to provide the `credentials.json` file in
> the root directory. Please follow the instructions in the page:
> [Python quickstart](https://developers.google.com/gmail/api/quickstart/python)
> to create your own App and download the `credentials.json` file.

Run the mail app:

```bash
poe dev mail
```

#### Authorize the app

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

#### Send mail

You can send an email to the address you logged in to the app.

- Currently, the max number of emails that are fetched from the server is `5`.

#### Instruction format

```
(<command>:<options>)
```

- **command**: The command to execute. The command is case-sensitive.
- **options**: The options of the command. The options are separated by `;`. The
  allowed characters are alphanumeric characters, `\`, `:`, `;` and `.`.
  > **Note**: The `options` is optional and can be omitted.

> **Note**: Each `instruction` don't have to be on a separate line.

E.g.:

```
(command) # without options
(command:option1;option2) # with multiple options
(command1:) # with empty option
(command1:)(command2) # multiple instructions on the same line
```

  <details>
  <summary>Regex pattern</summary>

```python
cmdPattern = "|".join(DEFAULT_COMMANDS)
pattern = rf"\((?P<type>{cmdPattern})(?:\:(?P<options>[\w\\:;\.]*))?\)"
```

  </details>

#### Supported instructions

- `shutdown`: Shutdown the server machine.

  - Example:

    ```
    (shutdown)
    ```

- `logout`: Log out the current user.

  - Example:

    ```
    (logout)
    ```

- `mac_address`: Get the MAC address of the server machine.

  - Example:

    ```
    (mac_address)
    ```

- `screenshot`: Take a screenshot of the server machine.

  - Example:

    ```
    (screenshot)
    ```

- `list_directory`: List directories and files in the given path.

  - **Options**:

    - `path`: The path to list.

  - Example:

    ```
    (list_directory:C:\Users\Alice\Desktop)
    ```

- `copy_file_to_server`: Copy a file from the client machine to the server
  machine.

  - **Options**:

    - `srcPath`: The path to the file on the client machine.
    - `destPath`: The **directory** path to the file on the server machine.
      > **Note**: The file name from `srcPath` will be appended to the
      > `destPath`.

  - Example:

    ```
    (copy_file_to_server:C:\Users\Alice\Desktop\test.txt;C:\Users\Alice\Desktop\)
    ```

    This will copy the file `test.txt` from the client machine to the directory
    `C:\Users\Alice\Desktop\` on the server machine. The final path of the file
    is: `C:\Users\Alice\Desktop\test.txt`.

- `copy_file_to_client`: Copy a file from the server machine to the client
  machine.

  - **Options**:

    - `srcPath`: The path to the file on the server machine.
    - `destPath`: The **directory** path to the file on the client machine.

      > **Note**: The file name from `srcPath` will be appended to the
      > `destPath`.

  - Example:

    ```
    (copy_file_to_client:C:\Users\Alice\Desktop\test.txt;C:\Users\Alice\Desktop\)
    ```

    This will copy the file `test.txt` from the server machine to the directory
    `C:\Users\Alice\Desktop\` on the client machine. The final path of the file
    is: `C:\Users\Alice\Desktop\test.txt`.

- `delete_file`: Delete a file on the server machine.

  - **Options**:

    - `path`: The path to the file on the server machine.

  - Example:

    ```
    (delete_file:C:\Users\Alice\Desktop\test.txt)
    ```

- `list_process`: List all the processes on the server machine.

  - Example:

    ```
    (list_process)
    ```

- `list_application`: List all the applications on the server machine.

  - Example:

    ```
    (list_application)
    ```

- `kill_process`: Kill a process on the server machine.

  - **Options**:

    - `pid`: The process ID of the process to kill.

  - Example:

    ```
    (kill_process:1234)
    ```

#### Execute instructions

You can execute instructions by clicking the `Run` button on the right side of
the parsed instructions from received messages.

The result will be send back to the email sender. By default, the message will
be **sent as a reply** to the received message. The reply message may have
attachments.

### Dear PyGui Demo

Run the demo:

```bash
poe dev demo
```

The demo will demonstrate all the features of the Dear PyGui library.

### CLI

```bash
Usage: cli.py [OPTIONS] [SERVICE]:[server|server:legacy|client|mail]

Arguments:
  [SERVICE]:[server|server:legacy|client|mail]  Service to run  [default: server]

Options:
  --help  Show this message and exit.
```

<!-- Roadmap -->

## :compass: Roadmap

- [x] Rebuild the server with `Dear PyGui`.
- [ ] Rebuild the client app with `Dear PyGui`.
- [x] Support more features for Mail App.
  - [x] Copy files to client computer.
  - [x] Copy files to server computer.
  - [x] Delete files.

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
