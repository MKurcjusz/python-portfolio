import openai
import requests
from PIL import Image
from io import BytesIO
import os
import PyPDF2
import nltk
import re
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from colorama import Fore, Style

# First, set up your API key and the model you want to use
openai.api_key = "your API key"
model_engine = "image-alpha-001"

instruction0 = "Hello, I am Cundall_AI_Bot. Please enter one of the numbers:"
instruction1 = "1 - if you want me to look through your files"
instruction2 = "2 - if you want me to generate an image for you"
instruction3 = "3 - if you want me to modify your image"
instruction4 = "4 - if you want to talk with me (but I mostly generate just nonsense - sorry)"
instruction99 = "99 - if you want to exit"

while True:
    print()
    print("____________________________________________________________")
    print()
    print(Fore.RED + instruction0 + Style.RESET_ALL)
    print()
    print(Fore.RED + instruction1 + Style.RESET_ALL)
    print(Fore.RED + instruction2 + Style.RESET_ALL)
    print(Fore.RED + instruction3 + Style.RESET_ALL)
    print(Fore.RED + instruction4 + Style.RESET_ALL)
    print() #print("0 - if you want to change my functionality")
    print(Fore.RED + instruction99 + Style.RESET_ALL)
    print()
    choice = input()
    
#----------------------------------------------------------------------------------------------------------    
    
    if choice == "1":
        # nltk.download('punkt')  # Download the NLTK tokenizer
        print(Fore.GREEN + "I can help you to look for information in all the .pdf files in your folder." + Style.RESET_ALL)
        directory = input("Please enter the folder path: ")
        #directory = r"C:\Users\m.kurcjusz\00_documents\multisport"
        question = "What do you want to find in the documents? "
        highlighted_question = f"{Fore.BLUE}{question}{Style.RESET_ALL}"

        # Create a Porter stemmer object
        stemmer = PorterStemmer()

        while True:
            print("_________________________")
            print(highlighted_question)
            query = input()
            if query.lower() in ["quit", "exit","99"]:
                break

            # Tokenize the query and apply stemming
            query_tokens = word_tokenize(query)
            stemmed_query = [stemmer.stem(token) for token in query_tokens]

            # Create a regular expression to match the stemmed query words
            query_regex = r"\b({})\b".format("|".join(stemmed_query))

            query_found = False

            for filename in os.listdir(directory):
                if filename.endswith(".pdf"):
                    with open(os.path.join(directory, filename), "rb") as pdf_file:
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            page_text = page.extract_text()
                            sentences = sent_tokenize(page_text)
                            prev_sentence = ""
                            for i, sentence in enumerate(sentences):
                                next_sentence = sentences[i+1] if i < len(sentences) - 1 else ""
                                words = word_tokenize(sentence)
                                # Apply stemming to the words in the sentence
                                stemmed_words = [stemmer.stem(word) for word in words]
                                # Use regular expression search to find stemmed query words
                                match = re.search(query_regex, " ".join(stemmed_words), re.IGNORECASE)
                                if match:
                                    query_found = True
                                    print()
                                    print("Found in file: ", filename)
                                    print("On page number: ", page_num + 1)
                                    print()
                                    # Highlight the query word and any matching stemmed words in the sentence
                                    highlighted_sentence = sentence
                                    for word in query_tokens:
                                        highlighted_sentence = highlighted_sentence.replace(word, f"{Fore.YELLOW}{word}{Style.RESET_ALL}")
                                    for j, word in enumerate(words):
                                        if stemmer.stem(word) in stemmed_query:
                                            highlighted_sentence = highlighted_sentence.replace(word, f"{Fore.YELLOW}{word}{Style.RESET_ALL}")
                                    print(prev_sentence, highlighted_sentence, next_sentence)
                                    print()
                                    print()

                                    # Give the option to open the file
                                    while True:
                                        open_file = input(f"Do you want to open {filename}? (y/n) ")

                                        if open_file.lower() == "y":
                                            os.startfile(os.path.join(directory, filename))
                                            break
                                        elif open_file.lower() == "n":
                                            break
                                        else:
                                            print("Please enter 'y' or 'n'.")
                                prev_sentence = sentence

            if not query_found:
                print(Fore.GREEN + "Sorry. There is no such word in the .pdf documents in the folder." + Style.RESET_ALL)

#----------------------------------------------------------------------------------------------------------                
        
    elif choice == "2":
        
     # Define your prompt and image parameters
        image_size = "1024x1024"
        num_images = 1
         
        
        while True:
            print(Fore.GREEN + "Which image do you want to generate? " + Style.RESET_ALL)
            prompt = input()
            if prompt.lower() in ["quit", "exit","99"]:
                break        

            # Send the request to the OpenAI API
            response = openai.Image.create(
                prompt=prompt,
                model=model_engine,
                size=image_size,
                num_images=num_images,
            )

            # Get the URL of the generated image and download it
            image_url = response['data'][0]['url']
            image_bytes = BytesIO(requests.get(image_url).content)

            # Display the generated image
            image = Image.open(image_bytes)
            image.show()
        
#----------------------------------------------------------------------------------------------------------                       

    elif choice == "3":
        
     # Define your prompt and image parameters
        image_size = "1024x1024"
        num_images = 1
         
        
        while True:
            print(Fore.GREEN + "Which image do you want to modify? Please enter the file path: " + Style.RESET_ALL)
            image_path_slash = input()
            image_path_quote = image_path_slash.replace("\\", "/")
            image_path = image_path_quote[1:-1]
            if image_path_slash.lower() in ["quit", "exit","99"]:
                break        
#"C:/Users/m.kurcjusz/09_Presentations/230428 Hackathon/image creation/beach1.png"
            response = openai.Image.create_variation(
              image=open(image_path, "rb"),
              n=1,
              size="1024x1024"
            )
            image_url = response['data'][0]['url']
            image_bytes = BytesIO(requests.get(image_url).content)

            # Display the generated image
            image = Image.open(image_bytes)
            image.show()
        
#----------------------------------------------------------------------------------------------------------                       

    elif choice == "4":
        print(Fore.GREEN + "Sorry in advance, as my answers are usually just without sense :) How can I help you? " + Style.RESET_ALL)
    
        
        while True:
            
            prompt = input()
            if prompt.lower() in ["quit", "exit","99"]:
                break  
        
            # Send a message to ChatGPT
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=20,
                n=1,
                stop=None,
                temperature=0.3,
                presence_penalty=0.2,
                frequency_penalty=0.2,
                best_of=1,
            )

            # Get the response from ChatGPT
            message = response.choices[0].text.strip()
            print(Fore.GREEN + "Response from Cundall_AI_Bot:" + Style.RESET_ALL, Fore.GREEN + message + Style.RESET_ALL)

#----------------------------------------------------------------------------------------------------------        
        
    elif choice == "99":
        break
        
    else:
        print("Invalid input. Please try again.")
