""" Sonar Ping File script

This script allows you to input and process a text file containing Twitch chat logs 
and detect hate speech using HateSonar. The script's output will also be a text file 
containing the results of the hatesonar function, sonar.ping(), for each line of chat 
message (in the same order). The results will be structured as a list of ping results.

It accepts an argument for the text file's filepath.
"""


import argparse
import json
from hatesonar import Sonar


def arg_parse():
    """Parse arguments provided from the console"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset_path',
        type=str,
        help="The file path of the dataset where you want to merge the classes."
    )
    parser.add_argument(
        '--out',
        type=str,
        help="Desired output file name. Default: <filename_without_extension>-processed.txt"
    )
    arguments = parser.parse_args()

    return arguments


def ping_file(dataset_path):
    """Run ping function on each line in the chat log file
        :param dataset_path:    file path of the dataset 
                                (specify directory name if the file is under a folder)
    """
    sonar = Sonar() 
    input_file = open(dataset_path, 'r', encoding="utf-8")

    # to read and remove "\n" escape characters at the end of each chat message
    chat_lines = input_file.read().splitlines() 

    # to trim whitespaces before and after each chat message
    chat_lines = [each_line.strip() for each_line in chat_lines] 

    # to get only the message after the [timestamp] <username>
    chat_lines = [each_line.partition("> ")[2] for each_line in chat_lines]

    return [sonar.ping(each_line) for each_line in chat_lines]


def save_results(dataset_path, output_file, ping_results):
    """Save results to a text file
    :param output_path:    desired file name of the resulting text file 
                            (specify directory name if you want the file under an *existing* folder)
    """
    output_filename = dataset_path.split('.txt')[0]+"-processed.txt" if output_file is None else output_file

    with open(output_filename, 'w') as file:
        file.write(json.dumps(ping_results, indent=4))


def main(arguments):
    dataset_path = arguments.dataset_path
    output_file = arguments.out

    ping_results_per_chat = ping_file(dataset_path)
    save_results(dataset_path, output_file, ping_results_per_chat)


if __name__ == "__main__":
    arguments = arg_parse()
    main(arguments)