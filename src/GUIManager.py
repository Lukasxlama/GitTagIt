##################################
# Project: GitTagIt             #
# Version: 1                    #
#                               #
# Code by LukasxLama :)         #
##################################

### Imports ###
from CTkMessagebox import CTkMessagebox
from LogManager import LogManager
from GitManager import GitManager
from tkinter import filedialog
from logging import Logger
from pathlib import Path
from threading import Thread

import customtkinter as ctk


### Logging ###
logger: Logger = LogManager().getLogger()


### Class ###
class GUIManager(ctk.CTk):
    def __init__(self):
        """
        Initializes the GitTagIt GUI.

        :return: None.
        """
        super().__init__()

        self.title("GitTagIt - Commit & Tag")
        self.geometry("600x300")
        self.resizable(False, False)

        self.gitManager = GitManager()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Input field for repository path
        self.repoPathLabel = ctk.CTkLabel(self, text="Repository Path:")
        self.repoPathLabel.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")

        self.repoPathEntry = ctk.CTkEntry(self, width=400, placeholder_text="Select or enter the repository path")
        self.repoPathEntry.grid(row=0, column=1, padx=10, pady=(20, 10), sticky="ew")

        self.browseButton = ctk.CTkButton(self, text="Browse", width=80, command=self.browseRepoPath)
        self.browseButton.grid(row=0, column=2, padx=10, pady=(20, 10))

        # Input field for commit message
        self.commitMessageLabel = ctk.CTkLabel(self, text="Commit Message:")
        self.commitMessageLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.commitMessageEntry = ctk.CTkEntry(self, placeholder_text="Enter the commit message")
        self.commitMessageEntry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        # Input field for tag name
        self.tagNameLabel = ctk.CTkLabel(self, text="Tag Name:")
        self.tagNameLabel.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.tagNameEntry = ctk.CTkEntry(self, placeholder_text="Enter an optional tag name")
        self.tagNameEntry.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        # Commit and push button
        self.commitPushButton = ctk.CTkButton(self, text="Commit & Push",
                                              command=lambda: Thread(target=self.commitAndPush).start())
        self.commitPushButton.grid(row=3, column=0, columnspan=3, padx=10, pady=20, sticky="ew")

    def browseRepoPath(self) -> None:
        """
        Opens a file dialog to browse for the repository path and sets the path in the entry field.

        :return: None.
        """
        if repoPath := filedialog.askdirectory(title="Select Git Repository"):
            self.repoPathEntry.delete(0, ctk.END)
            self.repoPathEntry.insert(0, repoPath)

    def commitAndPush(self) -> None:
        """
        Executes commit and push logic by interacting with the GitManager.

        :return: None.
        """

        repoPath = Path(self.repoPathEntry.get().strip())
        commitMessage = self.commitMessageEntry.get().strip()
        tagName = self.tagNameEntry.get().strip()

        logger.debug(f"[GUIManager@commitAndPush]\n\trepoPath: {repoPath}\n\tcommitMessage: "
                     f"{commitMessage}\n\ttagName: {tagName}")

        if not repoPath or not repoPath.exists():
            CTkMessagebox(title="Error", message="Please select a valid repository path.", icon="cancel")
            return

        if not commitMessage:
            CTkMessagebox(title="Error", message="Please provide a commit message.", icon="cancel")
            return

        try:
            self.gitManager.currentRepoPath = repoPath
            self.gitManager.loadRepo()

        except Exception as ERR_01:
            CTkMessagebox(title="Error", message=f"Failed to load repository: {ERR_01}", icon="cancel")
            return

        try:
            self.gitManager.addFiles(filePattern='.')
            self.gitManager.commit(commitMessage)

            if tagName:
                self.gitManager.currentTag = tagName

            self.gitManager.push()

            CTkMessagebox(title="Success", message="Changes committed and pushed successfully!", icon="check")

        except Exception as ERR_02:
            CTkMessagebox(title="Error", message=f"Failed to commit or push changes. "
                                                 f"Look in critical.log for more information", icon="cancel")
            logger.critical(ERR_02, exc_info=True)
