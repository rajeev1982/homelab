import os
import sys
import eyed3
from eyed3.id3.apple import GRP1


class IDE3TagManager:
    __audiofile: eyed3.core.AudioFile

    def __init__(self, filepath: str) -> None:
        audiofile = eyed3.load(filepath)
        if not audiofile:
            raise Exception("Failed to load audio file")

        self.__audiofile = audiofile
        if not self.__audiofile.tag:
            self.__audiofile.initTag()

    def get_tag_version(self) -> tuple[int, int, int] | None:
        if self.__audiofile.tag.version:  # type: ignore
            print(f"ID3 Tag version for file {self.__audiofile.path}: {self.__audiofile.tag.version}")  # type: ignore
            return self.__audiofile.tag.version  # type: ignore
        else:
            print(f"No ID3 Tag version found for file {self.__audiofile.path}")
            return None

    def does_tit1_exist(self) -> bool:
        return bool(
            self.__audiofile.tag
            and self.__audiofile.tag.frame_set.get(b"TIT1")  # type: ignore
            and len(self.__audiofile.tag.frame_set[b"TIT1"]) > 0  # type: ignore
        )

    def does_grp1_exist(self, data: str | None = None) -> bool:
        grp1_exists = bool(
            self.__audiofile.tag
            and self.__audiofile.tag.frame_set.get(b"GRP1")  # type: ignore
            and len(self.__audiofile.tag.frame_set[b"GRP1"]) > 0  # type: ignore
        )
        if not grp1_exists:
            return False

        if not data:
            return grp1_exists
        else:
            for tag in self.__audiofile.tag.frame_set[b"GRP1"]:  # type: ignore
                print(f"Existing GRP1 tag: {tag.data}")
                if tag.data == data:
                    print(f"GRP1 tag already exists with same data: {tag.data}")
                    return True
            return False

    def copy_tit1_to_grp1(self) -> None:
        if self.does_grp1_exist():
            del self.__audiofile.tag.frame_set[b"GRP1"]  # type: ignore

        if not self.does_tit1_exist():
            print(f"No TIT1 tag found for file: {self.__audiofile.path} ")
            return

        for tit1 in self.__audiofile.tag.frame_set[b"TIT1"]:  # type: ignore # type: ignore
            grp1: GRP1 = GRP1()
            grp1.__dict__ = tit1.__dict__.copy()  # type: ignore
            grp1.id = b"GRP1"
            self.__audiofile.tag.frame_set[b"GRP1"] = grp1  # type: ignore

        v_major: int
        v_minor: int
        v_rivision: int
        v_major, v_minor, v_rivision = self.get_tag_version() or (0, 0, 0)
        if v_major < 2 or (v_major == 2 and v_minor < 3):
            self.__audiofile.tag.save(version=(2, 3, 0))  # type: ignore
        else:
            self.__audiofile.tag.save()  # type: ignore

        print(f"Copied TIT1 to GRP1 for file: {self.__audiofile.path}")


class MusicManager:
    __folderpath: str | None

    def __init__(self, folderpath: str) -> None:
        self.__folderpath = folderpath

        if not folderpath or not os.path.exists(folderpath) or not os.path.isdir(folderpath):
            raise Exception(f"Folder path does not exist: {folderpath}")

    def update_ide3_tags(self) -> None:
        self.update_ide3_tags_for_folder(self.__folderpath)

    def update_ide3_tags_for_folder(self, folderpath: str | None) -> None:
        if not folderpath or not os.path.exists(folderpath) or not os.path.isdir(folderpath):
            raise Exception(f"Folder path does not exist: {folderpath}")

        for root, folders, files in os.walk(folderpath):
            for folder in folders:
                folderpath = os.path.join(root, folder)
                print(f"Processing folder: {folderpath}")
                self.update_ide3_tags_for_folder(folderpath)

            for file in files:
                if file.lower().endswith((".mp3")):
                    filepath = os.path.join(root, file)
                    print(f"Processing file: {filepath}")
                    try:
                        self.update_ide3_tags_for_file(filepath)
                    except Exception as e:
                        print(f"Error processing file {filepath}: {e}")

    def update_ide3_tags_for_file(self, filepath: str) -> None:
        tag_manager = IDE3TagManager(filepath)
        tag_manager.copy_tit1_to_grp1()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python copy_tit1_to_grp1_tag.py <path_to_music_folder>")
        sys.exit(1)

    folderpath = sys.argv[1]
    music_tag_manager = MusicManager(folderpath)
    music_tag_manager.update_ide3_tags()

    # IDE3TagManager("/Users/rajeev/DJ Music/Hindi/Dandiya Remixes/Piya Se Milan Gai.mp3").copy_tit1_to_grp1()
    # tag_manager = IDE3TagManager("/Users/rajeev/DJ Music/Hindi/Dandiya Remixes/Piya Se Milan Gai.mp3").get_tag_version()
