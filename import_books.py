import pandas as pd
import os
import requests
from extensions import db
from models import Book
import time
from PIL import Image
import re
from wsgi import app

# Data import script 

UPLOAD_FOLDER = 'static/images/book_covers'

def download_image(image_url, title):
    """
    Download an image from a URL and save it as JPEG with the book title as filename.
    Returns None if the image is not successfully downloaded or is invalid.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Save the image as "title.jpg" (replace spaces for consistency)
        filename = f"{title.replace(' ', '_')[:100]}.jpg"  # Limit filename length
        image_path = os.path.join(UPLOAD_FOLDER, filename).replace("\\", "/")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        
        # Write image content to the file
        with open(image_path, 'wb') as f:
            f.write(response.content)
        
        # Verify the image and ensure it’s in JPEG format
        with Image.open(image_path) as img:
            width, height = img.size
            if img.format != 'JPEG' or width < 10 or height < 10 or os.path.getsize(image_path) == 0:
                os.remove(image_path)  # Remove the invalid image
                return None
        
        # Return the relative path for database storage
        return image_path.replace("static/", "")
    except Exception as e:
        print(f"Failed to download image for {title}: {e}")
        if 'image_path' in locals() and os.path.exists(image_path):
            os.remove(image_path)  # Remove any partially downloaded file
        return None

def import_books_from_csv(file_path):
    df = pd.read_csv(file_path)
    books_imported = 0
    books_skipped = 0
    books_updated = 0
    
    with app.app_context():
        for _, row in df.iterrows():
            # Extract only numeric characters for ISBN
            isbn = re.sub(r'\D', '', row['ISBN'])  # Keep only digits
            
            # Skip if ISBN is not a valid integer or empty
            if not isbn.isdigit():
                print(f"Invalid ISBN for '{row['Book-Title']}', skipping.")
                books_skipped += 1
                continue
            
            # Check if the book already exists
            existing_book = Book.query.filter_by(isbn=int(isbn)).first()
            
            if existing_book:
                # Update the existing book if needed
                if existing_book.imagepath is None:
                    image_path = download_image(row['Image-URL-L'], row['Book-Title'])
                    if image_path:
                        existing_book.imagepath = image_path
                        books_updated += 1
                        print(f"Updated image for existing book: {row['Book-Title']}")
                    else:
                        print(f"Failed to update image for existing book: {row['Book-Title']}")
                else:
                    print(f"Skipping existing book: {row['Book-Title']}")
                books_skipped += 1
                continue

            image_path = download_image(row['Image-URL-L'], row['Book-Title'])
            
            if image_path is None:
                print(f"Skipping book '{row['Book-Title']}' due to invalid or missing image")
                books_skipped += 1
                continue  # Skip to the next iteration if image is not good
            
            # Create and add the book to the database
            book = Book(
                isbn=int(isbn),  # Store ISBN as integer
                title=row['Book-Title'],
                author=row['Book-Author'],
                publicationyear=int(row['Year-Of-Publication']),
                publisher=row['Publisher'],
                imagepath=image_path  # Store the path of the saved image
            )
            db.session.add(book)
            books_imported += 1
            
            # Commit every 100 books to avoid large transactions
            if (books_imported + books_updated) % 100 == 0:
                db.session.commit()
                print(f"Processed {books_imported + books_updated} books so far...")
            
            time.sleep(1)  # Add a 1-second delay between requests
        
        # Final commit for any remaining books
        db.session.commit()
        print(f"Import completed. {books_imported} books imported, {books_updated} books updated, {books_skipped} books skipped.")

# Run the import function
if __name__ == "__main__":
    # Ensure the app context is available
    with app.app_context():
        import_books_from_csv('static/csv/books.csv')
