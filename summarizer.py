from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization")


def generate_summary(book_content):
    summary = summarizer(book_content, max_length=50, min_length=4, do_sample=False)
    return summary[0]['summary_text']


# print(generate_summary("EdFinancial and the Oklahoma Student Loan Authority (OSLA) are notifying over 2.5
# million loanees that their personal data was exposed in a data breach. The target of the breach was Nelnet
# Servicing, the Lincoln, Neb.-based servicing system and web portal provider for OSLA and EdFinancial,
# according to a breach disclosure letter. Nelnet revealed the breach to affected loan recipients
# on July 21, 2022 via a letter."))
