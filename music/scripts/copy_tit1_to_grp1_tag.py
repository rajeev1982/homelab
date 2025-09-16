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
        del self.__audiofile.tag.frame_set[b"GRP1"]  # type: ignore

        if not self.does_tit1_exist():
            print(f"No TIT1 tag found for file: {self.__audiofile.path} ")
            return

        for tit1 in self.__audiofile.tag.frame_set[b"TIT1"]:  # type: ignore # type: ignore
            # print(f"TIT1: {tit1.data}")
            grp1: GRP1 = GRP1()
            grp1.__dict__ = self.__audiofile.tag.frame_set[b"TIT1"][0].__dict__.copy()  # type: ignore
            grp1.id = b"GRP1"
            self.__audiofile.tag.frame_set[b"GRP1"] = grp1  # type: ignore

        self.__audiofile.tag.save()  # type: ignore
        print(f"Copied TIT1 to GRP1 for file: {self.__audiofile.path}")


if __name__ == "__main__":
    # import sys

    # if len(sys.argv) != 2:
    #     print("Usage: python copy_tit1_to_grp1_tag.py <path_to_music_folder>")
    #     sys.exit(1)

    # folderpath = sys.argv[1]

    filepath: str = "/Users/rajeev/Music/DJ Music/Hindi/Dance Songs/Besharam Rang.mp3"
    tag_manager = IDE3TagManager(filepath)
    tag_manager.copy_tit1_to_grp1()
