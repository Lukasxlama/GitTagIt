# GitTagIt

## Overview
**GitTagIt** is a Python-based GUI application designed to help users manage Git repositories with ease. It offers the ability to commit and tag changes in a repository via a user-friendly interface built with **CustomTkinter**. Logs for various operations (INFO, DEBUG, ERROR) are also saved for later reference.

### Features:
- Select a Git repository from your local system.
- Commit changes with a specified commit message.
- Optionally, add a tag to the commit.
- Push the changes and tag to the remote repository.
- Logging support for debugging and tracking operations.

## Project Structure

```plaintext
GitTagIt/
├── src/
│   ├── __main__.py         # Entry point for the application
│   ├── GitManager.py       # Manages Git operations
│   ├── GUIManager.py       # Handles the GUI for user interactions
│   ├── LogManager.py       # Configures and manages logging
├── log/                    # Log directory (generated after first run)
│   ├── info.log
│   ├── debug.log
│   ├── error.log
│   └── critical.log
└── README.md               # Project documentation
```

## Installation
Prerequisites:
- Python 3.11 or higher
- pip (Python package installer)
- Git installed on your system

## Clone the Repository
```bash
git clone https://github.com/lukasxlama/GitTagIt.git
cd GitTagIt/src
```

## Install Dependencies
```bash
pip install customtkinter gitpython CTkMessagebox
```

## Usage

1. **Run the Application**:
   Start the application by running the following command from the `src` directory:
   
   ```bash
   python __main__.py
   ```

2. **Select Repository**:
   - Use the "Browse" button to select the local Git repository you want to work with.

3. **Commit Changes**:
   - Enter your commit message in the designated field.
   - Optionally, provide a tag name if you want to tag the commit.

4. **Push to Remote**:
   - Click "Commit & Push" to execute the operations. The application will commit the changes, add the tag (if specified), and push everything to the remote repository.
     This may take a moment, but the program will not hang.

## Logging

GitTagIt provides a simple logging system that captures all major actions and errors. The logs are saved in the `log/` directory and are split into different files based on severity:

- **info.log**: Contains general information about routine operations, such as repository loading and successful commits.
- **debug.log**: Provides detailed debugging information, useful for troubleshooting during development or when issues arise.
- **error.log**: Logs errors that occur during usage, including stack traces to help with debugging.
- **critical.log**: Records critical issues that require immediate attention, such as major Git failures.

This logging system ensures that all important information is easily accessible for review and debugging. Logs are saved in rotating files with a maximum size of 5 MB, ensuring that the log directory does not grow excessively large.
