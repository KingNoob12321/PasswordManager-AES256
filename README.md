Hello!

To launch this script, go to your terminal and just type "python", then copy and paste the script.

How it is secure:
  It uses AES256 encryption that is literally used for military!
  It uses Salting, so you absolutely need the master password to decrypt it.
  The key is saved in your RAM and gets deleted the MOMENT you close the terminal window. It will never be saved to a hard drive.
  You can add, generate or view your passwords completely decrypted (which leaves no footprints)! Also, the generator uses every single ASCII approved character, so you can use it anywhere.

Though, PLEASE do NOT put valuable accounts like your bank account or master email. This is good, sure. But you can't beat million dollar companies with no money!

And yes, adding a master password into the script like plain text is on purpose, because if a hacker ever has access to directly read your local scripts, it is already over. But if you want to hash it, it is entirely possible!

Here's a tutorial actually.

open your terminal (or VS code or anything that supports python!) and type python, then put this:

  import hashlib
  print(hashlib.sha256("YOUR_SECRET_PASSWORD".encode()).hexdigest())

after that, open the script, and delete the master_password: "The MasterPassword" or anything similar, and replace it with:

  import hashlib (Add this at the TOP, right under the other imports if you want it to be clean!)

  STORED_HASH = "your_64_character_fingerprint_here"

right under login = input("Enter the master password. ") add

  input_hash = hashlib.sha256(login_input.encode()).hexdigest()

after that, replace  

  if login == master_password:
      print("Access granted! Welcome to the program!")
  else:
      print("Access denied! Maybe you typed it wrong.")
      sys.exit()

with

  if input_hash == STORED_HASH:
      print("Access granted! Welcome to the program!")
  else:
      print("Access denied! Maybe you typed it wrong.")
      sys.exit()

  and it should work!
