import os

from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(

    SUPABASE_URL,

    SUPABASE_KEY

)


def upload_report(pdf_path, user_email):

    file_name = os.path.basename(pdf_path)

    with open(pdf_path, "rb") as file:

        supabase.storage.from_(

            "reports"

        ).upload(

            file_name,

            file,

            {

                "content-type": "application/pdf"

            }

        )

    public_url = supabase.storage.from_(

        "reports"

    ).get_public_url(

        file_name

    )

    supabase.table(

        "reports"

    ).insert(

        {

            "user_email": user_email,

            "report_url": public_url

        }

    ).execute()

    return public_url