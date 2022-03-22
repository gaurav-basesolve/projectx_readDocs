import argparse
from pathlib import Path
import os
from pprint import pprint

from cli.base import aws_cp, check_access, save_access
from cli.service import projectx_service


def projectx_arg_parser():
    """Genereate CLI parser with command line parameters for user to interact with the application

    :return: An object with all parsed informations
    :rtype: argparse.parser
    """
    # create the top-level parser
    parser = argparse.ArgumentParser(
        description="ProjectX CLI Client.",
        epilog="""
    How to add your access-key to projectx (configure)
    $ projectx configure
    Enter deployment name> *********
    Enter your api_key> *************

    Execution Example (list):
    $ projectx list analysis --more --all
    $ projectx list analysis --sample-id <sample_id>

    Execution Example (download):
    $ projectx download <sample_id> 
    $ projectx download <sample_id> --file-list <comma seperated list of filenames to download>
    $ projectx download <sample_id> --download-directory <absolute path of the location to download files>""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparser = parser.add_subparsers(dest="command", required=True)

    # creating sub-parser 'configure'
    configurator = subparser.add_parser(
        "configure",
        help="""This command access no arguments.Helps to configure projectx-cli with API key.""",
    )

    # creating sub-parser 'list'
    listing = subparser.add_parser(
        "list",
        help="""List out available analysis and thier respective sample related details""",
    )

    # create sub-parser under 'list'
    listing_subparser = listing.add_subparsers(dest="sub_command", required=True)
    # listing_runs = listing_subparser.add_parser('runs', help='Get available flowcell ids')
    # listing_sample = listing_subparser.add_parser('samples', help='Get available samples ids')
    listing_analysis = listing_subparser.add_parser(
        "analysis", help="Get list of ProjectX- analysis"
    )

    # adding argument for 'analysis'
    # listing_files.add_argument('-flowcell',type=str, help='Get list of sample-ids that are associated with input flowcell id' ,)
    listing_analysis.add_argument(
        "-s",
        "--sample-id",
        type=str,
        help="List all available files under an analysis",
    )
    listing_analysis.add_argument(
        "-m", "--more", help="To see more meta data per analysis", action="store_true"
    )
    listing_analysis.add_argument(
        "-a",
        "--all",
        help="Show all available analysis. [Default 20].",
        action="store_true",
    )

    # creating sub-parser 'download'
    download = subparser.add_parser(
        "download", help="Download ProjectX analysis outputs"
    )

    # adding argument for 'download'
    download.add_argument(
        "-s",
        "--sample-id",
        required=True,
        type=str,
        help="Fetch outputs from analysis based on sample id",
    )
    download.add_argument(
        "-d",
        "--download-directory",
        help="Download location. [Default: ~/Downloads/projectx-download]",
        default=str(os.path.join(Path.home(), "Downloads")),
    )
    download.add_argument(
        "-f",
        "--file-list",
        type=str,
        help="list of comma separated filenames of the files to download",
    )

    # parsing arguments
    return parser.parse_args()


if __name__ == "__main__":
    """Parses the arguments and executes required functionalites"""
    args = projectx_arg_parser()

    if args.command == "configure":
        # Prompt user for input and store them
        deployment_name = input("Enter deployment name> ")
        apikey = input("Enter your api_key> ")
        if len(deployment_name) == 0:
            print("[Error]: Did not recieved any value for Deployment Name. Try again.")
        if len(apikey) == 0:
            print("[Error]: Did not recieved any value for API Key. Try again.")
        if len(apikey) != 0 or len(deployment_name) != 0:
            save_access(deployment_name, apikey)

    deployment_name, apikey = check_access()
    projectx_session = projectx_service(apikey, deployment_name)
    if not projectx_session.apikey_is_valid:
        exit("Invalid api key configured")

    if args.command == "list":
        if args.sub_command == "analysis":
            if args.sample_id:
                filepaths_retrieved = (
                    projectx_session.get_downloadable_files_from_analysis(
                        args.sample_id
                    )
                )
                sampleId_files = {}
                sampleId_files["files"] = [key for key in filepaths_retrieved[0].keys()]
                pprint(sampleId_files)
            else:
                sample_json = {}
                samples = projectx_session.get_analysis_samples(more=args.more)
                if len(samples) != 0:
                    sample_json["analysis"] = samples
                    if not args.all:
                        pprint(sample_json["analysis"][:20], sort_dicts=False)
                        if len(sample_json["analysis"]) > 20:
                            print(
                                "\n[INFO] You are seeing 20 results at a time. To see all those document you have access too, pass --all argument."
                            )
                    else:
                        pprint(sample_json["analysis"], sort_dicts=False)
                    if not args.more:
                        print(
                            "\n[INFO] Result list has flowcell-id, lims-id and sample-id right now. To get more data, pass --more argument"
                        )

        # key = check_access()
        # if args.flowcell:
        #     pass
        #     if check_input(client, db="GenotypePhenotype", key=key, flowcell=args.flowcell):
        #         sample_ids = runs_query(client, db="GenotypePhenotype", flowcell=args.flowcell)
        #         sampleId_json = {}
        #         sampleId_json['sample_id'] = [sample_id for sample_id in sample_ids[0]['sample_id']]
        #         pprint(sampleId_json)

        # if args.cmd == 'runs':
        #     key = check_access()
        #     flowcell_ids = runs_all(client, db='GenotypePhenotype', key=key)
        #     runs_json = {}
        #     if len(flowcell_ids)!=0:
        #         runs_json['flowcell_ids'] = [flowcell['flowcell_id'] for flowcell in flowcell_ids]
        #         pprint(runs_json)
        #     else:
        #         print('[INFO] You do not have access to projectx')

    if args.command == "download":
        if args.sample_id:
            filepaths_retrieved = projectx_session.get_downloadable_files_from_analysis(
                args.sample_id,
                filenames=args.file_list,
            )
            if filepaths_retrieved:
                for file in filepaths_retrieved[0]:
                    print("Downloading:", file)
                    aws_cp(
                        projectx_session,
                        args.download_directory,
                        filepaths_retrieved[0][file],
                        filepaths_retrieved[1],
                        filepaths_retrieved[2],
                        filepaths_retrieved[3],
                        filepaths_retrieved[4],
                    )
        else:
            print("[Error]: Please specify a valid sample_id")
