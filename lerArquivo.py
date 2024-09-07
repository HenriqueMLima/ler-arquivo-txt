import threading
from collections import defaultdict
import os

# Função para contar palavras em um segmento de texto
def count_words(segment, word_counts):
    word = ''
    for char in segment:
        if char.isalnum():
            word += char.lower()
        elif word:
            word_counts[word] += 1
            word = ''
    if word:
        word_counts[word] += 1

# Função para processar o arquivo em segmentos utilizando threads
def process_file(filename, n_threads):
    with open(filename, 'r') as file:
        content = file.read()
    
    file_size = len(content)
    segment_size = file_size // n_threads
    threads = []
    word_counts_list = [defaultdict(int) for _ in range(n_threads)]

    for i in range(n_threads):
        start = i * segment_size
        end = None if i == n_threads - 1 else (i + 1) * segment_size
        segment = content[start:end]
        thread = threading.Thread(target=count_words, args=(segment, word_counts_list[i]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_word_counts = defaultdict(int)
    for word_counts in word_counts_list:
        for word, count in word_counts.items(): 
            total_word_counts[word] += count

    for word, count in total_word_counts.items():
        print(f"Palavra '{word}': {count} vezes")

if __name__ == "__main__":
    filename = "texto.txt"
    if not os.path.exists(filename):
        print("Arquivo não encontrado o___o")
    else:
        n_threads = 4
        process_file(filename, n_threads)