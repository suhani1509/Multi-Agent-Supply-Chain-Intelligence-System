import bcrypt

from database import supabase

password = "35693569"

hashed = bcrypt.hashpw(

    password.encode(),

    bcrypt.gensalt()

).decode()

supabase.table("users").insert(

    {

        "email": "supplychain.project.ai@gmail.com",

        "password_hash": hashed

    }

).execute()

print("User added")