from collections import Counter
import math
import re


def read_input(filename):
    with open(filename) as file:
        return file.read()


def calculate_entropy(sequence):
    total = len(sequence)
    counts = Counter(sequence)
    probabilities = {symbol: count / total for symbol, count in counts.items()}  # .items() makes a pair: (symbol,count)
    entropy = -sum(p * math.log2(p) for p in probabilities.values() if p > 0)
    return entropy


def calculate_conditional_entropy(sequence, n):
    if n == 0:
        return calculate_entropy(sequence)

    ngrams = [sequence[i: i + n + 1] for i in range(len(sequence) - n)]
    ngram_counts = Counter(ngrams)
    prefix_counts = Counter([ngram[:-1] for ngram in ngrams])

    entropy = 0
    for ngram, count_ngram in ngram_counts.items():
        prefix = ngram[:-1]
        count_prefix = prefix_counts[prefix]

        # P(X|Y) = P(X,Y) / P(Y)
        if count_prefix > 0:
            p_conditional = count_ngram / count_prefix
        else:
            p_conditional = 0

        if p_conditional > 0:
            entropy -= (count_ngram / len(ngrams)) * math.log2(p_conditional)
        else:
            entropy -= 0

    return entropy


if __name__ == '__main__':
    # zad1
    language = "en"
    text = read_input(f"norm_wiki_{language}.txt")
    entropy_char = calculate_entropy(text)
    print(f"Entropy of characters for english language: {entropy_char}")

    # zad2
    text_words = re.findall(r'\b\w+\b', text)
    entropy_words = calculate_entropy(text_words)
    print(f"Entropy of words for english language: {entropy_words}")

    # zad3
    conditional_entropy = calculate_conditional_entropy(text, 1)
    print(f"Conditional entropy of the first order for english language: {conditional_entropy}")

    # zad4
    languages = ["en", "eo", "et", "ht", "la", "nv", "so"] # todo: pairs of language short and full name
    orders = [0, 1, 2, 3]


    for lang in languages:
        print(f"Language: {lang}")
        text = read_input(f"norm_wiki_{lang}.txt")
        text_words = re.findall(r'\b\w+\b', text)

        print(f"Entropy of characters for {lang} language: {calculate_entropy(text)}")
        print(f"Entropy of words for {lang} language: {calculate_entropy(text_words)}")

        for order in orders:
            print(f"Conditional entropy of the {order} order for {lang} language: {calculate_conditional_entropy(text, order)}")

    # zad 5
    samples = [0, 1, 2, 3, 4, 5]

    for sample in samples:
        print(f"Sample {sample}:")
        text = read_input(f"sample{sample}.txt")

        for order in orders:
            print(f"Conditional entropy of the {order} order for sample{sample}: {calculate_conditional_entropy(text, order)}")


