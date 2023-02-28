import telebot
from telebot import types
from ELTtools import converter, spell_checker
from ELTtools import texts_cleaner
import os
import time
texts_path = "/home/sadraplyrics/Desktop/Programming/DataScieince/python/data_science/nlp_paper/texts/"
with open("token.txt", "r") as tok_file:
    TOKEN = tok_file.read()

NLPbot = telebot.TeleBot(TOKEN)

start_message = "Hello! We are happy to see you using our ELT bot\n\
Use the command /check to submit the document you would like to spellcheck\n\
Use the command /correct to activate a simple chatbot\n\
Use the command /convert to convert unmarked pdf to txt"

@NLPbot.message_handler(commands=["start", "help"])
def start(message):
    NLPbot.send_message(message.chat.id, start_message)


@NLPbot.message_handler(commands=["check"])
def spell_check(message):
    msg = NLPbot.reply_to(message, "Please, submit the document you would love to check")
    NLPbot.register_next_step_handler(msg, spell_check_2)    
def spell_check_2(message):
    try:
        if message.document.mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or message.document.mime_type == "text/plain":
            document_id = message.document.file_id
            document_path = NLPbot.get_file(document_id).file_path
            downloaded_file = NLPbot.download_file(document_path)

            with open(f"{texts_path}{message.document.file_name}", \
                "wb") as new_file:
                new_file.write(downloaded_file)
            without_ext = message.document.file_name.split('.')[0]
            NLPbot.send_message(message.chat.id,"Submitted!")
            if message.document.mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                print("check")
                spell_checker.docx_spell_checker(without_ext)
                with open(f"texts/{without_ext}.txt", "rb") as reply_doc:
                    NLPbot.send_document(message.chat.id, reply_doc)
            elif message.document.mime_type == "text/plain":
                print("check")
                spell_checker.txt_spell_checker(without_ext)
                with open(f"texts/{without_ext}.txt", "rb") as reply_doc:
                    NLPbot.send_document(message.chat.id, reply_doc)
            texts_cleaner.delete_all_files_from_texts()
        else:
            NLPbot.send_message(message.chat.id, "Please send .docx or .txt\nTo convert marked pdf to txt you may use \convert command")
    except Exception as ex:
        print(ex)
        NLPbot.send_message(message.chat.id, "Something went wrong, try again")


# This command takes in a pdf, converts it to txt and send it back 
# to the user

@NLPbot.message_handler(commands=["convert"])
def convert_command(message):
    msg = NLPbot.reply_to(message, "Please, submit a PDF you would love to convert to a .txt")
    NLPbot.register_next_step_handler(msg, file_downloader1)    
def file_downloader1(message):
    try:
        if message.document.mime_type == "application/pdf":
            document_id = message.document.file_id
            document_path = NLPbot.get_file(document_id).file_path
            downloaded_file = NLPbot.download_file(document_path)
            with open(f"{texts_path}{message.document.file_name}", \
                "wb") as new_file:
                new_file.write(downloaded_file)
            without_ext = message.document.file_name.split('.')[0]
            NLPbot.send_message(message.chat.id,"Submitted!")
            converter.custom_convert_function(without_ext)
            with open(f"texts/{without_ext}.txt", "rb") as reply_doc:
                NLPbot.send_document(message.chat.id, reply_doc)
            time.sleep(1)
            texts_cleaner.delete_all_files_from_texts()
        else:
            NLPbot.send_message(message.chat.id, "Please, submit a PDF document")
    except Exception as ex:
        print(ex)
        NLPbot.send_message(message.chat.id, "Something went wrong, try again")



@NLPbot.message_handler(commands=["correct"])
def correct_command(message):
    msg = NLPbot.reply_to(message, "Please, submit a .txt document that you would like to correct")
    NLPbot.register_next_step_handler(msg, file_downloader)    
def file_downloader(message):
    try:
        if message.document.mime_type == "text/plain":
            document_id = message.document.file_id
            document_path = NLPbot.get_file(document_id).file_path
            downloaded_file = NLPbot.download_file(document_path)
            NLPbot.send_message(message.chat.id,"Submitted!")
            with open(f"{texts_path}{message.document.file_name}", \
                "wb") as new_file:
                new_file.write(downloaded_file)
            without_ext = message.document.file_name.split('.')[0]
            spell_checker.simple_corrector(without_ext)
            with open(f"texts/{without_ext}.txt", "rb") as reply_doc:
                NLPbot.send_document(message.chat.id, reply_doc)
            time.sleep(1)
            texts_cleaner.delete_all_files_from_texts()
        else:
            NLPbot.send_message(message.chat.id, "Please, submit a .txt document")
    except Exception as ex:
        print(ex)
        NLPbot.send_message(message.chat.id, "Something went wrong, try again")






    # Older verison of the download_file funcion
    """final_link = f"https://api.telegram.org/file/bot{TOKEN}/{document_path}"
    print(final_link)
    final = requests.get(final_link, allow_redirects=True)
    open(f"/home/sadraplyrics/Desktop/Programming/DataScieince/python/data_science/nlp_paper/texts\
        /{message.document.file_name}", "wb").write(final.content)"""



if __name__ == "__main__":
    NLPbot.enable_save_next_step_handlers(delay=2)
    NLPbot.load_next_step_handlers()
    NLPbot.polling()