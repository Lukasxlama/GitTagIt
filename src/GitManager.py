#########################
# Project: GitTagIt     #
# Version: 1            #
#                       #
# Code by LukasxLama :) #
#########################


### Imports ###
from LogManager import LogManager
from typing import Optional
from logging import Logger
from pathlib import Path

import git


### Logging ###
logger: Logger = LogManager().getLogger()


### Class ###
class GitManager:
    def __init__(self) -> None:
        """
        Initializes the GitManager.

        :return: None.
        """

        self._currentRepoPath: Optional[Path] = None
        self.__repo: Optional[git.Repo] = None

        self._currentTag: Optional[str] = None
        self.__currentTagReference: Optional[git.TagReference] = None

    @property
    def currentRepoPath(self) -> Optional[Path]:
        """
        Property for the repository path if set.

        :return: The path object of the repository.
        """

        return self._currentRepoPath

    @currentRepoPath.setter
    def currentRepoPath(self, newPath) -> None:
        """
        Sets a new repository path.

        :return: None.
        """

        self._currentRepoPath = Path(newPath)

    @property
    def currentTag(self) -> Optional[str]:
        """
        Property for the current tag if set.

        :return: The name of the tag.
        """

        return self._currentTag

    @currentTag.setter
    def currentTag(self, tagName: str) -> None:
        """
        Property for the current tag.

        :return: The tag object of the current tag.
        """

        if self._currentTag is not None:
            logger.warning("[GitManager@currentTag.setter] Warning: Deleting previous tag")
            git.TagReference.delete(self.__repo, self.__currentTagReference)

        if not self.__repo.head.is_valid():
            raise ValueError("[GitManager@currentTag] Cannot create tag: No commit found (HEAD is invalid).")

        self.__currentTagReference = self.__repo.create_tag(tagName)
        self._currentTag = tagName
        logger.info(f'[GitManager@currentTag.setter] Tag "{self._currentTag}" added successfully')

    def loadRepo(self) -> None:
        """
        Loads the git repository.

        :return: None.
        """

        if self._currentRepoPath is None:
            raise ValueError("[GitManager@loadRepo] Repository Path not set")

        if self._currentRepoPath.exists() and self._currentRepoPath.is_dir():
            try:
                self.__repo = git.Repo(self._currentRepoPath)
                logger.info(f'[GitManager@loadRepo] Repository "{self._currentRepoPath}" loaded successfully')

            except git.exc.InvalidGitRepositoryError:
                raise Exception(f'[GitManager@loadRepo] "{self._currentRepoPath}" is not a valid repository')

            except Exception as ERR_01:
                raise Exception(f'[GitManager@loadRepo] Unknown error occurred: {ERR_01}')

        else:
            raise Exception(f'[GitManager@loadRepo] "{self._currentRepoPath}" does not exist or is not a directory')

    def checkForChanges(self) -> bool:
        """
        Checks whether uncommitted changes or untracked files are in the repository.

        :return: True if there are changes, False otherwise.
        """

        if self.__repo.is_dirty(untracked_files=True):
            logger.error("[GitManager@checkForChanges] Uncommitted changes or untracked files found.")
            return True

        else:
            logger.info("[GitManager@checkForChanges] No changes found in the repository.")
            return False

    def addFiles(self, filePattern: str = '.') -> None:
        """
        Adds specific files or all changes to the staging area.
        
        :param filePattern: The Pattern to match.
        :return: None.
        """

        try:
            self.__repo.git.add(filePattern)
            logger.info(f'[GitManager@addFiles] Added files with pattern "{filePattern}" to staging area.')

        except Exception as ERR_02:
            logger.error(f"[GitManager@addFiles] Error adding files: {ERR_02}")

    def commit(self, message: str) -> None:
        """
        Commits all changes.

        :param message: The commit message.
        :return: None.
        """

        try:
            if self.checkForChanges():
                self.__repo.git.commit('-m', message)
                logger.info(f'[GitManager@commitAll] Committed changes with message "{message}" successfully.')

        except Exception as ERR_03:
            logger.error(f"[GitManager@commitAll] Error committing changes: {ERR_03}")

    def push(self) -> None:
        """
        Pushes the latest commit and the optional tag to the remote repository.

        :return: None.
        """

        try:
            origin: git.Remote = self.__repo.remote(name="origin")
            origin.push()
            logger.info("[GitManager@pushCommitAndTag] Pushed commit to origin.")

            if self._currentTag:
                origin.push(self._currentTag)
                logger.info(f"[GitManager@pushCommitAndTag] Pushed tag '{self._currentTag}' to origin.")

        except Exception as ERR_04:
            logger.error(f"[GitManager@pushCommitAndTag] Error pushing commit or tag: {ERR_04}")
