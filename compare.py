import argparse
from re import sub


def check(text1, text2):
    """
    This function calculates the measure of similarity of the two given texts.
    It works according to dynamic programming approach of finding Levenshtein distance but instead of storing the
    whole table we store only one line which is called 'cur'. Thus, if there are N words in text1 and M words in text2,
    then the overall time complexity is O(N * M) and space complexity is O(min(N, M))
    """
    text1, text2 = sub(r'[^\w\s]', ' ', text1).split(), sub(r'[^\w\s]', ' ', text2).split()
    text1, text2 = [word.lower() for word in text1], [word.lower() for word in text2]
    n1, n2 = len(text1), len(text2)
    swapped = False
    if n1 < n2:
        n1, n2 = n2, n1
        swapped = True
    cur = [j for j in range(n2 + 3)]
    for i in range(1, n1 + 1):
        cur[n2 + 1] = cur[0]
        cur[0] += 1
        for j in range(1, n2 + 1):
            m = not (not swapped and text1[i - 1] == text2[j - 1] or swapped and text1[j - 1] == text2[i - 1])
            cur[n2 + 2] = cur[j]
            cur[j] = min(cur[j - 1] + 1, cur[j] + 1, cur[n2 + 1] + m)
            cur[n2 + 1] = cur[n2 + 2]
    return 1 - cur[n2] / n1


def similarity(input_file, output_file):
    """
    This function changes output_file with writing results of
    function check applied for each pair of texts listed in input_file
    """
    with open(input_file, encoding='utf8') as f:
        paths = f.read().splitlines()
        paths_count = len(paths)
        output = open(output_file, 'w')
        for i in range(paths_count):
            for j in range(i + 1, paths_count):
                f1, f2 = open(paths[i], 'r', encoding='utf8'), open(paths[j], 'r', encoding='utf8')
                data1, data2 = ''.join(f1.read().splitlines()), ''.join(f2.read().splitlines())
                output.write(str(check(data1, data2)) + '\n')
                f1.close()
                f2.close()
        output.close()


def my_parser():
    parser = argparse.ArgumentParser(description='anti-plagiarism check')
    parser.add_argument('input_path', type=str)
    parser.add_argument('output_path', type=str)
    return parser


def main():
    parser = my_parser()
    args = parser.parse_args()
    similarity(args.input_path, args.output_path)


if __name__ == '__main__':
    main()
