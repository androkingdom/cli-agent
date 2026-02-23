from pathlib import Path
from typing import Any, Iterable


class SecureFileSystem:
    DEFAULT_DENY = {
        ".git",
        ".env",
        ".ssh",
        "__pycache__",
        ".cli_agent",
        "venv",
    }

    DEFAULT_ALLOWED_EXT = {
        ".py", ".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".html", ".css", ".js"
    }

    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

    def __init__(
        self,
        root: Path,
        deny_names: Iterable[str] | None = None,
        allowed_ext: Iterable[str] | None = None,
    ) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

        self.deny_names = set(deny_names or self.DEFAULT_DENY)
        self.allowed_ext = set(allowed_ext or self.DEFAULT_ALLOWED_EXT)

    # ----------------------------
    # Internal helpers
    # ----------------------------

    def _resolve(self, user_path: str) -> Path:
        target = (self.root / user_path).resolve()

        if not str(target).startswith(str(self.root)):
            raise ValueError("Access outside workspace is not allowed.")

        if any(part in self.deny_names for part in target.parts):
            raise ValueError("Access to restricted path denied.")

        return target

    def _check_extension(self, path: Path) -> None:
        if path.suffix not in self.allowed_ext:
            raise ValueError("File type not allowed.")

    # ----------------------------
    # Public commands
    # ----------------------------

    def read(self, path: str) -> dict[str, Any]:
        try:
            p = self._resolve(path)
            if not p.exists() or not p.is_file():
                return {"error": "File not found"}

            self._check_extension(p)

            if p.stat().st_size > self.MAX_FILE_SIZE:
                return {"error": "File too large"}

            return {"content": p.read_text(encoding="utf-8")}

        except Exception as e:
            return {"error": str(e)}

    def write(self, path: str, content: str, force: bool = False) -> dict[str, Any]:
        try:
            p = self._resolve(path)
            self._check_extension(p)

            if p.exists() and not force:
                return {"error": "File exists. Use force=True to overwrite."}

            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")

            return {"success": True}

        except Exception as e:
            return {"error": str(e)}

    def ls(self, path: str = ".") -> dict[str, Any]:
        try:
            p = self._resolve(path)
            if not p.exists() or not p.is_dir():
                return {"error": "Directory not found"}

            items = [
                {
                    "name": item.name,
                    "type": "dir" if item.is_dir() else "file",
                }
                for item in p.iterdir()
                if not any(part in self.deny_names for part in item.parts)
            ]

            return {"items": items}

        except Exception as e:
            return {"error": str(e)}
        
from agents import function_tool


def build_file_tools(fs: SecureFileSystem):

    @function_tool
    def read(path: str) -> dict:
        """Read a file inside workspace."""
        return fs.read(path)

    @function_tool
    def write(path: str, content: str, force: bool = False) -> dict:
        """Write a file inside workspace."""
        return fs.write(path, content, force)

    @function_tool
    def ls(path: str = ".") -> dict:
        """List directory contents."""
        return fs.ls(path)

    return [read, write, ls]