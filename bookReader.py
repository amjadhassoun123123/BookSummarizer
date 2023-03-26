import re
import openai

openai.api_key = "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"


def split_chapters(book_text):
    # Find all occurrences of the word "Chapter" followed by a number and their corresponding text
    chapters = re.findall(
        r'(Chapter \d+)([\s\S]*?)(?=Chapter \d+|$)', book_text)

    # Create a dictionary with chapter headings as keys and their corresponding text as values
    chapters_dict = {chapter: text.strip() for chapter, text in chapters}

    return chapters_dict


def getSummary(chapter_text):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are SummaryGPT, users will give you a chapter from a book, and you will return the summary of the chapter. At the end of the summary, give key points the reader should understand from the chapter."},
                {"role": "user", "content": f"Give me a summary of this chapter : {chapter_text}"}
            ]
        )
    except:
        return "Chapter was too long"
    return completion.choices[0].message["content"]


if __name__ == "__main__":
    bookName = input(
        "Input the name full name of the text file that contains the book: ")
    with open(bookName, "r", encoding="utf-8") as file:
        book_text = file.read()

    chapters_dict = split_chapters(book_text)

    # Sort the dictionary items by their chapter numbers
    sorted_chapters = sorted(chapters_dict.items(),
                             key=lambda x: int(x[0].split()[1]))

    with open(f"bookSummary{bookName}", "w", encoding="utf-8") as output_file:
        for chapter, chapter_text in sorted_chapters:
            summary = getSummary(chapter_text)
            output_file.write(f"{chapter}\n\n{summary}\n\n")
