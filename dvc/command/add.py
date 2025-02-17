import argparse
import logging

from dvc.command import completion
from dvc.command.base import CmdBase, append_doc_link

logger = logging.getLogger(__name__)


class CmdAdd(CmdBase):
    def run(self):
        from dvc.exceptions import (
            DvcException,
            RecursiveAddingWhileUsingFilename,
        )

        try:
            if len(self.args.targets) > 1 and self.args.file:
                raise RecursiveAddingWhileUsingFilename()

            self.repo.add(
                self.args.targets,
                recursive=self.args.recursive,
                no_commit=self.args.no_commit,
                fname=self.args.file,
                external=self.args.external,
                glob=self.args.glob,
                desc=self.args.desc,
            )

        except DvcException:
            logger.exception("")
            return 1
        return 0


def add_parser(subparsers, parent_parser):
    ADD_HELP = "Track data files or directories with DVC."

    parser = subparsers.add_parser(
        "add",
        parents=[parent_parser],
        description=append_doc_link(ADD_HELP, "add"),
        help=ADD_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-R",
        "--recursive",
        action="store_true",
        default=False,
        help="Recursively add files under directory targets.",
    )
    parser.add_argument(
        "--no-commit",
        action="store_true",
        default=False,
        help="Don't put files/directories into cache.",
    )
    parser.add_argument(
        "--external",
        action="store_true",
        default=False,
        help="Allow targets that are outside of the DVC repository.",
    )
    parser.add_argument(
        "--glob",
        action="store_true",
        default=False,
        help="Allows targets containing shell-style wildcards.",
    )
    parser.add_argument(
        "--file",
        help="Specify name of the DVC-file this command will generate.",
        metavar="<filename>",
    )
    parser.add_argument(
        "--desc",
        type=str,
        metavar="<text>",
        help=(
            "User description of the data (optional). "
            "This doesn't affect any DVC operations."
        ),
    )
    parser.add_argument(
        "targets", nargs="+", help="Input files/directories to add.",
    ).complete = completion.FILE
    parser.set_defaults(func=CmdAdd)
