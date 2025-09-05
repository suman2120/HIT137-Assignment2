'''Program that reads the text file "raw_text.txt", encrypts its contents using a simple encryption method, and writes the encrypted text to a new file
"encrypted_text.txt". Then create a function to decrypt the content and a function to verify the decryption was successful '''

# Function to shift a letter forward within start-end range with wrap-around.
def shift_forward(char, shift_amount, start, end):
    new_ord = ord(char) + shift_amount  #shift letter forward
    if new_ord > ord(end):        # if it goes past the end letter, it wraps back to start.(eg. shifting z froward by 1 = a)
        new_ord = ord(start) + (new_ord - ord(end) - 1)
    return chr(new_ord)   #return new character

# Function to shift a letter backward within start-end range with wrap-around.
def shift_backward(char, shift_amount, start, end):
    new_ord = ord(char) - shift_amount #shift letter backward
    if new_ord < ord(start):   #wrap around if before start
        new_ord = ord(end) - (ord(start) - new_ord - 1)
    return chr(new_ord)


# Function to encrypt single character
def encrypt_char(char, shift1, shift2):
    if 'a' <= char <= 'm':   # if it is lowercase from a-m
        return shift_forward(char, shift1 * shift2, 'a', 'z')
    elif 'n' <= char <= 'z':  # if it is in lowercase from n-z
        return shift_backward(char, shift1 + shift2, 'a', 'z')
    elif 'A' <= char <= 'M':  # if it is in uppercase from A-M
        return shift_backward(char, shift1, 'A', 'Z')
    elif 'N' <= char <= 'Z':  # if it is in uppercase from N-Z
        return shift_forward(char, shift2 ** 2, 'A', 'Z')
    else:           # if it is numbers, spaces, punctuation
        return char

# Function to  decrypt single character using original character
def decrypt_char(char, shift1, shift2, original_char):
    if 'a' <= original_char <= 'm':  # reverse lowercase a-m
        return shift_backward(char, shift1 * shift2, 'a', 'z')
    elif 'n' <= original_char <= 'z': # reverse lowercase a-z
        return shift_forward(char, shift1 + shift2, 'a', 'z')
    elif 'A' <= original_char <= 'M': # reverse uppercase A-M
        return shift_forward(char, shift1, 'A', 'Z')
    elif 'N' <= original_char <= 'Z': # reverse uppercase N-Z
        return shift_backward(char, shift2 ** 2, 'A', 'Z')
    else:  # non-alphabet characters
        return char

# Function to encrypt full text
def encrypt_text(text, shift1, shift2):
    return "".join(encrypt_char(c, shift1, shift2) for c in text)  # encrypt a whole text string, letter by letter


# Function to decrypt full text
def decrypt_text(encrypted_text, raw_text, shift1, shift2):
    # pair each encrypted character with its original character
    return "".join(
        decrypt_char(enc, shift1, shift2, orig) # decrypt one character using the original letter to know which rule to reverse
                   for enc, orig in zip(encrypted_text, raw_text))   # loop through encrypted and original letters together


# Function to verify decryption 
def verify_decrypt(original_text, decrypted_text):
    if original_text == decrypted_text:
        print("Decryption is successful. Raw texts and decrypted texts match.")
    else:
        print("Decryption is failed. Raw texts and decrypted texts doesn't match")


# Function to validate input entered by users
def get_valid_input(prompt):
    while True:
        value = input(prompt)   # get input by user
        if value.isdigit():    # check whether the input is valid number or not
            return int(value)
        print("Invalid input, Please enter a number only")  # if user enter invalid input, ask to enter a valid number


# Main program
def main():
    # Get shift values from user
    shift1 = get_valid_input("Enter shift1 (number): ")
    shift2 = get_valid_input("Enter shift2 (number): ")

    # Read raw text
    with open("ques1/raw_text.txt", "r",) as file:
        raw_text = file.read()

    # Encrypt raw text and save
    encrypted_text = encrypt_text(raw_text, shift1, shift2)
    with open("ques1/encrypted_text.txt", "w",) as file:
        file.write(encrypted_text)

    # Decrypt encrypt text and save
    decrypted_text = decrypt_text(encrypted_text, raw_text, shift1, shift2)
    with open("ques1/decrypted_text.txt", "w",) as file:
        file.write(decrypted_text)

    # Verify decryption is successful or not 
    verify_decrypt(raw_text, decrypted_text)

# Run main function
main()
